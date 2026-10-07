"""
Pruebas Unitarias para Validación Territorial DIVIPOLA DANE.
Verifica normalización de ceros a la izquierda (zfill) y longitudes obligatorias.
"""

import pandas as pd
from src.domain.divipola import (
    normalizar_codigo_depto,
    normalizar_codigo_mpio,
    validar_serie_divipola,
)


def test_normalizar_codigo_depto():
    # Pérdida común de ceros en Excel
    assert normalizar_codigo_depto(5) == "05"
    assert normalizar_codigo_depto("5") == "05"
    assert normalizar_codigo_depto("5.0") == "05"
    assert normalizar_codigo_depto(25) == "25"
    assert normalizar_codigo_depto("11") == "11"
    assert normalizar_codigo_depto(None) is None
    assert normalizar_codigo_depto("abc") is None


def test_normalizar_codigo_mpio():
    # Ejemplos emblemáticos de papas (La Unión Antioquia 05400, Túquerres 52838, Villapinzón 25875)
    assert normalizar_codigo_mpio(5400) == "05400"
    assert normalizar_codigo_mpio("5400") == "05400"
    assert normalizar_codigo_mpio("5400.0") == "05400"
    assert normalizar_codigo_mpio("52838") == "52838"
    assert normalizar_codigo_mpio(25875) == "25875"
    assert normalizar_codigo_mpio("11001") == "11001"
    assert normalizar_codigo_mpio(None) is None


def test_validar_serie_divipola():
    serie_mpios = pd.Series([5400, "52838", "25875.0", None, "texto"])
    serie_norm = validar_serie_divipola(serie_mpios, longitud=5)

    assert serie_norm.tolist() == ["05400", "52838", "25875", None, None]
