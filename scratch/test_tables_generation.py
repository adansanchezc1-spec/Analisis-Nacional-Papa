import pandas as pd
import numpy as np

df_eva = pd.read_parquet('data/CLEANED/dataset_eva_agricola_nacional.parquet')
col_a = [c for c in df_eva.columns if 'a' in c.lower() and 'o' in c.lower() and len(c) <= 4][0]
df_eva = df_eva.rename(columns={col_a: 'anio'})

# -------------------------------------------------------------
# TABLA 1: SIEMBRA VS COSECHA Y FENOLOGÍA
# -------------------------------------------------------------
t1 = df_eva.groupby('anio').agg({
    'area_sembrada_ha': 'sum',
    'area_cosechada_ha': 'sum'
}).reset_index()
t1['perdida_ha'] = t1['area_sembrada_ha'] - t1['area_cosechada_ha']
t1['efectividad_pct'] = (t1['area_cosechada_ha'] / t1['area_sembrada_ha']) * 100.0

t1['var_sembrada_ha'] = t1['area_sembrada_ha'].diff()
t1['var_sembrada_pct'] = t1['area_sembrada_ha'].pct_change() * 100.0
t1['var_cosechada_ha'] = t1['area_cosechada_ha'].diff()
t1['var_cosechada_pct'] = t1['area_cosechada_ha'].pct_change() * 100.0
t1['var_perdida_ha'] = t1['perdida_ha'].diff()
t1['var_efectividad_pp'] = t1['efectividad_pct'].diff()

regimenes_t1 = [
    'Línea base pre-pandemia; régimen bimodal regular',
    'Expansión de siembras (+6.6%); inicio choque logístico',
    'Contracción de área (-5.8%); paro nacional y lluvias',
    'Crisis global de insumos; urea y fertilizantes récord',
    'Fenómeno de El Niño severo; merma récord (17,102 ha)',
    'Recuperación gradual de efectividad (+2.0 p.p.)',
    'Normalización agroclimática; consolidación UPRA'
]

# Total row
tot_sembrada = t1['area_sembrada_ha'].sum()
tot_cosechada = t1['area_cosechada_ha'].sum()
tot_perdida = t1['perdida_ha'].sum()
tot_efectividad = (tot_cosechada / tot_sembrada) * 100.0

print(f"Total sembrada: {tot_sembrada:,.0f} ha")
print(f"Total cosechada: {tot_cosechada:,.0f} ha")
print(f"Total perdida: {tot_perdida:,.0f} ha ({tot_efectividad:.2f}%)")

# -------------------------------------------------------------
# TABLA 2: PRODUCCIÓN, ÁREA COSECHADA Y RENDIMIENTO
# -------------------------------------------------------------
t2 = df_eva.groupby('anio').agg({
    'produccion_ton': 'sum',
    'area_cosechada_ha': 'sum',
    'rendimiento_ton_ha': 'mean'
}).reset_index()

t2['var_prod_ton'] = t2['produccion_ton'].diff()
t2['var_prod_pct'] = t2['produccion_ton'].pct_change() * 100.0
t2['var_area_ha'] = t2['area_cosechada_ha'].diff()
t2['var_area_pct'] = t2['area_cosechada_ha'].pct_change() * 100.0
t2['var_rend_tha'] = t2['rendimiento_ton_ha'].diff()
t2['var_rend_pct'] = t2['rendimiento_ton_ha'].pct_change() * 100.0
t2['prod_base2019_pct'] = ((t2['produccion_ton'] / t2['produccion_ton'].iloc[0]) - 1.0) * 100.0

diagnosticos_t2 = [
    'Pico de oferta; abastecimiento pleno nacional',
    'Estabilidad de volumen; leve contracción de rto.',
    'Caída de producción (-7.4%); bloqueos y costos',
    'Valle de cosecha por encarecimiento de fertilizantes',
    'Estrés hídrico en tuberización; recuperación parcial',
    'Repunte productivo (+6.5%); expansión en Cundinamarca',
    'Cosecha récord plurianual (+15.6%); alta productividad'
]

tot_prod = t2['produccion_ton'].sum()
tot_area2 = t2['area_cosechada_ha'].sum()
mean_rend = t2['rendimiento_ton_ha'].mean()

print(f"Total producción: {tot_prod:,.0f} ton")
print(f"Rendimiento medio plurianual: {mean_rend:.2f} t/ha")
