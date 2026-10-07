"""
Pruebas Unitarias para el Módulo de EDA (EdaService).
Verifica cálculos de tendencia central, dispersión, asimetría, curtosis y correlación.
"""

import pytest
import numpy as np
import pandas as pd

from src.application.eda_service import EdaService


@pytest.fixture
def sample_market_df():
    """Genera un DataFrame sintético para pruebas de EDA."""
    np.random.seed(42)
    n = 100
    precios = np.random.normal(loc=2000, scale=200, size=n)
    volumenes = np.random.uniform(low=10, high=100, size=n)
    return pd.DataFrame({
        "precio_prom_kg": precios,
        "volumen_ingreso_ton": volumenes,
        "año": [2022] * 50 + [2023] * 50,
        "mes": list(range(1, 13)) * 8 + [1, 2, 3, 4],
        "variedad_papa": ["PAPA PASTUSA"] * 50 + ["PAPA CAPIRO"] * 50
    })


def test_calcular_medidas_resumen(sample_market_df):
    eda = EdaService(sample_market_df)
    res = eda.calcular_medidas_resumen(columna="precio_prom_kg")

    assert res["n_observaciones"] == 100
    assert 1800 < res["media"] < 2200
    assert 1800 < res["mediana"] < 2200
    assert res["desviacion_estandar"] > 0
    assert res["iqr"] > 0
    assert res["mad"] > 0
    assert "asimetria_skewness" in res
    assert "curtosis_pearson" in res
    assert res["asimetria_al_cuadrado"] >= 0


def test_calcular_coordenadas_cullen_frey(sample_market_df):
    eda = EdaService(sample_market_df)
    coords = eda.calcular_coordenadas_cullen_frey(columna="precio_prom_kg", n_bootstraps=50)

    assert "skewness_observado" in coords
    assert "skewness_sq_observado" in coords
    assert "kurtosis_observado" in coords
    assert len(coords["bootstrap_skewness_sq"]) == 50
    assert len(coords["bootstrap_kurtosis"]) == 50


def test_calcular_matrices_correlacion(sample_market_df):
    eda = EdaService(sample_market_df)
    corr_p, corr_s = eda.calcular_matrices_correlacion(columnas=["precio_prom_kg", "volumen_ingreso_ton"])

    # Diagonal debe ser 1.0
    assert np.isclose(corr_p.loc["precio_prom_kg", "precio_prom_kg"], 1.0)
    assert np.isclose(corr_s.loc["precio_prom_kg", "precio_prom_kg"], 1.0)

    # Valores en rango [-1, 1]
    assert -1.0 <= corr_p.loc["precio_prom_kg", "volumen_ingreso_ton"] <= 1.0
    assert -1.0 <= corr_s.loc["precio_prom_kg", "volumen_ingreso_ton"] <= 1.0
