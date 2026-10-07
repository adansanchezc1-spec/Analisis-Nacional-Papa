"""
Servicio de Análisis Exploratorio de Datos (EDA).
Etapa 2 de CRISP-DM: Data Understanding / EDA.
Calcula medidas de tendencia central, dispersión, forma (asimetría, curtosis),
diagnóstico de Cullen & Frey, y matrices de correlación bivariada.
"""

from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
from scipy import stats


class EdaService:
    """Orquestador analítico para caracterización empírica de distribuciones."""

    def __init__(self, df: pd.DataFrame):
        """
        Inicializa el servicio con un DataFrame de mercado.
        df debe contener como mínimo: 'precio_prom_kg', 'volumen_ingreso_ton', 'año', 'mes', 'variedad_papa'.
        """
        self.df = df.copy()

    def calcular_medidas_resumen(self, columna: str = "precio_prom_kg") -> Dict[str, float]:
        """
        Calcula el conjunto completo de medidas descriptivas univariadas:
        Tendencia central, dispersión y forma.
        """
        serie = self.df[columna].dropna()
        n = len(serie)
        if n == 0:
            return {}

        media = float(np.mean(serie))
        mediana = float(np.median(serie))
        media_recortada_5 = float(stats.trim_mean(serie, 0.05))

        # Moda
        moda_res = stats.mode(serie, keepdims=True)
        moda = float(moda_res.mode[0]) if len(moda_res.mode) > 0 else media

        # Dispersión
        varianza = float(np.var(serie, ddof=1)) if n > 1 else 0.0
        desv_std = float(np.std(serie, ddof=1)) if n > 1 else 0.0
        q25 = float(np.percentile(serie, 25))
        q75 = float(np.percentile(serie, 75))
        iqr = q75 - q25
        mad = float(stats.median_abs_deviation(serie))
        cv = (desv_std / media) if media != 0 else 0.0

        # Forma (Skewness y Kurtosis)
        # Fisher-Pearson skewness
        skewness = float(stats.skew(serie, bias=False)) if n > 2 else 0.0
        # Curtosis de Fisher (exceso respecto a 3: Normal = 0)
        kurtosis_fisher = float(stats.kurtosis(serie, fisher=True, bias=False)) if n > 3 else 0.0
        # Curtosis de Pearson (Normal = 3)
        kurtosis_pearson = kurtosis_fisher + 3.0
        skewness_sq = skewness ** 2

        return {
            "n_observaciones": n,
            "media": media,
            "media_recortada_5pct": media_recortada_5,
            "mediana": mediana,
            "moda": moda,
            "varianza": varianza,
            "desviacion_estandar": desv_std,
            "coeficiente_variacion": cv,
            "q25": q25,
            "q75": q75,
            "iqr": iqr,
            "mad": mad,
            "minimo": float(np.min(serie)),
            "maximo": float(np.max(serie)),
            "asimetria_skewness": skewness,
            "asimetria_al_cuadrado": skewness_sq,
            "curtosis_fisher_exceso": kurtosis_fisher,
            "curtosis_pearson": kurtosis_pearson,
        }

    def calcular_resumen_estratificado(
        self,
        col_agrupacion: str = "año",
        col_variable: str = "precio_prom_kg"
    ) -> pd.DataFrame:
        """Calcula medidas estadísticas estratificadas por una dimensión (año, variedad, mercado)."""
        resultados = []
        for valor, grupo in self.df.groupby(col_agrupacion):
            eda_grupo = EdaService(grupo)
            res = eda_grupo.calcular_medidas_resumen(columna=col_variable)
            res[col_agrupacion] = valor
            resultados.append(res)

        df_res = pd.DataFrame(resultados)
        # Reordenar columna de agrupación al inicio
        cols = [col_agrupacion] + [c for c in df_res.columns if c != col_agrupacion]
        return df_res[cols]

    def calcular_coordenadas_cullen_frey(
        self,
        columna: str = "precio_prom_kg",
        n_bootstraps: int = 500
    ) -> Dict[str, Any]:
        """
        Calcula las coordenadas empíricas para el gráfico de Cullen & Frey:
        Observado: (Skewness^2, Kurtosis de Pearson)
        Bootstrap: Conjunto de réplicas para graficar la nube de incertidumbre muestral.
        """
        serie = self.df[columna].dropna().values
        n = len(serie)
        if n < 4:
            raise ValueError("Se requieren al menos 4 observaciones para Cullen & Frey.")

        s_obs = float(stats.skew(serie, bias=False))
        k_obs = float(stats.kurtosis(serie, fisher=False, bias=False))

        # Bootstrap de coordenadas (S^2, K)
        boot_s2 = []
        boot_k = []
        np.random.seed(42)
        for _ in range(n_bootstraps):
            sample = np.random.choice(serie, size=n, replace=True)
            s_b = float(stats.skew(sample, bias=False))
            k_b = float(stats.kurtosis(sample, fisher=False, bias=False))
            boot_s2.append(s_b ** 2)
            boot_k.append(k_b)

        return {
            "skewness_observado": s_obs,
            "skewness_sq_observado": s_obs ** 2,
            "kurtosis_observado": k_obs,
            "bootstrap_skewness_sq": boot_s2,
            "bootstrap_kurtosis": boot_k,
        }

    def calcular_matrices_correlacion(
        self,
        columnas: Optional[List[str]] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Calcula matrices de correlación bivariada:
        1. Pearson (Lineal / Paramétrica)
        2. Spearman (Monótona / No paramétrica basada en rangos)
        """
        if not columnas:
            columnas = [
                c for c in ["volumen_ingreso_ton", "precio_prom_kg", "precio_min_kg", "precio_max_kg", "año", "mes"]
                if c in self.df.columns
            ]

        df_subset = self.df[columnas].dropna()
        corr_pearson = df_subset.corr(method="pearson")
        corr_spearman = df_subset.corr(method="spearman")

        return corr_pearson, corr_spearman
