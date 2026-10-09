import os
import pandas as pd
import numpy as np

def audit_sipsa():
    print("=" * 80)
    print("AUDITORIA: DATASET SIPSA")
    print("=" * 80)
    
    paths = [
        "data/CLEANED/dataset_sipsa_mensual_nacional.parquet",
        "data/CLEANED/dataset_sipsa_mensual_limpio.parquet",
        "data/FEATURES/dataset_sipsa_features.parquet",
        "data/POWERBI/Fact_Precios_SIPSA.parquet",
        "data/POWERBI/Fact_Abastecimiento_SIPSA.parquet"
    ]
    
    for p in paths:
        if not os.path.exists(p):
            print(f"[-] No existe: {p}")
            continue
        df = pd.read_parquet(p)
        print(f"\n[+] Archivo: {p} | Filas: {len(df):,} | Columnas: {len(df.columns)}")
        print(f"    Columnas: {list(df.columns)}")
        
        # Nulos
        nulls = df.isnull().sum()
        nulls_present = nulls[nulls > 0]
        if len(nulls_present) > 0:
            print("    [!] Columnas con NULOS:")
            for c, n in nulls_present.items():
                print(f"        - {c}: {n:,} ({n/len(df)*100:.2f}%)")
        else:
            print("    [OK] Cero nulos encontrados.")
            
        # Duplicados
        dups = df.duplicated().sum()
        if dups > 0:
            print(f"    [!] Filas exactamente duplicadas: {dups:,}")
            
        # Variables numericas
        num_cols = df.select_dtypes(include=[np.number]).columns
        for c in num_cols:
            c_min = df[c].min()
            c_max = df[c].max()
            neg_count = (df[c] < 0).sum()
            zero_count = (df[c] == 0).sum()
            print(f"    -> {c}: min={c_min}, max={c_max}, ceros={zero_count:,}, negativos={neg_count:,}")
            
        # Comprobaciones especificas
        if "precio_min_kg" in df.columns and "precio_prom_kg" in df.columns and "precio_max_kg" in df.columns:
            incoherencias = (df["precio_min_kg"] > df["precio_prom_kg"]) | (df["precio_prom_kg"] > df["precio_max_kg"])
            print(f"    [?] Incoherencias min <= prom <= max: {incoherencias.sum():,}")
            
        if "variedad_papa" in df.columns:
            top_var = df["variedad_papa"].value_counts().head(10)
            print(f"    [i] Variedades top:\n{top_var}")
            if "PAPA OTRAS VARIEDADES" in df["variedad_papa"].values:
                n_otras = (df["variedad_papa"] == "PAPA OTRAS VARIEDADES").sum()
                print(f"    [!] PAPA OTRAS VARIEDADES: {n_otras:,} ({n_otras/len(df)*100:.2f}%)")

def audit_eva():
    print("\n" + "=" * 80)
    print("AUDITORIA: DATASET EVA")
    print("=" * 80)
    
    paths = [
        "data/CLEANED/dataset_eva_agricola_nacional.parquet",
        "data/FEATURES/dataset_eva_features.parquet",
        "data/POWERBI/Fact_Produccion_EVA.parquet"
    ]
    
    for p in paths:
        if not os.path.exists(p):
            print(f"[-] No existe: {p}")
            continue
        df = pd.read_parquet(p)
        print(f"\n[+] Archivo: {p} | Filas: {len(df):,} | Columnas: {len(df.columns)}")
        print(f"    Columnas: {list(df.columns)}")
        
        nulls = df.isnull().sum()
        nulls_present = nulls[nulls > 0]
        if len(nulls_present) > 0:
            print("    [!] Columnas con NULOS:")
            for c, n in nulls_present.items():
                print(f"        - {c}: {n:,} ({n/len(df)*100:.2f}%)")
        else:
            print("    [OK] Cero nulos.")
            
        num_cols = df.select_dtypes(include=[np.number]).columns
        for c in num_cols:
            c_min = df[c].min()
            c_max = df[c].max()
            neg_count = (df[c] < 0).sum()
            zero_count = (df[c] == 0).sum()
            print(f"    -> {c}: min={c_min}, max={c_max}, ceros={zero_count:,}, negativos={neg_count:,}")

def audit_powerbi_relational():
    print("\n" + "=" * 80)
    print("AUDITORIA: INTEGRIDAD RELACIONAL POWER BI (STAR SCHEMA)")
    print("=" * 80)
    
    dim_geo = pd.read_parquet("data/POWERBI/Dim_Geografia.parquet")
    dim_tiempo = pd.read_parquet("data/POWERBI/Dim_Tiempo.parquet")
    dim_variedad = pd.read_parquet("data/POWERBI/Dim_Variedad.parquet")
    dim_mercado = pd.read_parquet("data/POWERBI/Dim_Mercado.parquet")
    
    fact_precios = pd.read_parquet("data/POWERBI/Fact_Precios_SIPSA.parquet")
    fact_abast = pd.read_parquet("data/POWERBI/Fact_Abastecimiento_SIPSA.parquet")
    fact_prod = pd.read_parquet("data/POWERBI/Fact_Produccion_EVA.parquet")
    
    print(f"Dim_Geografia llaves: {dim_geo['id_geografia'].nunique():,} / {len(dim_geo):,}")
    print(f"Dim_Tiempo llaves: {dim_tiempo['id_tiempo'].nunique():,} / {len(dim_tiempo):,}")
    print(f"Dim_Variedad llaves: {dim_variedad['id_variedad'].nunique():,} / {len(dim_variedad):,}")
    print(f"Dim_Mercado llaves: {dim_mercado['id_mercado'].nunique():,} / {len(dim_mercado):,}")
    
    # Fact_Precios integridad
    orphan_tiempo = (~fact_precios['id_tiempo'].isin(dim_tiempo['id_tiempo'])).sum()
    orphan_mercado = (~fact_precios['id_mercado'].isin(dim_mercado['id_mercado'])).sum()
    orphan_variedad = (~fact_precios['id_variedad'].isin(dim_variedad['id_variedad'])).sum()
    print(f"Fact_Precios huerfanos: Tiempo={orphan_tiempo}, Mercado={orphan_mercado}, Variedad={orphan_variedad}")
    
    # Fact_Abastecimiento integridad
    orphan_tiempo_a = (~fact_abast['id_tiempo'].isin(dim_tiempo['id_tiempo'])).sum()
    orphan_mercado_a = (~fact_abast['id_mercado'].isin(dim_mercado['id_mercado'])).sum()
    orphan_variedad_a = (~fact_abast['id_variedad'].isin(dim_variedad['id_variedad'])).sum()
    orphan_geo_a = (~fact_abast['id_geografia_origen'].isin(dim_geo['id_geografia'])).sum()
    print(f"Fact_Abast huerfanos: Tiempo={orphan_tiempo_a}, Mercado={orphan_mercado_a}, Variedad={orphan_variedad_a}, Geo={orphan_geo_a}")
    
    # Fact_Produccion integridad
    orphan_tiempo_p = (~fact_prod['id_tiempo'].isin(dim_tiempo['id_tiempo'])).sum()
    orphan_geo_p = (~fact_prod['id_geografia'].isin(dim_geo['id_geografia'])).sum()
    orphan_variedad_p = (~fact_prod['id_variedad'].isin(dim_variedad['id_variedad'])).sum()
    print(f"Fact_Prod huerfanos: Tiempo={orphan_tiempo_p}, Geo={orphan_geo_p}, Variedad={orphan_variedad_p}")

if __name__ == "__main__":
    audit_sipsa()
    audit_eva()
    audit_powerbi_relational()
