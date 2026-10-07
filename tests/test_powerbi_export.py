"""
Pruebas Unitarias para el Servicio de Modelado y Exportación a Power BI.
Verifica integridad referencial, cobertura temporal y consistencia de esquema en estrella.
"""
import pytest
import pandas as pd
from pathlib import Path

from src.infrastructure.config import DATA_DIR
from src.application.powerbi_export_service import PowerBIExportService

@pytest.fixture(scope="module")
def powerbi_tables():
    """Genera o carga las tablas exportadas para Power BI."""
    pbi_dir = DATA_DIR / "POWERBI"
    nombres = [
        "Dim_Tiempo",
        "Dim_Geografia",
        "Dim_Variedad",
        "Dim_Mercado",
        "Fact_Produccion_EVA",
        "Fact_Abastecimiento_SIPSA",
        "Fact_Precios_SIPSA"
    ]
    # Si no existen, ejecutamos el servicio
    if not all((pbi_dir / f"{n}.parquet").exists() for n in nombres):
        service = PowerBIExportService()
        service.ejecutar_exportacion()

    tablas = {n: pd.read_parquet(pbi_dir / f"{n}.parquet") for n in nombres}
    return tablas

def test_existencia_y_volumen_tablas(powerbi_tables):
    """Verifica que todas las tablas existan y tengan registros válidos."""
    assert len(powerbi_tables["Dim_Tiempo"]) == 84  # 7 años * 12 meses
    assert len(powerbi_tables["Dim_Geografia"]) > 400
    assert len(powerbi_tables["Dim_Variedad"]) == 2
    assert len(powerbi_tables["Dim_Mercado"]) >= 30
    assert len(powerbi_tables["Fact_Produccion_EVA"]) == 5574
    assert len(powerbi_tables["Fact_Abastecimiento_SIPSA"]) == 86054
    assert len(powerbi_tables["Fact_Precios_SIPSA"]) == 86054

def test_integridad_referencial_tiempo(powerbi_tables):
    """Verifica que todas las claves temporales de hechos existan en Dim_Tiempo."""
    tiempos_validos = set(powerbi_tables["Dim_Tiempo"]["id_tiempo"])
    
    assert set(powerbi_tables["Fact_Produccion_EVA"]["id_tiempo"]).issubset(tiempos_validos)
    assert set(powerbi_tables["Fact_Abastecimiento_SIPSA"]["id_tiempo"]).issubset(tiempos_validos)
    assert set(powerbi_tables["Fact_Precios_SIPSA"]["id_tiempo"]).issubset(tiempos_validos)

def test_integridad_referencial_variedad(powerbi_tables):
    """Verifica que los códigos de variedad pertenezcan a Dim_Variedad."""
    variedades_validas = set(powerbi_tables["Dim_Variedad"]["cod_variedad"])
    
    assert set(powerbi_tables["Fact_Produccion_EVA"]["cod_variedad"]).issubset(variedades_validas)
    assert set(powerbi_tables["Fact_Abastecimiento_SIPSA"]["cod_variedad"]).issubset(variedades_validas)
    assert set(powerbi_tables["Fact_Precios_SIPSA"]["cod_variedad"]).issubset(variedades_validas)

def test_integridad_referencial_mercado(powerbi_tables):
    """Verifica que los IDs de mercado en SIPSA existan en Dim_Mercado."""
    mercados_validos = set(powerbi_tables["Dim_Mercado"]["id_mercado"])
    
    assert set(powerbi_tables["Fact_Abastecimiento_SIPSA"]["id_mercado"]).issubset(mercados_validos)
    assert set(powerbi_tables["Fact_Precios_SIPSA"]["id_mercado"]).issubset(mercados_validos)

def test_no_negatividad_metricas(powerbi_tables):
    """Verifica que las medidas cuantitativas clave no tengan valores negativos espurios."""
    assert (powerbi_tables["Fact_Produccion_EVA"]["produccion_ton"] >= 0).all()
    assert (powerbi_tables["Fact_Produccion_EVA"]["area_cosechada_ha"] >= 0).all()
    assert (powerbi_tables["Fact_Precios_SIPSA"]["precio_prom_kg"] >= 0).all()
    assert (powerbi_tables["Fact_Abastecimiento_SIPSA"]["volumen_ingreso_ton"] >= 0).all()
