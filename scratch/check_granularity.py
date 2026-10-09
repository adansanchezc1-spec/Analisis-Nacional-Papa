import pandas as pd

def check_fact_duplicates():
    fact_precios = pd.read_parquet("data/POWERBI/Fact_Precios_SIPSA.parquet")
    fact_abast = pd.read_parquet("data/POWERBI/Fact_Abastecimiento_SIPSA.parquet")
    
    print("--- GRANULARIDAD FACT_PRECIOS ---")
    print(f"Total filas: {len(fact_precios):,}")
    print(f"Combinaciones unicas (id_tiempo, id_mercado, cod_variedad): {fact_precios[['id_tiempo', 'id_mercado', 'cod_variedad']].drop_duplicates().shape[0]:,}")
    
    print("\n--- GRANULARIDAD FACT_ABASTECIMIENTO ---")
    print(f"Total filas: {len(fact_abast):,}")
    print(f"Combinaciones unicas (id_tiempo, id_mercado, cod_variedad): {fact_abast[['id_tiempo', 'id_mercado', 'cod_variedad']].drop_duplicates().shape[0]:,}")
    
    print("\n--- DISTRIBUCION DE cod_variedad EN FACT_PRECIOS ---")
    print(fact_precios['cod_variedad'].value_counts())

def check_dim_geografia():
    dim_geo = pd.read_parquet("data/POWERBI/Dim_Geografia.parquet")
    print("\n--- DIM_GEOGRAFIA ---")
    print(f"Total filas: {len(dim_geo):,}")
    print(f"cod_mpio unicos: {dim_geo['cod_mpio'].nunique():,}")
    dups_mpio = dim_geo[dim_geo['cod_mpio'].duplicated(keep=False)]
    if len(dups_mpio) > 0:
        print(f"cod_mpio duplicados en Dim_Geografia:\n{dups_mpio.head(10)}")
        
def check_dim_mercado():
    dim_mercado = pd.read_parquet("data/POWERBI/Dim_Mercado.parquet")
    print("\n--- DIM_MERCADO ---")
    print(f"Total filas: {len(dim_mercado):,}")
    print(f"id_mercado unicos: {dim_mercado['id_mercado'].nunique():,}")

if __name__ == "__main__":
    check_fact_duplicates()
    check_dim_geografia()
    check_dim_mercado()
