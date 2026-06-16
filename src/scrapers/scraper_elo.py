import pandas as pd
import duckdb
from datetime import date
import logging
import subprocess
import io
import sys
import os

# Ajustar el path para importar country_codes
sys.path.append(os.path.dirname(__file__))
from country_codes import get_country_name

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_PATH = 'worldcup.duckdb'
TSV_URL = 'https://www.eloratings.net/World.tsv'

def get_elo_data():
    logger.info(f"Descargando datos de {TSV_URL}...")
    
    try:
        # Usamos curl para evitar bloqueos y timeout
        result = subprocess.check_output(['curl', '-s', TSV_URL])
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al descargar datos con curl: {e}")
        return
        
    df = pd.read_csv(io.BytesIO(result), sep='\t', header=None)
    df_elo = df[[2, 3]].copy()
    df_elo.columns = ['codigo', 'rating_elo']
    
    # Limpieza
    df_elo['codigo'] = df_elo['codigo'].astype(str).str.strip()
    df_elo['rating_elo'] = pd.to_numeric(df_elo['rating_elo'], errors='coerce')
    df_elo = df_elo.dropna(subset=['rating_elo'])
    df_elo['rating_elo'] = df_elo['rating_elo'].astype(int)
    
    # Aplicar mapeo de nombres
    df_elo['nombre'] = df_elo['codigo'].apply(get_country_name)
    
    logger.info("Datos parseados, procediendo a inserción masiva en DuckDB...")
    conn = duckdb.connect(DB_PATH)
    
    try:
        conn.execute("BEGIN TRANSACTION")
        
        # 1. Insertar en Dim_Equipo
        df_dim = df_elo[['codigo', 'nombre']].drop_duplicates()
        dim_data = list(df_dim.itertuples(index=False, name=None))
        conn.executemany('''
            INSERT INTO Dim_Equipo (codigo_iso, nombre, confederacion) 
            VALUES (?, ?, 'FIFA') 
            ON CONFLICT (nombre) DO NOTHING
        ''', dim_data)
        
        # 2. Obtener equipo_ids para Facts
        db_equipos = conn.execute('SELECT codigo_iso, equipo_id FROM Dim_Equipo').fetchdf()
        
        # 3. Preparar Facts
        df_facts = df_elo.merge(db_equipos, left_on='codigo', right_on='codigo_iso')
        df_facts['fecha_actualizacion'] = date.today()
        facts_data = df_facts[['equipo_id', 'fecha_actualizacion', 'rating_elo']]
        
        # 4. Inserción Masiva en Fact_Momento_Equipo (UPSERT)
        facts_tuples = list(facts_data.itertuples(index=False, name=None))
        conn.executemany('''
            INSERT INTO Fact_Momento_Equipo (equipo_id, fecha_actualizacion, rating_elo)
            VALUES (?, ?, ?)
            ON CONFLICT (equipo_id, fecha_actualizacion) 
            DO UPDATE SET rating_elo = EXCLUDED.rating_elo
        ''', facts_tuples)
        
        conn.execute("COMMIT")
        logger.info(f"Extracción finalizada. Total registros insertados/actualizados: {len(facts_data)}")
        
    except Exception as e:
        conn.execute("ROLLBACK")
        logger.error(f"Error procesando base de datos: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    get_elo_data()
