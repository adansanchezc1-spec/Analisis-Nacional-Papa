"""
Renderizador de Diagramas de Caja y Bigotes (Boxplots).
Permite examinar la dispersión, mediana, cuartiles y valores atípicos
estratificados por año, mes o variedad comercial.
"""

from pathlib import Path
from typing import Optional, List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class BoxplotPlotter:
    """Generador gráfico de diagramas de caja y bigotes estandarizados."""

    @staticmethod
    def plot_comparativo(
        df: pd.DataFrame,
        x_col: str,
        y_col: str = "precio_prom_kg",
        hue_col: Optional[str] = None,
        titulo: str = "Distribución y Dispersión de Precios",
        xlabel: str = "Categoría",
        ylabel: str = "Precio ($/kg)",
        output_path: Optional[Path] = None,
        dpi: int = 300,
        figsize: tuple = (12, 6)
    ) -> plt.Figure:
        """Renderiza un boxplot estilizado con Seaborn y Matplotlib."""
        fig, ax = plt.subplots(figsize=figsize, dpi=dpi)

        # Paleta armoniosa
        palette = "Set2" if hue_col else "Blues_r"

        sns.boxplot(
            data=df,
            x=x_col,
            y=y_col,
            hue=hue_col,
            palette=palette,
            showmeans=True,
            meanprops={"marker": "D", "markerfacecolor": "red", "markeredgecolor": "black", "markersize": 6},
            boxprops={"edgecolor": "black", "linewidth": 1.2},
            whiskerprops={"color": "black", "linewidth": 1.2},
            capprops={"color": "black", "linewidth": 1.2},
            medianprops={"color": "darkorange", "linewidth": 2.0},
            flierprops={"marker": "o", "color": "gray", "alpha": 0.5, "markersize": 4},
            ax=ax
        )

        ax.set_title(titulo, fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel(xlabel, fontsize=11, fontweight="bold")
        ax.set_ylabel(ylabel, fontsize=11, fontweight="bold")
        ax.grid(True, linestyle=":", alpha=0.5, axis="y")

        # Rotar etiquetas si son muchas categorías
        if df[x_col].nunique() > 6:
            plt.xticks(rotation=45, ha="right")

        if hue_col:
            ax.legend(title=hue_col, frameon=True, fontsize=9)

        plt.tight_layout()

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(output_path, dpi=dpi, bbox_inches="tight")

        return fig
