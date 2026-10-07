"""
Pruebas Unitarias para el Servicio de Inferencia Estadística Dual (ModelService).
Verifica cálculos paramétricos (ANOVA, Welch, Levene) y no paramétricos (Kruskal, Bootstrap BCa).
"""

import numpy as np
import pandas as pd
import pytest

from src.application.model_service import ModelService


@pytest.fixture
def multi_group_df():
    np.random.seed(42)
    # Grupo A: media 2000, Grupo B: media 3000
    g_a = np.random.normal(2000, 200, size=30)
    g_b = np.random.normal(3000, 300, size=30)
    return pd.DataFrame({
        "grupo": ["A"] * 30 + ["B"] * 30,
        "precio_prom_kg": np.concatenate([g_a, g_b])
    })


def test_ejecutar_canal_parametrico(multi_group_df):
    mod = ModelService(multi_group_df)
    res = mod.ejecutar_canal_parametrico(col_grupo="grupo", col_valor="precio_prom_kg")

    assert "prueba_levene" in res
    assert "anova_clasico" in res
    assert "anova_welch" in res
    assert res["anova_clasico"]["diferencia_significativa"] is True
    assert res["anova_clasico"]["p_valor"] < 0.001


def test_calcular_bootstrap_bca_intervalo():
    np.random.seed(42)
    datos = np.random.normal(1500, 100, size=50)
    mod = ModelService(pd.DataFrame({"precio_prom_kg": datos}))

    ic_inf, ic_sup = mod.calcular_bootstrap_bca_intervalo(datos, B=500)

    assert ic_inf < 1500 < ic_sup
    assert ic_inf < ic_sup


def test_ejecutar_canal_no_parametrico(multi_group_df):
    mod = ModelService(multi_group_df)
    res = mod.ejecutar_canal_no_parametrico(col_grupo="grupo", col_valor="precio_prom_kg", B_bootstrap=200)

    assert "kruskal_wallis" in res
    assert res["kruskal_wallis"]["diferencia_significativa"] is True
    assert res["kruskal_wallis"]["p_valor"] < 0.001
    assert "intervalos_bootstrap_bca_95" in res
    assert "A" in res["intervalos_bootstrap_bca_95"]
    assert "B" in res["intervalos_bootstrap_bca_95"]
