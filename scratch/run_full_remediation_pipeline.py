import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import pandas as pd

from src.infrastructure.config import (
    SIPSA_CLEANED_PARQUET,
    EVA_CLEANED_PARQUET,
    EVA_RAW_FILE,
    CLEANED_DIR,
    FEATURES_DIR,
    DATA_DIR
)
from src.application.cleaning_service import CleaningService
from src.infrastructure.readers.eva_reader import EvaReader
from src.infrastructure.writers.parquet_writer import ParquetWriter
from src.application.features_service import FeaturesService
from src.application.powerbi_export_service import PowerBIExportService

def run():
    print("=" * 80)
    print("EJECUTANDO PIPELINE DE REMEDIACIÓN Y GOBERNANZA DAMA-BOK")
    print("=" * 80)
    
    # 1. Limpieza de SIPSA
    print("\n[Paso 1/5] Ejecutando CleaningService con catálogo expandido de 12 variedades...")
    df_sipsa_nacional = pd.read_parquet(SIPSA_CLEANED_PARQUET)
    cleaner = CleaningService(df_sipsa_nacional)
    df_sipsa_limpio = cleaner.ejecutar_limpieza()
    preview_sipsa_csv = CLEANED_DIR / "dataset_sipsa_mensual_limpio_preview.csv"
    df_sipsa_limpio.head(100).to_csv(preview_sipsa_csv, index=False, encoding="utf-8-sig")
    print(f" -> Guardado: {CLEANED_DIR / 'dataset_sipsa_mensual_limpio.parquet'} ({len(df_sipsa_limpio):,} filas)")
    print(f" -> Distribución de variedades:\n{df_sipsa_limpio['variedad_papa'].value_counts()}")
    
    # 2. Re-ingestión de EVA con sanitización de texto
    print("\n[Paso 2/5] Re-ingestión de EVA con sanitización de texto...")
    eva_reader = EvaReader()
    df_eva_limpio = eva_reader.read_eva_papa(EVA_RAW_FILE)
    ParquetWriter.write(df_eva_limpio, EVA_CLEANED_PARQUET)
    preview_eva_csv = CLEANED_DIR / "dataset_eva_agricola_nacional_preview.csv"
    df_eva_limpio.head(100).to_csv(preview_eva_csv, index=False, encoding="utf-8-sig")
    print(f" -> Guardado: {EVA_CLEANED_PARQUET} ({len(df_eva_limpio):,} filas)")
    
    # 3. Features SIPSA con MAD calibrado
    print("\n[Paso 3/5] Generación de Features SIPSA con detección MAD calibrada...")
    feat_sipsa = FeaturesService(df_sipsa_limpio)
    df_sipsa_feat = feat_sipsa.construir_panel_completo_features()
    print(f" -> Guardado: {FEATURES_DIR / 'dataset_sipsa_features.parquet'} ({len(df_sipsa_feat):,} filas)")
    print(f" -> Outliers IQR: {df_sipsa_feat['es_outlier_iqr'].sum():,} | Outliers MAD: {df_sipsa_feat['es_outlier_mad'].sum():,}")
    
    # 4. Features EVA
    print("\n[Paso 4/5] Enriquecimiento demográfico de EVA...")
    df_eva_feat = FeaturesService.acoplar_eva_con_demografia(df_eva_limpio)
    print(f" -> Guardado: {FEATURES_DIR / 'dataset_eva_features.parquet'} ({len(df_eva_feat):,} filas)")
    
    # 5. Exportación a Power BI
    print("\n[Paso 5/5] Re-exportación dimensional Star Schema Power BI...")
    pbi_exporter = PowerBIExportService()
    res_pbi = pbi_exporter.ejecutar_exportacion()
    print(" -> Tablas exportadas con éxito:")
    for tabla, n_filas in res_pbi.items():
        print(f"    - {tabla:26s}: {n_filas:7,} filas")

if __name__ == "__main__":
    run()
