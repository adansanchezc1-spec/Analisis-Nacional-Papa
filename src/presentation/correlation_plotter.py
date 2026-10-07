"""
Renderizador de Matrices de Correlación Bivariada (Pearson y Spearman).
Genera mapas de calor con valores numéricos anotados y paleta divergente.
"""

from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class CorrelationPlotter:
    """Generador gráfico de matrices de calor de correlación."""

    @staticmethod
    def plot_dual_heatmaps(
        corr_pearson: pd.DataFrame,
        corr_spearman: pd.DataFrame,
        titulo: str = "Matrices de Correlación Bivariada: Pearson vs Spearman",
        output_path: Optional[Path] = None,
        dpi: int = 300,
        figsize: tuple = (15, 6)
    ) -> plt.Figure:
        """Renderiza en paralelo los heatmaps de correlación lineal y no paramétrica."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, dpi=dpi)

        # Mapa de Calor 1: Pearson (Lineal)
        sns.heatmap(
            corr_pearson,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            vmin=-1.0,
            vmax=1.0,
            cbar=True,
            square=True,
            linewidths=0.5,
            ax=ax1
        )
        ax1.set_title("Correlación de Pearson (Lineal)", fontsize=11, fontweight="bold")

        # Mapa de Calor 2: Spearman (Monótona / Rangos)
        sns.heatmap(
            corr_spearman,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            vmin=-1.0,
            vmax=1.0,
            cbar=True,
            square=True,
            linewidths=0.5,
            ax=ax2
        )
        ax2.set_title("Correlación de Spearman (No Paramétrica / Rangos)", fontsize=11, fontweight="bold")

        fig.suptitle(titulo, fontsize=13, fontweight="bold", y=1.02)
        plt.tight_layout()

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(output_path, dpi=dpi, bbox_inches="tight")

        return fig
