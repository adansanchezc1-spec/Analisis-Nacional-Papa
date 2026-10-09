import pandas as pd

df = pd.read_parquet("data/FEATURES/dataset_sipsa_features.parquet")
print(f"Total filas: {len(df):,}")
print(f"es_outlier_iqr: {df['es_outlier_iqr'].sum():,} ({df['es_outlier_iqr'].mean()*100:.2f}%)")
print(f"es_outlier_mad: {df['es_outlier_mad'].sum():,} ({df['es_outlier_mad'].mean()*100:.2f}%)")

print("\nOutliers detectados por año:")
print(df.groupby("año")[["es_outlier_iqr", "es_outlier_mad"]].sum())
