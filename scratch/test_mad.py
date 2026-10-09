import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_parquet("data/FEATURES/dataset_sipsa_features.parquet")
max_z_list = []
for (año, var), grupo in df.groupby(["año", "variedad_papa"]):
    precios = grupo["precio_prom_kg"].values
    if len(precios) < 5:
        continue
    mediana = np.median(precios)
    mad = stats.median_abs_deviation(precios)
    if mad > 0:
        mod_z = np.abs(precios - mediana) / (1.4826 * mad)
        max_z_list.append(mod_z.max())
print(f"Max modified z-score across all groups: {max(max_z_list) if max_z_list else 0:.4f}")
