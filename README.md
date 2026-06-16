# BetScraper Mundial 2026

Una herramienta de análisis multidimensional para apuestas deportivas, enfocada en la Copa Mundial 2026.

## Arquitectura

El proyecto está diseñado de forma modular para permitir la ingesta masiva de datos:

- **`src/database/db_schema.py`**: Esquema de la base de datos analítica DuckDB. Define un esquema de estrella (`Dim_Equipo`, `Fact_Momento_Equipo`) optimizado con restricciones UPSERT para evitar duplicados históricos.
- **`src/scrapers/scraper_elo.py`**: Scraper automatizado optimizado con Pandas que obtiene el Rating ELO en tiempo real desde `eloratings.net` y realiza inserciones masivas en BD.
- **`src/scrapers/country_codes.py`**: Diccionario nativo para mapear códigos a nombres reales de países.

## Configuración y Ejecución

1. Crea el entorno virtual e instala las dependencias:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Inicializa la base de datos DuckDB:
```bash
python src/database/db_schema.py
```

3. Ejecuta la extracción de datos:
```bash
python src/scrapers/scraper_elo.py
```