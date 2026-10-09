import os
import pandas as pd
import numpy as np

def inspect_powerbi_tables():
    print("--- TABLAS DE POWER BI ---")
    for f in os.listdir("data/POWERBI"):
        if f.endswith(".parquet"):
            df = pd.read_parquet(os.path.join("data/POWERBI", f))
            print(f"\n[+] {f}: {len(df):,} filas | Columnas: {list(df.columns)}")
            print("Primeras 2 filas:")
            print(df.head(2).to_dict(orient="records"))

def inspect_raw_sipsa_varieties():
    print("\n--- VARIEDADES EN CLEANED / RAW ---")
    df_clean = pd.read_parquet("data/CLEANED/dataset_sipsa_mensual_limpio.parquet")
    print("Columnas de sipsa mensual limpio:", df_clean.columns.tolist())
    if "variedad_papa_original" in df_clean.columns:
        print("\nTop 20 variedad_papa_original que terminaron en 'PAPA OTRAS VARIEDADES':")
        otras = df_clean[df_clean["variedad_papa"] == "PAPA OTRAS VARIEDADES"]
        print(otras["variedad_papa_original"].value_counts().head(25))

def inspect_eva_columns_and_encoding():
    print("\n--- ENCODING / COLUMNAS EN EVA ---")
    df_eva = pd.read_parquet("data/CLEANED/dataset_eva_agricola_nacional.parquet")
    print("Columnas EVA:", df_eva.columns.tolist())
    for col in df_eva.columns:
        if "" in col:
            print(f"[!] Columna con caracter corrompido: {repr(col)}")

if __name__ == "__main__":
    inspect_powerbi_tables()
    inspect_raw_sipsa_varieties()
    inspect_eva_columns_and_encoding()
