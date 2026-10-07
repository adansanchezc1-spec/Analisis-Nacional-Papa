"""
Servicio de Ingeniería de Características (Features) y Acople Demográfico.
Etapa 5 de CRISP-DM: Feature Engineering.
Calcula métricas per cápita (kg/hab/mes y ton/hab/año),
Índice Estacional de Precios (IEP), Índice Estacional de Oferta (IEO),
y etiquetado booleano de anomalías (IQR Tukey y MAD).
"""

from pathlib import Path
from typing import Dict, Optional, Tuple
import numpy as np
import pandas as pd
from scipy import stats

from src.infrastructure.config import RAW_DEMO_DIR, FEATURES_DIR
from src.infrastructure.writers.parquet_writer import ParquetWriter


class FeaturesService:
    """Orquestador de enriquecimiento analítico y cálculo de indicadores per cápita."""

    # Proyecciones macro-demográficas nacionales DANE 2018-2026 (Cabecera y Total)
    # Extraídas oficialmente de PPED-AreaNac-2018-2070.xlsx
    POBLACION_NACIONAL_DANE = {
        2018: {"cabecera": 36414521, "rural": 11843973, "total": 48258494},
        2019: {"cabecera": 37219289, "rural": 12047237, "total": 49266526},
        2020: {"cabecera": 38130362, "rural": 12260428, "total": 50390790},
        2021: {"cabecera": 38710371, "rural": 12405266, "total": 51115637},
        2022: {"cabecera": 39130235, "rural": 12513330, "total": 51643565},
        2023: {"cabecera": 39507801, "rural": 12609266, "total": 52117067},
        2024: {"cabecera": 39903699, "rural": 12710054, "total": 52613753},
        2025: {"cabecera": 40257670, "rural": 12799542, "total": 53057212},
        2026: {"cabecera": 40529928, "rural": 12869243, "total": 53399171},
    }

    def __init__(self, df: pd.DataFrame, output_dir=FEATURES_DIR):
        self.df = df.copy()
        self.output_dir = output_dir

    def acoplar_demografia_y_per_capita(self) -> pd.DataFrame:
        """Incorpora la población nacional y calcula consumo mayorista per cápita (kg/hab/mes)."""
        df_feat = self.df.copy()

        # Asignar población según año
        def obtener_pob(año, tipo="total"):
            return self.POBLACION_NACIONAL_DANE.get(int(año), {}).get(tipo, 51000000)

        df_feat["poblacion_nacional_total"] = df_feat["año"].apply(lambda y: obtener_pob(y, "total"))
        df_feat["poblacion_nacional_cabecera"] = df_feat["año"].apply(lambda y: obtener_pob(y, "cabecera"))

        # Consumo per cápita mensual por mercado mayorista en kilogramos por habitante
        # (Volumen en toneladas * 1000 kg / Población cabecera de influencia)
        df_feat["consumo_mayorista_per_capita_kg"] = (
            (df_feat["volumen_ingreso_ton"] * 1000.0) / df_feat["poblacion_nacional_cabecera"]
        )

        return df_feat

    def calcular_indices_estacionales(self) -> pd.DataFrame:
        """
        Calcula el Índice Estacional de Precios (IEP) y de Oferta (IEO)
        IEP_m = (Precio_promedio_mes_m / Precio_promedio_anual) * 100
        """
        df_feat = self.df.copy()

        # Promedios anuales de referencia
        prom_anual_p = df_feat.groupby("año")["precio_prom_kg"].transform("mean")
        prom_anual_v = df_feat.groupby("año")["volumen_ingreso_ton"].transform("mean")

        # Índice mensual respecto al promedio de su año
        df_feat["indice_estacional_precio_iep"] = (df_feat["precio_prom_kg"] / prom_anual_p) * 100.0
        df_feat["indice_estacional_oferta_ieo"] = (
            (df_feat["volumen_ingreso_ton"] / prom_anual_v) * 100.0
            if prom_anual_v.min() > 0 else 100.0
        )

        return df_feat

    def etiquetar_anomalias(self) -> pd.DataFrame:
        """
        Etiqueta outliers de precio utilizando dos métodos robustos:
        1. Criterio de Tukey (IQR): Fuera de [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
        2. Z-Score Modificado con MAD: |Precio - Mediana| / (1.4826 * MAD) > 3.5
        No elimina filas; genera columnas booleanas de marcado.
        """
        df_feat = self.df.copy()

        # Por cada variedad y año para no mezclar heterogeneidades estructurales
        df_feat["es_outlier_iqr"] = False
        df_feat["es_outlier_mad"] = False

        for (año, var), grupo in df_feat.groupby(["año", "variedad_papa"]):
            precios = grupo["precio_prom_kg"].values
            if len(precios) < 5:
                continue

            q25, q75 = np.percentile(precios, [25, 75])
            iqr = q75 - q25
            lim_inf = q25 - 1.5 * iqr
            lim_sup = q75 + 1.5 * iqr

            mask_iqr = (grupo["precio_prom_kg"] < lim_inf) | (grupo["precio_prom_kg"] > lim_sup)
            df_feat.loc[grupo.index, "es_outlier_iqr"] = mask_iqr

            # MAD
            mediana = np.median(precios)
            mad = stats.median_abs_deviation(precios)
            if mad > 0:
                mod_z = np.abs(precios - mediana) / (1.4826 * mad)
                mask_mad = mod_z > 3.5
                df_feat.loc[grupo.index, "es_outlier_mad"] = mask_mad

        return df_feat

    def construir_panel_completo_features(self) -> pd.DataFrame:
        """Ejecuta todo el pipeline de generación de características y persiste."""
        # 1. Demografía y Per Cápita
        self.df = self.acoplar_demografia_y_per_capita()

        # 2. Estacionalidad
        self.df = self.calcular_indices_estacionales()

        # 3. Anomalías
        self.df = self.etiquetar_anomalias()

        # Persistencia en Capa FEATURES
        out_parquet = self.output_dir / "dataset_sipsa_features.parquet"
        ParquetWriter.write(self.df, out_parquet)

        return self.df
