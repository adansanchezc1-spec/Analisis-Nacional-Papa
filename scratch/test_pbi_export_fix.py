import pandas as pd
import numpy as np

df_sipsa = pd.read_parquet("data/CLEANED/dataset_sipsa_mensual_nacional.parquet")
df_sipsa["fecha"] = pd.to_datetime(df_sipsa["fecha_mes"])
df_sipsa["id_tiempo"] = df_sipsa["fecha"].dt.strftime("%Y%m%d").astype(int)
df_sipsa["cod_mpio"] = df_sipsa["divipola_mpio"].astype(str).str.zfill(5)
df_sipsa["cod_variedad"] = np.where(
    df_sipsa["variedad_papa"].str.lower().str.contains("criolla"),
    "CRIOLLA",
    "PASTUSA_SUPREMA"
)

cols_abast = [
    "id_tiempo",
    "mercado_mayorista",
    "cod_mpio",
    "cod_variedad",
    "variedad_papa",
    "volumen_ingreso_ton",
]
print("Duplicados con mpio y variedad:", df_sipsa[cols_abast].duplicated().sum())
