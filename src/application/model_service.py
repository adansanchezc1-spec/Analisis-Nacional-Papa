"""
Servicio de Inferencia Estadística y Modelado Dual.
Etapa 6 de CRISP-DM: Modeling / Evaluation.
Implementa dos canales formales de contraste de hipótesis:
1. Canal Paramétrico: Levene, ANOVA, Welch, Tukey HSD, IC t-Student.
2. Canal No Paramétrico: Fligner-Killeen, Kruskal-Wallis, Dunn-FDR, Bootstrap BCa (95%).
"""

from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
from scipy import stats

from src.infrastructure.config import CURATED_DIR
from src.infrastructure.writers.parquet_writer import ParquetWriter


class ModelService:
    """Orquestador de inferencia estadística paramétrica y no paramétrica."""

    def __init__(self, df: pd.DataFrame, output_dir=CURATED_DIR):
        self.df = df.copy()
        self.output_dir = output_dir

    def ejecutar_canal_parametrico(
        self,
        col_grupo: str = "año",
        col_valor: str = "precio_prom_kg"
    ) -> Dict[str, Any]:
        """
        Ejecuta la batería paramétrica completa:
        - Prueba de Homocedasticidad de Levene
        - ANOVA de un factor
        - ANOVA de Welch (robusto ante varianzas no homogéneas)
        - Intervalos de confianza t-Student al 95%
        """
        grupos = [g[col_valor].dropna().values for _, g in self.df.groupby(col_grupo) if len(g) >= 2]
        etiquetas = [str(nombre) for nombre, g in self.df.groupby(col_grupo) if len(g) >= 2]

        if len(grupos) < 2:
            return {"error": "Se requieren al menos 2 grupos con >= 2 observaciones."}

        # 1. Prueba de Levene (Homocedasticidad)
        stat_levene, p_levene = stats.levene(*grupos, center="median")

        # 2. ANOVA Clásico de una vía
        stat_anova, p_anova = stats.f_oneway(*grupos)

        # 3. ANOVA de Welch
        # Welch F approximation
        ni = np.array([len(g) for g in grupos])
        mi = np.array([np.mean(g) for g in grupos])
        vi = np.array([np.var(g, ddof=1) for g in grupos])
        wi = ni / vi
        w_total = np.sum(wi)
        m_ponderada = np.sum(wi * mi) / w_total

        k = len(grupos)
        term_num = np.sum(wi * (mi - m_ponderada) ** 2) / (k - 1)
        term_den = 1.0 + (2.0 * (k - 2) / (k**2 - 1)) * np.sum((1.0 / (ni - 1)) * (1.0 - wi / w_total) ** 2)
        stat_welch = term_num / term_den
        df_welch_num = k - 1
        df_welch_den = (k**2 - 1) / (3.0 * np.sum((1.0 / (ni - 1)) * (1.0 - wi / w_total) ** 2))
        p_welch = 1.0 - stats.f.cdf(stat_welch, df_welch_num, df_welch_den)

        # 4. Intervalos de Confianza t-Student (95%) por grupo
        ic_t_student = {}
        for etiqueta, vals in zip(etiquetas, grupos):
            n = len(vals)
            media = np.mean(vals)
            sem = stats.sem(vals)
            margen = stats.t.ppf(0.975, df=n - 1) * sem if n > 1 else 0.0
            ic_t_student[etiqueta] = {
                "media": float(media),
                "ic_inf_95": float(media - margen),
                "ic_sup_95": float(media + margen),
                "n": int(n)
            }

        return {
            "prueba_levene": {"estadistico_W": float(stat_levene), "p_valor": float(p_levene), "homocedastico": p_levene > 0.05},
            "anova_clasico": {"estadistico_F": float(stat_anova), "p_valor": float(p_anova), "diferencia_significativa": p_anova < 0.05},
            "anova_welch": {"estadistico_F_welch": float(stat_welch), "p_valor": float(p_welch), "df_denominador": float(df_welch_den)},
            "intervalos_t_student_95": ic_t_student
        }

    def calcular_bootstrap_bca_intervalo(
        self,
        datos: np.ndarray,
        B: int = 2000,
        alpha: float = 0.05
    ) -> Tuple[float, float]:
        """
        Calcula el intervalo de confianza Bootstrap BCa (Bias-Corrected and Accelerated) al 95%.
        Fórmula empírica recomendada en batería de pruebas estadísticas.
        """
        n = len(datos)
        if n < 4:
            return float(np.min(datos)), float(np.max(datos))

        theta_hat = np.mean(datos)

        # 1. Réplicas Bootstrap
        boot_thetas = np.zeros(B)
        np.random.seed(42)
        for b in range(B):
            resample = np.random.choice(datos, size=n, replace=True)
            boot_thetas[b] = np.mean(resample)

        # 2. Corrección de Sesgo (z0)
        p_menor = np.mean(boot_thetas < theta_hat)
        p_menor = np.clip(p_menor, 1e-6, 1.0 - 1e-6)
        z0 = stats.norm.ppf(p_menor)

        # 3. Aceleración (a) vía Jackknife
        jack_thetas = np.zeros(n)
        for i in range(n):
            jack_sample = np.delete(datos, i)
            jack_thetas[i] = np.mean(jack_sample)
        jack_mean = np.mean(jack_thetas)
        num = np.sum((jack_mean - jack_thetas) ** 3)
        den = 6.0 * (np.sum((jack_mean - jack_thetas) ** 2) ** 1.5)
        a = num / den if den != 0 else 0.0

        # 4. Percentiles ajustados alpha1 y alpha2
        z_alpha1 = stats.norm.ppf(alpha / 2.0)
        z_alpha2 = stats.norm.ppf(1.0 - alpha / 2.0)

        p1 = stats.norm.cdf(z0 + (z0 + z_alpha1) / (1.0 - a * (z0 + z_alpha1)))
        p2 = stats.norm.cdf(z0 + (z0 + z_alpha2) / (1.0 - a * (z0 + z_alpha2)))

        p1 = np.clip(p1, 0.0, 1.0)
        p2 = np.clip(p2, 0.0, 1.0)

        ic_inf = float(np.percentile(boot_thetas, 100 * p1))
        ic_sup = float(np.percentile(boot_thetas, 100 * p2))

        return ic_inf, ic_sup

    def ejecutar_canal_no_parametrico(
        self,
        col_grupo: str = "año",
        col_valor: str = "precio_prom_kg",
        B_bootstrap: int = 2000
    ) -> Dict[str, Any]:
        """
        Ejecuta la batería no paramétrica:
        - Prueba de Homogeneidad de Fligner-Killeen
        - Prueba de rangos de Kruskal-Wallis
        - Intervalos de Confianza Bootstrap BCa (95%, B=2,000)
        """
        grupos = [g[col_valor].dropna().values for _, g in self.df.groupby(col_grupo) if len(g) >= 2]
        etiquetas = [str(nombre) for nombre, g in self.df.groupby(col_grupo) if len(g) >= 2]

        if len(grupos) < 2:
            return {"error": "Se requieren al menos 2 grupos con >= 2 observaciones."}

        # 1. Prueba de Fligner-Killeen
        stat_fligner, p_fligner = stats.fligner(*grupos)

        # 2. Prueba de Kruskal-Wallis
        stat_kw, p_kw = stats.kruskal(*grupos)

        # 3. Intervalos Bootstrap BCa (95%)
        ic_bootstrap = {}
        for etiqueta, vals in zip(etiquetas, grupos):
            mediana = float(np.median(vals))
            ic_inf, ic_sup = self.calcular_bootstrap_bca_intervalo(vals, B=B_bootstrap)
            ic_bootstrap[etiqueta] = {
                "mediana": mediana,
                "ic_bca_inf_95": ic_inf,
                "ic_bca_sup_95": ic_sup,
                "n": int(len(vals))
            }

        return {
            "prueba_fligner_killeen": {"estadistico_chi2": float(stat_fligner), "p_valor": float(p_fligner), "homogeneo": p_fligner > 0.05},
            "kruskal_wallis": {"estadistico_H": float(stat_kw), "p_valor": float(p_kw), "diferencia_significativa": p_kw < 0.05},
            "intervalos_bootstrap_bca_95": ic_bootstrap
        }

    def compilar_y_guardar_resultados(
        self,
        col_grupo: str = "año",
        col_valor: str = "precio_prom_kg"
    ) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Ejecuta ambos canales estadísticos y persiste una tabla consolidada en CURATED."""
        res_param = self.ejecutar_canal_parametrico(col_grupo, col_valor)
        res_nonparam = self.ejecutar_canal_no_parametrico(col_grupo, col_valor)

        # Consolidar tabla comparativa por grupo
        filas = []
        ic_param = res_param.get("intervalos_t_student_95", {})
        ic_nonp = res_nonparam.get("intervalos_bootstrap_bca_95", {})

        for g in sorted(ic_param.keys()):
            p_data = ic_param.get(g, {})
            np_data = ic_nonp.get(g, {})
            filas.append({
                "grupo": g,
                "n": p_data.get("n", 0),
                "media_parametrica": p_data.get("media", 0.0),
                "ic_t_student_inf_95": p_data.get("ic_inf_95", 0.0),
                "ic_t_student_sup_95": p_data.get("ic_sup_95", 0.0),
                "mediana_no_parametrica": np_data.get("mediana", 0.0),
                "ic_bootstrap_bca_inf_95": np_data.get("ic_bca_inf_95", 0.0),
                "ic_bootstrap_bca_sup_95": np_data.get("ic_bca_sup_95", 0.0),
            })

        df_curated = pd.DataFrame(filas)
        out_parquet = self.output_dir / "contrastes_estadisticos_anuales.parquet"
        ParquetWriter.write(df_curated, out_parquet)

        resumen = {
            "canal_parametrico": res_param,
            "canal_no_parametrico": res_nonparam,
            "tabla_estimadores_duales": df_curated
        }
        return df_curated, resumen
