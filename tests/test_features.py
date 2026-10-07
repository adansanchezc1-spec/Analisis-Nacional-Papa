"""
Pruebas Unitarias para el Servicio de Features y Acople Demográfico.
Verifica cálculo de consumo per cápita, índices estacionales y etiquetado de anomalías.
"""

import pandas as pd
import numpy as np

from src.application.features_service import FeaturesService


def test_acoplar_demografia_y_per_capita():
    df = pd.DataFrame({
        "año": [2022, 2023],
        "volumen_ingreso_ton": [391.30235, 395.07801],  # Toneladas
        "precio_prom_kg": [2000.0, 2500.0],
        "variedad_papa": ["PAPA PASTUSA", "PAPA PASTUSA"]
    })

    feat_service = FeaturesService(df)
    df_res = feat_service.acoplar_demografia_y_per_capita()

    # En 2022 cabecera es 39,130,235. 391.30235 ton * 1000 / 39130235 = 0.01 kg/hab
    assert np.isclose(df_res.loc[0, "consumo_mayorista_per_capita_kg"], 0.01)
    assert "poblacion_nacional_cabecera" in df_res.columns


def test_calcular_indices_estacionales():
    df = pd.DataFrame({
        "año": [2023, 2023],
        "mes": [1, 2],
        "precio_prom_kg": [1500.0, 2500.0],  # Promedio anual = 2000.0
        "volumen_ingreso_ton": [100.0, 100.0],
        "variedad_papa": ["PAPA CAPIRO", "PAPA CAPIRO"]
    })

    feat_service = FeaturesService(df)
    df_res = feat_service.calcular_indices_estacionales()

    # IEP mes 1 = 1500 / 2000 * 100 = 75.0
    # IEP mes 2 = 2500 / 2000 * 100 = 125.0
    assert np.isclose(df_res.loc[0, "indice_estacional_precio_iep"], 75.0)
    assert np.isclose(df_res.loc[1, "indice_estacional_precio_iep"], 125.0)


def test_etiquetar_anomalias():
    # 20 observaciones con un outlier extremo
    precios = [2000.0] * 19 + [15000.0]
    df = pd.DataFrame({
        "año": [2023] * 20,
        "variedad_papa": ["PAPA PASTUSA"] * 20,
        "precio_prom_kg": precios
    })

    feat_service = FeaturesService(df)
    df_res = feat_service.etiquetar_anomalias()

    assert "es_outlier_iqr" in df_res.columns
    assert df_res.loc[19, "es_outlier_iqr"] == True
    assert df_res.loc[0, "es_outlier_iqr"] == False
