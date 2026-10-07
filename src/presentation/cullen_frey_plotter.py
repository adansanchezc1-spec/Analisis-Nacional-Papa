"""
Renderizador del Gráfico de Cullen y Frey (Skewness^2 vs Kurtosis).
Permite diagnosticar visualmente la familia de distribución de probabilidad empírica
(Normal, Lognormal, Gamma, Weibull, Uniforme, Exponencial) con incertidumbre Bootstrap.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np
import matplotlib.pyplot as plt


class CullenFreyPlotter:
    """Generador gráfico del mapa de Cullen y Frey estándar (fitdistrplus style)."""

    @staticmethod
    def plot(
        cf_coords: Dict[str, Any],
        titulo: str = "Gráfico de Cullen y Frey — Diagnóstico de Distribución",
        output_path: Optional[Path] = None,
        dpi: int = 300
    ) -> plt.Figure:
        """
        Renderiza el gráfico de Cullen & Frey.
        Eje X: Skewness^2 (Asimetría al cuadrado).
        Eje Y: Curtosis de Pearson (con eje invertido como en el estándar biométrico).
        """
        fig, ax = plt.subplots(figsize=(9, 7), dpi=dpi)

        s2_obs = cf_coords["skewness_sq_observado"]
        k_obs = cf_coords["kurtosis_observado"]
        boot_s2 = cf_coords.get("bootstrap_skewness_sq", [])
        boot_k = cf_coords.get("bootstrap_kurtosis", [])

        # Rango del gráfico
        max_s2 = max(4.5, s2_obs * 1.3, max(boot_s2) if boot_s2 else 0)
        max_k = max(10.0, k_obs * 1.3, max(boot_k) if boot_k else 0)

        # 1. Puntos Teóricos de Referencia
        ax.plot(0, 3, "o", color="blue", markersize=8, label="Normal (0, 3)")
        ax.plot(0, 1.8, "s", color="green", markersize=8, label="Uniforme (0, 1.8)")
        ax.plot(4, 9, "^", color="darkorange", markersize=8, label="Exponencial (4, 9)")
        ax.plot(0, 4.2, "d", color="purple", markersize=8, label="Logística (0, 4.2)")

        # 2. Líneas Teóricas Continuas
        s2_vals = np.linspace(0, max_s2 + 1, 200)

        # Línea Gamma: K = 3 + 1.5 * S^2
        k_gamma = 3 + 1.5 * s2_vals
        ax.plot(s2_vals, k_gamma, "--", color="red", linewidth=1.8, label="Línea Gamma ($K = 3 + 1.5 S^2$)")

        # Línea Lognormal aproximada
        # Para lognormal, S = (w+2)*sqrt(w-1), K = w^4 + 2w^3 + 3w^2 - 3 con w = exp(sigma^2)
        w = np.linspace(1.001, 2.5, 200)
        s_ln = (w + 2) * np.sqrt(w - 1)
        k_ln = w**4 + 2 * w**3 + 3 * w**2 - 3
        ax.plot(s_ln**2, k_ln, "-.", color="brown", linewidth=1.8, label="Línea Lognormal")

        # 3. Nube de Incertidumbre Bootstrap
        if boot_s2 and boot_k:
            ax.scatter(boot_s2, boot_k, color="gold", alpha=0.35, s=25, label="Réplicas Bootstrap", zorder=3)

        # 4. Dato Observado de la Muestra
        ax.scatter(
            [s2_obs], [k_obs],
            color="crimson",
            s=120,
            edgecolors="black",
            linewidths=1.5,
            label=f"Observación Empírica ($S^2={s2_obs:.2f}, K={k_obs:.2f}$)",
            zorder=5
        )

        # Configuración estética
        ax.set_xlabel("Asimetría al cuadrado ($Skewness^2$)", fontsize=11, fontweight="bold")
        ax.set_ylabel("Curtosis de Pearson ($Kurtosis$)", fontsize=11, fontweight="bold")
        ax.set_title(titulo, fontsize=13, fontweight="bold", pad=12)

        # Eje invertido tradicional (Mayor curtosis abajo)
        ax.set_ylim(bottom=max_k + 1, top=1.0)
        ax.set_xlim(left=-0.1, right=max_s2 + 0.5)

        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), frameon=True, fontsize=9)

        plt.tight_layout()

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(output_path, dpi=dpi, bbox_inches="tight")

        return fig
