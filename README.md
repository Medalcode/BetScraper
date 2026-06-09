# BetScraper Mundial 2026

Una herramienta de análisis multidimensional para apuestas deportivas, enfocada en la Copa Mundial 2026.

## Arquitectura Inicial
- **Base de Datos**: DuckDB, estructurada en un esquema de estrella (`Dim_Equipo`, `Fact_Momento_Equipo`).
- **Extracción de Datos**: Scraper automatizado que obtiene el Rating ELO en tiempo real desde `eloratings.net`.
- **Lenguaje**: Python 3.

## Configuración y Ejecución

1. Crea el entorno virtual e instala las dependencias:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Inicializa la base de datos DuckDB:
```bash
python db_schema.py
```

3. Descarga los datos y ejecuta el scraper ELO:
```bash
curl -s "https://www.eloratings.net/World.tsv" -o "World.tsv"
python scraper_elo.py
```