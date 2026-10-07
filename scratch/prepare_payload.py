import pandas as pd
import json
from pathlib import Path

# Paths
root = Path(r"c:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando")
eva_path = root / "data/CLEANED/dataset_eva_agricola_nacional.parquet"
sipsa_path = root / "data/CLEANED/dataset_sipsa_mensual_nacional.parquet"

df_eva = pd.read_parquet(eva_path)
df_sipsa = pd.read_parquet(sipsa_path)

# Normalize column names
col_a_eva = [c for c in df_eva.columns if 'a' in c.lower() and 'o' in c.lower() and len(c) <= 4][0]
df_eva = df_eva.rename(columns={col_a_eva: 'anio'})

col_a_sipsa = [c for c in df_sipsa.columns if 'a' in c.lower() and 'o' in c.lower() and len(c) <= 4][0]
df_sipsa = df_sipsa.rename(columns={col_a_sipsa: 'anio'})

def map_var(v):
    v = str(v).lower()
    if 'pastusa' in v: return 'Pastusa'
    if 'r-12' in v or 'r12' in v: return 'R-12'
    if 'criolla' in v or 'chaucha' in v: return 'Criolla'
    if 'capiro' in v or 'diacol' in v: return 'Diacol Capiro'
    if 'superior' in v: return 'Superior'
    if 'tuquerre' in v: return 'Tuquerreña'
    return 'Otras Variedades'

df_eva['var'] = df_eva['desagregacion_cultivo'].apply(map_var)
df_eva['departamento'] = df_eva['departamento'].astype(str).str.strip().str.title()
df_eva['municipio'] = df_eva['municipio'].astype(str).str.strip().str.title()

eva_agg = df_eva.groupby(['departamento', 'municipio', 'var', 'anio']).agg({
    'produccion_ton': 'sum',
    'area_cosechada_ha': 'sum'
}).reset_index()
eva_agg['rend'] = (eva_agg['produccion_ton'] / eva_agg['area_cosechada_ha'].replace(0, 1)).round(1)
eva_agg['produccion_ton'] = eva_agg['produccion_ton'].round(1)
eva_agg['area_cosechada_ha'] = eva_agg['area_cosechada_ha'].round(1)

records_eva = eva_agg[['departamento', 'municipio', 'var', 'anio', 'produccion_ton', 'area_cosechada_ha', 'rend']].values.tolist()

df_sipsa['var'] = df_sipsa['variedad_papa'].apply(map_var)
df_sipsa['depto'] = df_sipsa['nombre_depto'].astype(str).str.strip().str.title()

sipsa_prices = df_sipsa.groupby(['depto', 'var', 'anio']).agg({
    'precio_prom_kg': 'mean',
    'volumen_ingreso_ton': 'sum'
}).reset_index()
sipsa_prices['precio_prom_kg'] = sipsa_prices['precio_prom_kg'].round(0).astype(int)
sipsa_prices['volumen_ingreso_ton'] = sipsa_prices['volumen_ingreso_ton'].round(1)
records_sipsa = sipsa_prices[['depto', 'var', 'anio', 'precio_prom_kg', 'volumen_ingreso_ton']].values.tolist()

sipsa_monthly = df_sipsa.groupby(['depto', 'anio', 'mes']).agg({
    'precio_prom_kg': 'mean',
    'volumen_ingreso_ton': 'sum'
}).reset_index()
sipsa_monthly['precio_prom_kg'] = sipsa_monthly['precio_prom_kg'].round(0).astype(int)
sipsa_monthly['volumen_ingreso_ton'] = sipsa_monthly['volumen_ingreso_ton'].round(1)
records_monthly = sipsa_monthly[['depto', 'anio', 'mes', 'precio_prom_kg', 'volumen_ingreso_ton']].values.tolist()

data_dict = {
    'eva': records_eva,
    'sipsa': records_sipsa,
    'monthly': records_monthly
}

data_json_str = json.dumps(data_dict, ensure_ascii=False)
print(f"Data prepared successfully: {len(records_eva)} EVA rows, {len(records_sipsa)} SIPSA rows, {len(records_monthly)} Monthly rows.")
print(f"Total payload size: {len(data_json_str)/1024:.2f} KB")

# Save payload to json file for reference
with open(root / "scratch/dashboard_payload.json", "w", encoding="utf-8") as f:
    f.write(data_json_str)
