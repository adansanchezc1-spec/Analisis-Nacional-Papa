import numpy as np
import pandas as pd
from scipy import stats

precios = [2000.0] * 19 + [15000.0]
mediana = np.median(precios)
mad = stats.median_abs_deviation(precios)
mod_z = np.abs(precios - mediana) / (1.4826 * mad) if mad > 0 else 0
print(f"Test case mod_z for 15000: {mod_z[-1] if hasattr(mod_z, '__getitem__') else mod_z}")

df = pd.read_parquet("data/FEATURES/dataset_sipsa_features.parquet")
outliers_30 = 0
outliers_35 = 0
for (año, var), grupo in df.groupby(["año", "variedad_papa"]):
    p = grupo["precio_prom_kg"].values
    if len(p) < 5: continue
    med = np.median(p)
    m = stats.median_abs_deviation(p)
    if m > 0:
        mz = np.abs(p - med) / (1.4826 * m)
        outliers_30 += (mz > 3.0).sum()
        outliers_35 += (mz > 3.5).sum()
print(f"En dataset completo: outliers con umbral 3.0: {outliers_30:,} | con umbral 3.5: {outliers_35:,}")
