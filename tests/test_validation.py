"""
Pruebas Unitarias para el Servicio de Validación DAMA-BOK.
Verifica cumplimiento de invariantes de negocio, reporte DAMA-BOK y validación DIVIPOLA.
"""

import pandas as pd
import numpy as np

from src.application.validation_service import ValidationService


def test_ejecutar_auditoria_completa_con_datos_validos():
    df = pd.DataFrame({
        "precio_prom_kg": [2000.0, 2500.0],
        "precio_min_kg": [1900.0, 2400.0],
        "precio_max_kg": [2100.0, 2600.0],
        "volumen_ingreso_ton": [50.0, 75.0],
        "divipola_depto": ["25", "52"],
        "divipola_mpio": ["25875", "52838"]
    })

    val = ValidationService(df)
    df_clean, rep = val.ejecutar_auditoria_completa()

    assert len(df_clean) == 2
    assert rep["dimension_completitud"]["precios_nulos_descartados"] == 0
    assert rep["dimension_consistencia_territorial"]["inconsistencias_codigo_departamento"] == 0
    assert rep["estado_general"] == "APROBADO_CON_CERO_NULOS"


def test_ejecutar_auditoria_completa_con_precios_nulos():
    df = pd.DataFrame({
        "precio_prom_kg": [2000.0, np.nan, -100.0, 3000.0],
        "precio_min_kg": [1900.0, 1000.0, 0.0, 2900.0],
        "precio_max_kg": [2100.0, 1500.0, 0.0, 3100.0],
        "volumen_ingreso_ton": [50.0, 10.0, 5.0, 80.0],
        "divipola_depto": ["25", "11", "15", "05"],
        "divipola_mpio": ["25875", "11001", "15001", "05001"]
    })

    val = ValidationService(df)
    df_clean, rep = val.ejecutar_auditoria_completa()

    # Solo deben quedar los registros con precio válido y > 0 (2 registros)
    assert len(df_clean) == 2
    assert rep["dimension_completitud"]["precios_nulos_descartados"] == 2
    assert df_clean["precio_prom_kg"].isna().sum() == 0
    assert (df_clean["precio_prom_kg"] <= 0).sum() == 0
