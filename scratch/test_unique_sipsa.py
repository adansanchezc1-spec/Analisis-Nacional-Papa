import pandas as pd

df_sipsa = pd.read_parquet("data/CLEANED/dataset_sipsa_mensual_nacional.parquet")
print(f"Total filas: {len(df_sipsa):,}")

# Combinaciones con mercado, divipola_mpio, variedad
comb1 = df_sipsa[['fecha_mes', 'mercado_mayorista', 'divipola_mpio', 'variedad_papa']].drop_duplicates()
print(f"Combinaciones unicas con variedad cruda: {len(comb1):,}")

# Mapear variedad a criolla vs pastusa_suprema
v_bin = df_sipsa['variedad_papa'].str.lower().str.contains("criolla").map({True: 'CRIOLLA', False: 'PASTUSA_SUPREMA'})
comb2 = pd.DataFrame({
    'fecha': df_sipsa['fecha_mes'],
    'mercado': df_sipsa['mercado_mayorista'],
    'mpio': df_sipsa['divipola_mpio'],
    'var': v_bin
}).drop_duplicates()
print(f"Combinaciones unicas con variedad binaria y mpio: {len(comb2):,}")
