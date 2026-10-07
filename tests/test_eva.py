"""
Pruebas Unitarias para la Ingestión y Validación de la Base Agrícola EVA.
Verifica:
1. Ingestión y lectura correcta de registros de papa.
2. Segmentación en 'PAPA TODAS LAS VARIEDADES' y 'PAPA CRIOLLA'.
3. Cumplimiento de invariantes de producción física y consistencia DIVIPOLA.
"""

from pathlib import Path
import pytest
import pandas as pd

from src.infrastructure.config import EVA_RAW_FILE, EVA_CLEANED_PARQUET
from src.infrastructure.readers.eva_reader import EvaReader
from src.domain.entities import EvaRecord
from src.domain.invariants import validar_invariantes_eva_df


def test_eva_cleaned_parquet_exists_and_valid():
    """Verifica que el dataset canónico Parquet de EVA exista y contenga los datos esperados."""
    assert EVA_CLEANED_PARQUET.exists(), "El archivo dataset_eva_agricola_nacional.parquet no existe."
    df = pd.read_parquet(EVA_CLEANED_PARQUET)
    
    assert len(df) == 5574, f"Se esperaban 5,574 registros, se encontraron {len(df)}"
    assert set(df["desagregacion_cultivo"].unique()) == {"PAPA TODAS LAS VARIEDADES", "PAPA CRIOLLA"}
    
    # Conteo exacto verificado
    n_todas = (df["desagregacion_cultivo"] == "PAPA TODAS LAS VARIEDADES").sum()
    n_criolla = (df["desagregacion_cultivo"] == "PAPA CRIOLLA").sum()
    assert n_todas == 3869
    assert n_criolla == 1705


def test_eva_divipola_integrity():
    """Verifica que los códigos territoriales cumplan con la longitud y padding oficial DANE."""
    df = pd.read_parquet(EVA_CLEANED_PARQUET)
    
    # Códigos depto de 2 dígitos
    assert df["cod_depto"].str.len().eq(2).all(), "Existen códigos de departamento que no tienen 2 dígitos."
    # Códigos mpio de 5 dígitos
    assert df["cod_mpio"].str.len().eq(5).all(), "Existen códigos de municipio que no tienen 5 dígitos."


def test_eva_invariants_validation():
    """Verifica que las invariantes físicas se cumplan estrictamente en todos los registros."""
    df = pd.read_parquet(EVA_CLEANED_PARQUET)
    
    df_valido, invalidos = validar_invariantes_eva_df(df)
    assert invalidos == 0, f"Se detectaron {invalidos} registros con invariantes inválidas."
    assert len(df_valido) == len(df)
    
    # Valores positivos
    assert (df["produccion_ton"] >= 0).all()
    assert (df["rendimiento_ton_ha"] >= 0).all()
    assert (df["area_cosechada_ha"] >= 0).all()


def test_eva_record_entity_instantiation():
    """Verifica la instanciación de la entidad EvaRecord en el dominio."""
    record = EvaRecord(
        codigo_depto="25",
        departamento="CUNDINAMARCA",
        codigo_mpio="25899",
        municipio="ZIPAQUIRA",
        desagregacion_cultivo="PAPA TODAS LAS VARIEDADES",
        cultivo="PAPA",
        ciclo_cultivo="Transitorio",
        año=2024,
        periodo="2024A",
        area_sembrada_ha=120.5,
        area_cosechada_ha=118.0,
        produccion_ton=2360.0,
        rendimiento_ton_ha=20.0,
    )
    assert record.año == 2024
    assert record.rendimiento_ton_ha == 20.0
