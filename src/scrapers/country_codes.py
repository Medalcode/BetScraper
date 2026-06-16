# Mapeo de códigos de ELO Ratings a Nombres Reales
COUNTRY_MAPPING = {
    'AR': 'Argentina',
    'ES': 'España',
    'FR': 'Francia',
    'BR': 'Brasil',
    'EN': 'Inglaterra',
    'PT': 'Portugal',
    'CO': 'Colombia',
    'NL': 'Países Bajos',
    'EC': 'Ecuador',
    'DE': 'Alemania',
    'UY': 'Uruguay',
    'IT': 'Italia',
    'BE': 'Bélgica',
    'HR': 'Croacia',
    'US': 'Estados Unidos',
    'MX': 'México',
    'CH': 'Suiza',
    'MA': 'Marruecos',
    'JP': 'Japón',
    'SN': 'Senegal',
    'CL': 'Chile',
    'PE': 'Perú',
    'VE': 'Venezuela'
    # Se puede extender según sea necesario
}

def get_country_name(code):
    if not isinstance(code, str):
        code = str(code)
    if code.lower() == 'nan':
        return 'Unknown'
    return COUNTRY_MAPPING.get(code.strip().upper(), code.strip())
