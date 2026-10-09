import pandas as pd

df = pd.read_parquet("data/CLEANED/dataset_sipsa_mensual_nacional.parquet")
for col in df.columns:
    print(f"Columna: {repr(col)} -> codepoints: {[ord(c) for c in col]}")
