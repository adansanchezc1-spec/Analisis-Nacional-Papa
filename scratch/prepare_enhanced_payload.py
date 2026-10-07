import pandas as pd
import numpy as np
import json
from collections import defaultdict
from pathlib import Path

root = Path(r"c:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando")
eva_path = root / "data/CLEANED/dataset_eva_agricola_nacional.parquet"
sipsa_path = root / "data/CLEANED/dataset_sipsa_mensual_nacional.parquet"

df_eva = pd.read_parquet(eva_path)
df_sipsa = pd.read_parquet(sipsa_path)

col_a_eva = [c for c in df_eva.columns if 'a' in c.lower() and 'o' in c.lower() and len(c) <= 4][0]
df_eva = df_eva.rename(columns={col_a_eva: 'anio'})
col_a_sipsa = [c for c in df_sipsa.columns if 'a' in c.lower() and 'o' in c.lower() and len(c) <= 4][0]
df_sipsa = df_sipsa.rename(columns={col_a_sipsa: 'anio'})

def clean_var_name(v):
    v = str(v).strip().upper()
    if 'CRIOLLA' in v: return 'Papa Criolla'
    if 'SUPERIOR' in v: return 'Papa Superior'
    if 'UNICA' in v or 'ÚNICA' in v or 'NICA' in v: return 'Papa Única'
    if 'CAPIRA' in v or 'CAPIRO' in v: return 'Papa Diacol Capiro'
    if 'PASTUSA' in v: return 'Papa Parda Pastusa'
    if 'SUPREMA' in v: return 'Papa Suprema'
    if 'R-12' in v or 'R12' in v: return 'Papa R-12'
    if 'BETINA' in v: return 'Papa Betina'
    if 'RUBI' in v or 'RUBÍ' in v or 'RUB' in v: return 'Papa Rubí'
    if 'NEVADA' in v: return 'Papa Nevada'
    if 'SABANERA' in v: return 'Papa Sabanera'
    if 'MORASURCO' in v: return 'Papa Morasurco'
    return 'Otras Variedades'

df_sipsa['var_clean'] = df_sipsa['variedad_papa'].apply(clean_var_name)
df_sipsa['depto_clean'] = df_sipsa['nombre_depto'].astype(str).str.strip().str.title()

df_eva['depto_clean'] = df_eva['departamento'].astype(str).str.strip().str.title()
df_eva['mpio_clean'] = df_eva['municipio'].astype(str).str.strip().str.title()

pheno_days = {
    'Papa Criolla': 110,
    'Papa Superior': 165,
    'Papa Única': 150,
    'Papa Diacol Capiro': 165,
    'Papa Parda Pastusa': 170,
    'Papa Suprema': 160,
    'Papa R-12': 165,
    'Papa Betina': 160,
    'Papa Rubí': 160,
    'Papa Nevada': 170,
    'Papa Sabanera': 170,
    'Papa Morasurco': 160,
    'Otras Variedades': 165
}

# Regional market variety proportions from SIPSA
sipsa_non_criolla = df_sipsa[df_sipsa['var_clean'] != 'Papa Criolla']
depto_var_vols = sipsa_non_criolla.groupby(['depto_clean', 'var_clean'])['volumen_ingreso_ton'].sum()
depto_tot_vols = sipsa_non_criolla.groupby('depto_clean')['volumen_ingreso_ton'].sum()
depto_var_weights = (depto_var_vols / depto_tot_vols).fillna(0).to_dict()

nat_var_vols = sipsa_non_criolla.groupby('var_clean')['volumen_ingreso_ton'].sum()
nat_tot_vol = sipsa_non_criolla['volumen_ingreso_ton'].sum()
nat_var_weights = (nat_var_vols / nat_tot_vol).to_dict()

# Distribute EVA records
agg_eva = defaultdict(lambda: [0.0, 0.0, 0.0])
for _, row in df_eva.iterrows():
    d = row['depto_clean']
    m = row['mpio_clean']
    a = int(row['anio'])
    prod = float(row['produccion_ton'])
    area_s = float(row['area_sembrada_ha'])
    area_c = float(row['area_cosechada_ha'])
    desc = str(row['desagregacion_cultivo']).upper()

    if 'CRIOLLA' in desc:
        key = (d, m, 'Papa Criolla', a, 110)
        agg_eva[key][0] += area_s
        agg_eva[key][1] += area_c
        agg_eva[key][2] += prod
    else:
        sub_weights = {v: depto_var_weights.get((d, v), 0) for v in nat_var_weights.keys()}
        if sum(sub_weights.values()) <= 0:
            sub_weights = nat_var_weights
        
        top_vars = sorted(sub_weights.items(), key=lambda x: x[1], reverse=True)[:3]
        tot_top_w = sum(w for _, w in top_vars)
        if tot_top_w <= 0: tot_top_w = 1.0

        for v_name, w in top_vars:
            norm_w = w / tot_top_w
            key = (d, m, v_name, a, pheno_days.get(v_name, 165))
            agg_eva[key][0] += area_s * norm_w
            agg_eva[key][1] += area_c * norm_w
            agg_eva[key][2] += prod * norm_w

# Compile final EVA records: [depto, mpio, var, anio, areas, areac, efect, prod, rend, pheno]
final_eva = []
for (d, m, v, a, pheno), (as_, ac_, pr_) in agg_eva.items():
    if pr_ > 0 or ac_ > 0:
        efect = round((ac_ / as_) * 100, 1) if as_ > 0 else 100.0
        rend = round(pr_ / ac_, 1) if ac_ > 0 else 0.0
        final_eva.append([d, m, v, a, round(as_, 1), round(ac_, 1), efect, round(pr_, 1), rend, pheno])

# SIPSA prices and volumes by depto, variedad, anio
sipsa_prices = df_sipsa.groupby(['depto_clean', 'var_clean', 'anio']).agg({
    'precio_prom_kg': 'mean',
    'volumen_ingreso_ton': 'sum'
}).reset_index()
sipsa_prices['precio_prom_kg'] = sipsa_prices['precio_prom_kg'].round(0).astype(int)
sipsa_prices['volumen_ingreso_ton'] = sipsa_prices['volumen_ingreso_ton'].round(1)
records_sipsa = sipsa_prices[['depto_clean', 'var_clean', 'anio', 'precio_prom_kg', 'volumen_ingreso_ton']].values.tolist()

# Monthly timeline by variedad, anio, mes
sipsa_monthly = df_sipsa.groupby(['var_clean', 'anio', 'mes']).agg({
    'precio_prom_kg': 'mean',
    'volumen_ingreso_ton': 'sum'
}).reset_index()
sipsa_monthly['precio_prom_kg'] = sipsa_monthly['precio_prom_kg'].round(0).astype(int)
sipsa_monthly['volumen_ingreso_ton'] = sipsa_monthly['volumen_ingreso_ton'].round(1)
records_monthly = sipsa_monthly[['var_clean', 'anio', 'mes', 'precio_prom_kg', 'volumen_ingreso_ton']].values.tolist()

payload = {
    'eva': final_eva,
    'sipsa': records_sipsa,
    'monthly': records_monthly,
    'pheno_meta': pheno_days
}

dump_str = json.dumps(payload, ensure_ascii=False)
out_file = root / "scratch/dashboard_enhanced_payload.json"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(dump_str)

print(f"Aggregated payload saved to {out_file}: {len(final_eva):,} EVA rows, {len(records_sipsa):,} SIPSA rows, {len(records_monthly):,} Monthly rows.")
print(f"Total payload size: {len(dump_str)/1024:.2f} KB")
