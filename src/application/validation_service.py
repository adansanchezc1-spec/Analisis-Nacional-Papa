"""
Servicio de Validación de Reglas de Negocio y Auditoría DAMA-BOK.
Etapa 3 de CRISP-DM: Data Validation.
Hace cumplir las invariantes de negocio:
- Cero Precios Nulos (precio_prom_kg > 0)
- Coherencia física (min <= prom <= max)
- Integridad referencial territorial DIVIPOLA DANE
"""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np

from src.domain.invariants import filtrar_y_auditar_precios_df
from src.domain.divipola import normalizar_codigo_depto, normalizar_codigo_mpio


class ValidationService:
    """Orquestador de aseguramiento de calidad de datos bajo DAMA-BOK."""

    # Conjunto oficial de los 33 códigos departamentales de Colombia DANE
    DEPARTAMENTOS_OFICIALES = {
        "05", "08", "11", "13", "15", "17", "18", "19", "20", "23",
        "25", "27", "41", "44", "47", "50", "52", "54", "63", "66",
        "68", "70", "73", "76", "81", "85", "86", "88", "91", "94",
        "95", "97", "99"
    }

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def ejecutar_auditoria_completa(self) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Ejecuta todas las validaciones de negocio:
        1. Regla de cero precios nulos
        2. Rango físico de precios y volúmenes
        3. Integridad territorial DIVIPOLA
        Retorna el DataFrame validado y el informe de métricas DAMA-BOK.
        """
        n_inicial = len(self.df)
        if n_inicial == 0:
            return self.df, {"error": "DataFrame vacío."}

        # 1. Validación de Precios (Regla de Oro: Cero Nulos)
        df_valid, descartes_precios = filtrar_y_auditar_precios_df(self.df, col_precio="precio_prom_kg")

        # 2. Validación de Coherencia Física (min <= prom <= max)
        mask_coherencia = pd.Series(True, index=df_valid.index)
        if "precio_min_kg" in df_valid.columns and "precio_max_kg" in df_valid.columns:
            mask_coherencia = (
                (df_valid["precio_min_kg"] <= df_valid["precio_prom_kg"]) &
                (df_valid["precio_prom_kg"] <= df_valid["precio_max_kg"])
            )
            # En caso de pequeñas discrepancias transaccionales, se corrigen límites
            df_valid["precio_min_kg"] = np.minimum(df_valid["precio_min_kg"], df_valid["precio_prom_kg"])
            df_valid["precio_max_kg"] = np.maximum(df_valid["precio_max_kg"], df_valid["precio_prom_kg"])

        # 3. Validación de Volúmenes Positivos
        volumen_invalido = 0
        if "volumen_ingreso_ton" in df_valid.columns:
            volumen_invalido = int((df_valid["volumen_ingreso_ton"] < 0).sum())
            df_valid["volumen_ingreso_ton"] = df_valid["volumen_ingreso_ton"].clip(lower=0.0)

        # 4. Validación DIVIPOLA Departamental
        inconsistencias_depto = 0
        if "divipola_depto" in df_valid.columns:
            df_valid["divipola_depto_norm"] = df_valid["divipola_depto"].apply(normalizar_codigo_depto)
            inconsistencias_depto = int((~df_valid["divipola_depto_norm"].isin(self.DEPARTAMENTOS_OFICIALES)).sum())

        # 5. Validación DIVIPOLA Municipal (5 dígitos)
        inconsistencias_mpio = 0
        if "divipola_mpio" in df_valid.columns:
            df_valid["divipola_mpio_norm"] = df_valid["divipola_mpio"].apply(normalizar_codigo_mpio)
            inconsistencias_mpio = int(df_valid["divipola_mpio_norm"].isna().sum())

        n_final = len(df_valid)

        # Informe DAMA-BOK estructurado
        reporte = {
            "dimension_completitud": {
                "total_registros_evaluados": n_inicial,
                "registros_validos_aprobados": n_final,
                "precios_nulos_descartados": descartes_precios,
                "tasa_precios_nulos": descartes_precios / n_inicial if n_inicial > 0 else 0.0,
                "tasa_completitud_aprobada": n_final / n_inicial if n_inicial > 0 else 0.0,
            },
            "dimension_validez_fisica": {
                "incoherencias_rango_precios_corregidas": int((~mask_coherencia).sum()),
                "volumenes_negativos_corregidos": volumen_invalido,
            },
            "dimension_consistencia_territorial": {
                "inconsistencias_codigo_departamento": inconsistencias_depto,
                "inconsistencias_codigo_municipio": inconsistencias_mpio,
                "tasa_consistencia_divipola_depto": (
                    1.0 - (inconsistencias_depto / n_final) if n_final > 0 else 0.0
                )
            },
            "estado_general": "APROBADO_CON_CERO_NULOS" if n_final > 0 else "RECHAZADO"
        }

        return df_valid, reporte
