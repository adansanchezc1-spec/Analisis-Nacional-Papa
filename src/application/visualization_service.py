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
        titulo: Optional[str] = None,
        dpi: int = 300,
        año: Optional[int] = None
    ) -> Path:
        """
        Renderiza las trayectorias del Índice Estacional de Precios (IEP) por mes.
        
        Permite generar la curva consolidada multi-anual o la curva individual
        para un año específico si se proporciona el parámetro `año`.
        """
        df_plot = df if año is None else df[df["año"] == año].copy()

        if titulo is None:
            if año is not None:
                titulo = f"Curvas de Estacionalidad Mensual de Precios (IEP) - Año {año}"
            else:
                titulo = "Curvas de Estacionalidad Mensual de Precios (IEP)"

        fig, ax = plt.subplots(figsize=(11, 6), dpi=dpi)

        col_iep = "indice_estacional_precio_iep" if "indice_estacional_precio_iep" in df_plot.columns else "precio_prom_kg"

        sns.lineplot(
            data=df_plot,
            x="mes",
            y=col_iep,
            hue="variedad_papa" if "variedad_papa" in df_plot.columns else None,
            marker="o",
            linewidth=2.2,
            errorbar=("ci", 95) if len(df_plot) > 12 else None,
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
        ylabel = "Índice Estacional de Precios (IEP %)" if col_iep == "indice_estacional_precio_iep" else "Precio Promedio ($/kg)"
        ax.set_ylabel(ylabel, fontsize=11, fontweight="bold")
        ax.grid(True, linestyle=":", alpha=0.6)
        if "variedad_papa" in df_plot.columns and df_plot["variedad_papa"].nunique() > 1:
            ax.legend(title="Variedad de Papa", frameon=True, fontsize=9, loc="upper right")

        plt.tight_layout()
        filename = f"curvas_estacionalidad_mensual_{año}.png" if año is not None else "curvas_estacionalidad_mensual.png"
        out_path = self.output_dir / filename
        fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)

        return out_path

    def graficar_curvas_estacionalidad_por_año(
        self,
        df: pd.DataFrame,
        año: int,
        dpi: int = 300
    ) -> Path:
        """Atajo para renderizar la curva de estacionalidad mensual para un año específico."""
        return self.graficar_curvas_estacionalidad_mensual(df=df, año=año, dpi=dpi)

    def graficar_estacionalidad_todos_los_años(
        self,
        df: pd.DataFrame,
        dpi: int = 300
    ) -> Dict[int, Path]:
        """
        Genera y exporta a 300 DPI las curvas de estacionalidad mensual para cada año individual
        presente en el conjunto de datos (ej. 2019 a 2025).
        """
        anios = sorted(df["año"].dropna().unique().astype(int))
        rutas_generadas: Dict[int, Path] = {}
        for a in anios:
            rutas_generadas[a] = self.graficar_curvas_estacionalidad_mensual(df=df, año=a, dpi=dpi)
        return rutas_generadas

    def graficar_panel_estacionalidad_todos_los_años(
        self,
        df: pd.DataFrame,
        titulo: str = "Panel Comparativo de Estacionalidad Mensual de Precios por Año (SIPSA 2019-2025)",
        dpi: int = 300
    ) -> Path:
        """
        Genera un panel de subgráficos (facet grid) con las curvas de estacionalidad
        de cada año lado a lado para facilitar la comparación interanual.
        """
        anios = sorted(df["año"].dropna().unique().astype(int))
        n_anios = len(anios)
        if n_anios == 0:
            return self.graficar_curvas_estacionalidad_mensual(df, dpi=dpi)

        n_cols = 3
        n_rows = int(np.ceil(n_anios / n_cols))
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4.5 * n_rows), dpi=dpi, sharey=True)
        axes_flat = axes.flatten() if hasattr(axes, "flatten") else [axes]

        col_iep = "indice_estacional_precio_iep" if "indice_estacional_precio_iep" in df.columns else "precio_prom_kg"

        for idx, anio in enumerate(anios):
            ax = axes_flat[idx]
            df_anio = df[df["año"] == anio]
            sns.lineplot(
                data=df_anio,
                x="mes",
                y=col_iep,
                hue="variedad_papa" if "variedad_papa" in df_anio.columns else None,
                marker="o",
                linewidth=1.8,
                ax=ax,
                legend=True if idx == 0 else False
            )
            ax.axhline(100.0, color="gray", linestyle="--", alpha=0.6)
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels(["E", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"], fontsize=8)
            ax.set_title(f"Año {anio}", fontsize=11, fontweight="bold")
            ax.set_xlabel("Mes", fontsize=9)
            if idx % n_cols == 0:
                ax.set_ylabel("IEP (%)", fontsize=9, fontweight="bold")
            else:
                ax.set_ylabel("")
            ax.grid(True, linestyle=":", alpha=0.5)

        for idx in range(n_anios, len(axes_flat)):
            fig.delaxes(axes_flat[idx])

        fig.suptitle(titulo, fontsize=14, fontweight="bold", y=1.01)
        plt.tight_layout()

        out_path = self.output_dir / "panel_estacionalidad_interanual.png"
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
        sns.barplot(data=df_oferta, x="año", y="volumen_ingreso_ton", hue="año", palette="Greens_d", legend=False, ax=axes[0, 0])
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

    def graficar_tablero_produccion_eva(
        self,
        df_eva: pd.DataFrame,
        titulo: str = "Tablero de Producción Agrícola Primaria de Papa en Colombia (EVA 2019-2025)",
        dpi: int = 300
    ) -> Path:
        """
        Genera un panel integrado 2x2 para el Pilar de Oferta con datos oficiales de campo EVA:
        1. Producción anual en toneladas por variedad (Papa Criolla vs Papa Todas las Variedades).
        2. Comparativo de Área Sembrada vs Área Cosechada (Hectáreas anuales).
        3. Rendimiento promedio (t/ha) por departamentos líderes.
        4. Boxplot de rendimientos agronómicos por variedad.
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 11), dpi=dpi)

        # 1. Producción por variedad y año
        df_prod_var = df_eva.groupby(["año", "desagregacion_cultivo"])["produccion_ton"].sum().reset_index()
        sns.barplot(data=df_prod_var, x="año", y="produccion_ton", hue="desagregacion_cultivo", palette="Set2", ax=axes[0, 0])
        axes[0, 0].set_title("1. Producción Anual por Variedad (Toneladas)", fontsize=11, fontweight="bold")
        axes[0, 0].set_xlabel("Año", fontsize=10)
        axes[0, 0].set_ylabel("Toneladas Producidas", fontsize=10)
        axes[0, 0].legend(title="Variedad EVA", fontsize=9)
        axes[0, 0].grid(True, linestyle=":", alpha=0.5, axis="y")

        # 2. Área Sembrada vs Cosechada
        df_areas = df_eva.groupby("año")[["area_sembrada_ha", "area_cosechada_ha"]].sum().reset_index()
        df_areas_melt = df_areas.melt(id_vars="año", value_vars=["area_sembrada_ha", "area_cosechada_ha"], var_name="tipo_area", value_name="hectareas")
        df_areas_melt["tipo_area"] = df_areas_melt["tipo_area"].replace({"area_sembrada_ha": "Área Sembrada", "area_cosechada_ha": "Área Cosechada"})
        sns.barplot(data=df_areas_melt, x="año", y="hectareas", hue="tipo_area", palette="Blues_d", ax=axes[0, 1])
        axes[0, 1].set_title("2. Uso de la Tierra: Área Sembrada vs Cosechada (Ha)", fontsize=11, fontweight="bold")
        axes[0, 1].set_xlabel("Año", fontsize=10)
        axes[0, 1].set_ylabel("Hectáreas Totales", fontsize=10)
        axes[0, 1].legend(title="Métrica", fontsize=9)
        axes[0, 1].grid(True, linestyle=":", alpha=0.5, axis="y")

        # 3. Rendimiento en departamentos líderes
        deptos_top = df_eva.groupby("departamento")["produccion_ton"].sum().nlargest(6).index.tolist()
        df_top_deptos = df_eva[df_eva["departamento"].isin(deptos_top)].groupby(["departamento", "año"])["rendimiento_ton_ha"].mean().reset_index()
        sns.lineplot(data=df_top_deptos, x="año", y="rendimiento_ton_ha", hue="departamento", marker="o", ax=axes[1, 0])
        axes[1, 0].set_title("3. Rendimiento Agrícola Promedio en Cuencas Líderes (t/ha)", fontsize=11, fontweight="bold")
        axes[1, 0].set_xlabel("Año", fontsize=10)
        axes[1, 0].set_ylabel("Rendimiento (t/ha)", fontsize=10)
        axes[1, 0].legend(title="Departamento", fontsize=8)
        axes[1, 0].grid(True, linestyle=":", alpha=0.5)

        # 4. Boxplot de Rendimiento por Variedad
        sns.boxplot(data=df_eva, x="desagregacion_cultivo", y="rendimiento_ton_ha", hue="desagregacion_cultivo", palette="Pastel1", legend=False, ax=axes[1, 1])
        axes[1, 1].set_title("4. Distribución del Rendimiento por Variedad (t/ha)", fontsize=11, fontweight="bold")
        axes[1, 1].set_xlabel("Variedad Comercial", fontsize=10)
        axes[1, 1].set_ylabel("Rendimiento (t/ha)", fontsize=10)
        axes[1, 1].grid(True, linestyle=":", alpha=0.5, axis="y")

        fig.suptitle(titulo, fontsize=14, fontweight="bold", y=1.02)
        plt.tight_layout()

        out_path = self.output_dir / "tablero_produccion_agricola_eva.png"
        fig.savefig(out_path, dpi=dpi, bbox_inches="tight")
        plt.close(fig)

        return out_path

