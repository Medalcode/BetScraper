import duckdb

DB_PATH = 'worldcup.duckdb'

def init_db():
    print(f"Inicializando base de datos en {DB_PATH}...")
    conn = duckdb.connect(DB_PATH)
    
    # Sequencia para auto-incremento
    conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_equipo_id START 1;")
    
    # Crear Dim_Equipo
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Dim_Equipo (
        equipo_id INTEGER PRIMARY KEY DEFAULT nextval('seq_equipo_id'),
        codigo_iso VARCHAR(10) UNIQUE,
        nombre VARCHAR(100) UNIQUE,
        confederacion VARCHAR(50),
        titulos_mundiales INTEGER DEFAULT 0,
        partidos_historicos_ganados INTEGER DEFAULT 0
    );
    """)
    
    # Crear Fact_Momento_Equipo con la restriccion de unicidad
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Fact_Momento_Equipo (
        equipo_id INTEGER,
        fecha_actualizacion DATE,
        rating_elo INTEGER,
        FOREIGN KEY (equipo_id) REFERENCES Dim_Equipo(equipo_id),
        UNIQUE(equipo_id, fecha_actualizacion)
    );
    """)
    
    print("Tablas creadas y actualizadas exitosamente en DuckDB.")
    conn.close()

if __name__ == "__main__":
    init_db()
