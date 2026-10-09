import os
import pandas as pd
import numpy as np

def audit_raw_sipsa():
    print("=" * 80)
    print("1. AUDITORIA DE ARCHIVOS RAW SIPSA")
    print("=" * 80)
    sipsa_raw_dir = "data/RAW/sipsa"
    total_csvs = 0
    total_dtas = 0
    total_savs = 0
    for root, dirs, files in os.walk(sipsa_raw_dir):
        for f in files:
            if f.endswith(".csv"):
                total_csvs += 1
            elif f.endswith(".dta") or f.endswith(".DTA"):
                total_dtas += 1
            elif f.endswith(".sav"):
                total_savs += 1
    print(f"Archivos encontrados: {total_csvs} CSVs, {total_dtas} DTAs, {total_savs} SAVs")

def audit_sipsa_cleaned():
    print("\n" + "=" * 80)
    print("2. AUDITORIA DE SIPSA CLEANED & FEATURES")
    print("=" * 80)
    df_sipsa = pd.read_parquet("data/CLEANED/dataset_sipsa_mensual_nacional.parquet")
    print(f"Filas: {len(df_sipsa):,}")
    print("Columnas:", df_sipsa.columns.tolist())
    
    # 2.1 Fechas y Años
    print("\n[Fechas]")
    if "fecha_mes" in df_sipsa.columns:
        print(f"Min fecha: {df_sipsa['fecha_mes'].min()}, Max fecha: {df_sipsa['fecha_mes'].max()}")
    col_anio = [c for c in df_sipsa.columns if "a" in c and "o" in c][0]
    print(f"Distribucion de registros por año ({col_anio}):")
    print(df_sipsa[col_anio].value_counts().sort_index())
    
    # 2.2 Precios
    print("\n[Precios]")
    for col in ["precio_prom_kg", "precio_min_kg", "precio_max_kg"]:
        if col in df_sipsa.columns:
            s = df_sipsa[col]
            print(f"  {col}: min={s.min():.2f}, mean={s.mean():.2f}, max={s.max():.2f}, nulos={s.isna().sum()}, <=0: {(s<=0).sum()}")
            
    # Coherencia min <= prom <= max
    incoherencias = (df_sipsa["precio_min_kg"] > df_sipsa["precio_prom_kg"]) | (df_sipsa["precio_prom_kg"] > df_sipsa["precio_max_kg"])
    print(f"  Violaciones de coherencia (min <= prom <= max): {incoherencias.sum()}")
    
    # Precios extremos / sospechosos
    muy_altos = (df_sipsa["precio_prom_kg"] > 20000).sum()
    muy_bajos = (df_sipsa["precio_prom_kg"] < 300).sum()
    print(f"  Precios extremos sospechosos (> $20,000/kg): {muy_altos}")
    print(f"  Precios extremos sospechosos (< $300/kg): {muy_bajos}")
    
    # 2.3 Volumenes
    print("\n[Volúmenes]")
    if "volumen_ingreso_ton" in df_sipsa.columns:
        v = df_sipsa["volumen_ingreso_ton"]
        print(f"  volumen_ingreso_ton: min={v.min():.4f}, mean={v.mean():.2f}, max={v.max():.2f}, <=0: {(v<=0).sum()}")
        print(f"  Volumenes gigantes (> 10,000 ton/mes en una sola plaza y variedad): {(v > 10000).sum()}")
        
    # 2.4 Variedades
    print("\n[Variedades de Papa]")
    if "variedad_papa" in df_sipsa.columns:
        print(df_sipsa["variedad_papa"].value_counts())
        
    # 2.5 Plazas y Geografia
    print("\n[Geografía y Mercados]")
    print(f"  Mercados mayoristas únicos: {df_sipsa['mercado_mayorista'].nunique()}")
    print(f"  Municipios DIVIPOLA únicos: {df_sipsa['divipola_mpio'].nunique()}")
    print(f"  Departamentos DIVIPOLA únicos: {df_sipsa['divipola_depto'].nunique()}")
    
    # Códigos divipola extraños
    deptos = df_sipsa['divipola_depto'].unique()
    print("  Códigos departamentales:", sorted([str(d) for d in deptos]))

def audit_eva_data():
    print("\n" + "=" * 80)
    print("3. AUDITORIA DE DATASET EVA (AGRÍCOLA)")
    print("=" * 80)
    df_eva = pd.read_parquet("data/CLEANED/dataset_eva_agricola_nacional.parquet")
    print(f"Filas: {len(df_eva):,}")
    print("Columnas:", df_eva.columns.tolist())
    
    # Columnas con encoding corrompido
    corrupt_cols = [c for c in df_eva.columns if "\ufffd" in c or "" in c]
    print(f"  Columnas con caracteres corrompidos: {corrupt_cols}")
    
    col_anio = [c for c in df_eva.columns if "a" in c and "o" in c][0]
    print(f"\nDistribución por año ({col_anio}):")
    print(df_eva[col_anio].value_counts().sort_index())
    
    print("\nCultivos y desagregación:")
    print(df_eva["cultivo"].value_counts())
    print(df_eva["desagregacion_cultivo"].value_counts())
    
    print("\nProducción y Áreas:")
    for c in ["area_sembrada_ha", "area_cosechada_ha", "produccion_ton", "rendimiento_ton_ha"]:
        s = df_eva[c]
        print(f"  {c}: min={s.min()}, mean={s.mean():.2f}, max={s.max()}, ceros={(s==0).sum()}, negativos={(s<0).sum()}")
        
    # Incoherencias área cosechada > sembrada
    area_incoh = (df_eva["area_cosechada_ha"] > df_eva["area_sembrada_ha"]).sum()
    print(f"  Casos donde area_cosechada > area_sembrada: {area_incoh} ({area_incoh/len(df_eva)*100:.2f}%)")
    
    # Rendimiento teorico vs reportado
    mask_calc = df_eva["area_cosechada_ha"] > 0
    rend_calc = df_eva.loc[mask_calc, "produccion_ton"] / df_eva.loc[mask_calc, "area_cosechada_ha"]
    diff = np.abs(rend_calc - df_eva.loc[mask_calc, "rendimiento_ton_ha"])
    print(f"  Discrepancia entre rendimiento reportado y prod/area > 0.5 ton/ha: {(diff > 0.5).sum()}")

def audit_powerbi_anomalies():
    print("\n" + "=" * 80)
    print("4. AUDITORIA POWER BI / DIMENSIONAL")
    print("=" * 80)
    for fname in ["Dim_Geografia", "Dim_Tiempo", "Dim_Variedad", "Dim_Mercado", 
                  "Fact_Produccion_EVA", "Fact_Abastecimiento_SIPSA", "Fact_Precios_SIPSA"]:
        df = pd.read_parquet(f"data/POWERBI/{fname}.parquet")
        # Check corrupt chars in columns
        bad_cols = [c for c in df.columns if "\ufffd" in c]
        # Check string columns for corrupt chars
        str_bad = 0
        for c in df.select_dtypes(include=["object"]).columns:
            str_bad += df[c].astype(str).str.contains("\ufffd").sum()
        print(f"{fname:26s} | Filas: {len(df):7,} | Bad cols: {bad_cols} | Celdas con corrupcion: {str_bad:,}")

if __name__ == "__main__":
    audit_raw_sipsa()
    audit_sipsa_cleaned()
    audit_eva_data()
    audit_powerbi_anomalies()
