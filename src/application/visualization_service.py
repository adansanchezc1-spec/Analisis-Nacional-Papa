"""
Servicio de Visualización y Renderizado de Tableros Ejecutivos.
Etapa 7 de CRISP-DM: Visualization / Deployment.
Genera figuras en alta resolución (300 DPI) para los tres pilares del mercado:
Oferta, Demanda y Precios.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from src.infrastructure.config import CURATED_DIR
from src.presentation.cullen_frey_plotter import CullenFreyPlotter
from src.presentation.boxplot_plotter import BoxplotPlotter
from src.presentation.correlation_plotter import CorrelationPlotter


class VisualizationService:
    """Orquestador de reportes visuales y tableros analíticos a 300 DPI."""

    def __init__(self, output_dir: Path = CURATED_DIR / "reportes_graficos"):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def graficar_curvas_estacionalidad_mensual(
        self,
        df: pd.DataFrame,
        titulo: str = "Curvas de Estacionalidad Mensual de Precios (IEP)",
        dpi: int = 300
    ) -> Path:
        """Renderiza las trayectorias del Índice Estacional de Precios (IEP) por mes."""
        fig, ax = plt.subplots(figsize=(11, 6), dpi=dpi)

        col_iep = "indice_estacional_precio_iep" if "indice_estacional_precio_iep" in df.columns else "precio_prom_kg"

        sns.lineplot(
            data=df,
            x="mes",
            y=col_iep,
            hue="variedad_papa" if "variedad_papa" in df.columns else None,
            marker="o",
            linewidth=2.2,
            errorbar=("ci", 95),
            ax=ax
        )

        ax.axhline(100.0, color="gray", linestyle="--", alpha=0.7, label="Nivel Base Anual (100)")
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels([
            "Ene", "Feb", "Mar", "Abr", "May", "Jun",
            "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
        ], fontsize=10, fontweight="bold")

        ax.set_title(titulo, fontsize=13, fontweight="bold", pad=12)
        ax.set_xlabel("Mes Calendario", fontsize=11, fontweight="bold")
        ax.set_ylabel("Índice Estacional de Precios (IEP %)", fontsize=11, fontweight="bold")
        ax.grid(True, linestyle=":", alpha=0.6)
        ax.legend(title="Variedad de Papa", frameon=True, fontsize=9)

        plt.tight_layout()
        out_path = self.output_dir / "curvas_estacionalidad_mensual.png"
        fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)

        return out_path

    def graficar_tablero_ejecutivo_tres_pilares(
        self,
        df: pd.DataFrame,
        titulo: str = "Tablero Ejecutivo: Análisis Crítico del Mercado de la Papa en Colombia (SIPSA 2019-2025)",
        dpi: int = 300
    ) -> Path:
        """
        Genera un panel integrado 2x2 cubriendo los tres pilares de negocio:
        1. Oferta: Volúmenes históricos anuales (toneladas)
        2. Demanda: Consumo per cápita mayorista (kg/hab)
        3. Precios: Evolución temporal del precio promedio ($/kg)
        4. Dispersión: Relación Precio vs Volumen (Curva empírica de mercado)
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 11), dpi=dpi)

        # 1. PILAR OFERTA: Volúmenes por año
        df_oferta = df.groupby("año")["volumen_ingreso_ton"].sum().reset_index()
        sns.barplot(data=df_oferta, x="año", y="volumen_ingreso_ton", palette="Greens_d", ax=axes[0, 0])
        axes[0, 0].set_title("1. Pilar Oferta: Volumen Anual Ingresado (Toneladas)", fontsize=11, fontweight="bold")
        axes[0, 0].set_xlabel("Año", fontsize=10)
        axes[0, 0].set_ylabel("Toneladas Totales", fontsize=10)
        axes[0, 0].grid(True, linestyle=":", alpha=0.5, axis="y")

        # 2. PILAR DEMANDA: Consumo per cápita promedio
        col_percap = "consumo_mayorista_per_capita_kg" if "consumo_mayorista_per_capita_kg" in df.columns else "volumen_ingreso_ton"
        df_demanda = df.groupby("año")[col_percap].mean().reset_index()
        sns.lineplot(data=df_demanda, x="año", y=col_percap, marker="s", color="darkblue", linewidth=2.5, ax=axes[0, 1])
        axes[0, 1].set_title("2. Pilar Demanda: Absorción Mensual Per Cápita (kg/hab)", fontsize=11, fontweight="bold")
        axes[0, 1].set_xlabel("Año", fontsize=10)
        axes[0, 1].set_ylabel("kg / habitante / mes", fontsize=10)
        axes[0, 1].grid(True, linestyle=":", alpha=0.5)

        # 3. PILAR PRECIOS: Evolución de precios promedio con intervalo 95%
        sns.lineplot(data=df, x="año", y="precio_prom_kg", hue="variedad_papa" if "variedad_papa" in df.columns else None, marker="o", ax=axes[1, 0])
        axes[1, 0].set_title("3. Pilar Precios: Evolución Temporal ($/kg)", fontsize=11, fontweight="bold")
        axes[1, 0].set_xlabel("Año", fontsize=10)
        axes[1, 0].set_ylabel("Precio Promedio ($/kg)", fontsize=10)
        axes[1, 0].grid(True, linestyle=":", alpha=0.5)

        # 4. DISPERSIÓN MERCADO: Elasticidad y Relación Precio vs Volumen
        sns.scatterplot(data=df, x="volumen_ingreso_ton", y="precio_prom_kg", alpha=0.5, color="purple", ax=axes[1, 1])
        axes[1, 1].set_title("4. Formación de Mercado: Relación Volumen vs Precio", fontsize=11, fontweight="bold")
        axes[1, 1].set_xlabel("Volumen Ingresado (Ton)", fontsize=10)
        axes[1, 1].set_ylabel("Precio Promedio ($/kg)", fontsize=10)
        axes[1, 1].grid(True, linestyle=":", alpha=0.5)

        fig.suptitle(titulo, fontsize=14, fontweight="bold", y=1.02)
        plt.tight_layout()

        out_path = self.output_dir / "tablero_ejecutivo_tres_pilares.png"
        fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)

        return out_path
