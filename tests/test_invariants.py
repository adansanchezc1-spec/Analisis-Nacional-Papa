"""
Pruebas Unitarias para Invariantes de Negocio del Mercado.
Verifica la regla estricta: Ningún precio nulo o <= 0, y relaciones de orden físico.
"""

import pytest
import numpy as np
import pandas as pd

from src.domain.exceptions import PriceNullViolationError, PhysicalRangeViolationError
from src.domain.invariants import (
    validar_precio_escalar,
    validar_coherencia_precios_escalar,
    filtrar_y_auditar_precios_df,
)


def test_validar_precio_escalar_exitoso():
    assert validar_precio_escalar(1500.0) is True
    assert validar_precio_escalar(0.01) is True


def test_validar_precio_escalar_falla_con_nulo_o_cero():
    with pytest.raises(PriceNullViolationError):
        validar_precio_escalar(None)

    with pytest.raises(PriceNullViolationError):
        validar_precio_escalar(np.nan)

    with pytest.raises(PriceNullViolationError):
        validar_precio_escalar(0.0)

    with pytest.raises(PriceNullViolationError):
        validar_precio_escalar(-500.0)


def test_validar_coherencia_precios_escalar_exitoso():
    assert validar_coherencia_precios_escalar(1000.0, 1500.0, 2000.0) is True
    assert validar_coherencia_precios_escalar(1000.0, 1000.0, 1000.0) is True


def test_validar_coherencia_precios_escalar_falla_orden():
    with pytest.raises(PhysicalRangeViolationError):
        # min > prom
        validar_coherencia_precios_escalar(2000.0, 1500.0, 2500.0)

    with pytest.raises(PhysicalRangeViolationError):
        # prom > max
        validar_coherencia_precios_escalar(1000.0, 3000.0, 2500.0)


def test_filtrar_y_auditar_precios_df():
    data = {
        "producto": ["PAPA", "PAPA", "PAPA", "PAPA", "PAPA"],
        "precio_prom_kg": [1200.0, np.nan, 1800.0, 0.0, -100.0]
    }
    df = pd.DataFrame(data)

    df_limpio, n_descartes = filtrar_y_auditar_precios_df(df, col_precio="precio_prom_kg")

    assert len(df_limpio) == 2
    assert n_descartes == 3
    assert df_limpio["precio_prom_kg"].tolist() == [1200.0, 1800.0]
    assert df_limpio["precio_prom_kg"].isna().sum() == 0
