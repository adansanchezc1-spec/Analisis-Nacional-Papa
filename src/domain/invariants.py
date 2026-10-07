"""
Módulo de Invariantes de Negocio.
Asegura el cumplimiento estricto de reglas de integridad:
1. Cero Precios Nulos (precio_prom_kg IS NOT NULL and > 0).
2. Coherencia física de cotizaciones (min <= prom <= max).
"""

from typing import Tuple
import pandas as pd
import numpy as np

from src.domain.exceptions import PriceNullViolationError, PhysicalRangeViolationError


def validar_precio_escalar(precio: float) -> bool:
    """Verifica si un precio individual cumple la regla estricta de no nulidad y positividad."""
    if precio is None or pd.isna(precio) or np.isnan(precio) or precio <= 0:
        raise PriceNullViolationError(f"Precio inválido o nulo detectado: {precio}")
    return True


def validar_coherencia_precios_escalar(p_min: float, p_prom: float, p_max: float) -> bool:
    """Verifica la relación de orden física p_min <= p_prom <= p_max."""
    validar_precio_escalar(p_min)
    validar_precio_escalar(p_prom)
    validar_precio_escalar(p_max)
    if not (p_min <= p_prom <= p_max):
        raise PhysicalRangeViolationError(
            f"Inconsistencia física detectada: min ({p_min}) <= prom ({p_prom}) <= max ({p_max})"
        )
    return True


def filtrar_y_auditar_precios_df(df: pd.DataFrame, col_precio: str = "precio_prom_kg") -> Tuple[pd.DataFrame, int]:
    """
    Filtra vectorialmente cualquier registro con precio nulo o <= 0,
    retornando el DataFrame saneado y el conteo de registros excluidos para auditoría.
    """
    if col_precio not in df.columns:
        raise KeyError(f"Columna {col_precio} no presente en el DataFrame.")

    # Máscara booleana de validez estricta
    mascara_valida = (
        df[col_precio].notna() &
        ~df[col_precio].isin([np.nan, None]) &
        (df[col_precio] > 0)
    )

    n_nulos_o_invalidos = int((~mascara_valida).sum())
    df_saneado = df[mascara_valida].copy()

    return df_saneado, n_nulos_o_invalidos


def validar_invariantes_eva_df(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    """
    Valida las reglas de consistencia física para el dataset agrícola EVA:
    - area_sembrada_ha >= 0 y area_cosechada_ha >= 0
    - produccion_ton >= 0
    - rendimiento_ton_ha >= 0
    """
    cols_requeridas = ["area_sembrada_ha", "area_cosechada_ha", "produccion_ton", "rendimiento_ton_ha"]
    for c in cols_requeridas:
        if c not in df.columns:
            raise KeyError(f"Columna requerida {c} no encontrada en DataFrame EVA.")

    mascara_valida = (
        (df["area_sembrada_ha"] >= 0) &
        (df["area_cosechada_ha"] >= 0) &
        (df["produccion_ton"] >= 0) &
        (df["rendimiento_ton_ha"] >= 0)
    )
    n_invalidos = int((~mascara_valida).sum())
    df_valido = df[mascara_valida].copy()

    return df_valido, n_invalidos

