import pandas as pd
import duckdb
from datetime import date
import io

DB_PATH = 'worldcup.duckdb'
TSV_FILE = 'World.tsv'

def get_elo_data():
    print(f"Leyendo datos del archivo local {TSV_FILE}...")
    
    # El archivo TSV de eloratings tiene columnas separadas por tabulador
    df = pd.read_csv(TSV_FILE, sep='\t', header=None)
    
    # Extraemos el código de país (columna 2) y el ELO (columna 3)
    df_elo = df[[2, 3]].copy()
    df_elo.columns = ['codigo', 'rating_elo']
    
    conn = duckdb.connect(DB_PATH)
    
    registros = 0
    for index, row in df_elo.iterrows():
        codigo = str(row['codigo']).strip()
        try:
            rating = int(row['rating_elo'])
        except ValueError:
            continue
            
        # Insertar en Dim_Equipo ignorando duplicados si ya existe
        conn.execute('''
            INSERT INTO Dim_Equipo (nombre, confederacion) 
            VALUES (?, 'FIFA') 
            ON CONFLICT (nombre) DO NOTHING
        ''', (codigo,))
        
        # Obtener el equipo_id
        res = conn.execute('SELECT equipo_id FROM Dim_Equipo WHERE nombre = ?', (codigo,)).fetchone()
        if res:
            equipo_id = res[0]
            # Insertar en Fact_Momento_Equipo
            conn.execute('''
                INSERT INTO Fact_Momento_Equipo (equipo_id, fecha_actualizacion, rating_elo)
                VALUES (?, ?, ?)
            ''', (equipo_id, date.today(), rating))
            registros += 1
            
    print(f"Datos ELO insertados correctamente en DuckDB. Total registros: {registros}")
    
    # Mostrar los primeros 10 para verificar
    print("\nTop 10 Selecciones según el ELO actual en la DB:")
    top10 = conn.execute('''
        SELECT d.nombre, f.rating_elo
        FROM Fact_Momento_Equipo f
        JOIN Dim_Equipo d ON f.equipo_id = d.equipo_id
        WHERE f.fecha_actualizacion = current_date()
        ORDER BY f.rating_elo DESC
        LIMIT 10
    ''').fetchall()
    
    for r in top10:
        print(f"{r[0]}: {r[1]}")
        
    conn.close()

if __name__ == "__main__":
    get_elo_data()
