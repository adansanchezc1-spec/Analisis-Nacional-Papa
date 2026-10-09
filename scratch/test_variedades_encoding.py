import pandas as pd

df = pd.read_parquet("data/CLEANED/dataset_sipsa_mensual_nacional.parquet")
for v in df["variedad_papa"].unique():
    has_bad = any(ord(c) == 65533 for c in str(v))
    print(f"{repr(v)} -> bad_char: {has_bad} -> {[ord(c) for c in str(v)]}")
