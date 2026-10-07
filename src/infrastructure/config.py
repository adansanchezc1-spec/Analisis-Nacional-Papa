"""
Módulo de Configuración Global del Pipeline Analítico.
Centraliza rutas del sistema de archivos, constantes de negocio y mapeos de schema drift.
"""

from pathlib import Path

# Raíz del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Rutas del Sistema de Archivos Medallion
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "RAW"
RAW_SIPSA_DIR = RAW_DIR / "sipsa"
RAW_DEMO_DIR = RAW_DIR / "demografía"

CLEANED_DIR = DATA_DIR / "CLEANED"
FEATURES_DIR = DATA_DIR / "FEATURES"
CURATED_DIR = DATA_DIR / "CURATED"

# Asegurar existencia de directorios de salida
CLEANED_DIR.mkdir(parents=True, exist_ok=True)
FEATURES_DIR.mkdir(parents=True, exist_ok=True)
CURATED_DIR.mkdir(parents=True, exist_ok=True)

# Mapeo de Nombres de Columnas Canónicas (Esquema Unificado)
CANONICAL_COLUMNS = [
    "fecha_mes",
    "año",
    "mes",
    "divipola_depto",
    "nombre_depto",
    "divipola_mpio",
    "nombre_mpio",
    "mercado_mayorista",
    "alimento",
    "variedad_papa",
    "volumen_ingreso_ton",
    "precio_prom_kg",
    "precio_min_kg",
    "precio_max_kg",
    "num_transacciones",
]

# Diccionario de Sinonimias para Armonización de Schema Drift
COLUMN_RENAME_DICTIONARY = {
    # Fechas
    "FechaEncuesta": "fecha_cruda",
    "Fecha": "fecha_cruda",
    "FECHA": "fecha_cruda",
    "fecha": "fecha_cruda",
    # Departamentos
    "Cod. Depto Proc.": "cod_depto_crudo",
    "Código Departamento": "cod_depto_crudo",
    "Cod. Depto": "cod_depto_crudo",
    "Departamento Proc.": "nombre_depto_crudo",
    "Departamento": "nombre_depto_crudo",
    # Municipios
    "Cod. Municipio Proc.": "cod_mpio_crudo",
    " Código Municipio ": "cod_mpio_crudo",
    "Código Municipio": "cod_mpio_crudo",
    "Cod. Municipio": "cod_mpio_crudo",
    "Municipio Proc.": "nombre_mpio_crudo",
    "Municipio": "nombre_mpio_crudo",
    # Mercados
    "Fuente": "mercado_crudo",
    "\ufeffFuente": "mercado_crudo",
    "Cuidad, Mercado Mayorista": "mercado_crudo",
    "Mercado": "mercado_crudo",
    # Alimentos / Variedades
    "Grupo": "grupo_crudo",
    "Ali": "alimento_crudo",
    "Alimento": "alimento_crudo",
    # Cantidades y Precios
    "Cant Kg": "cantidad_kg_crudo",
    "Cantidad": "cantidad_kg_crudo",
    "Precio Prom": "precio_prom_crudo",
    "Precio Min": "precio_min_crudo",
    "Precio Max": "precio_max_crudo",
}
