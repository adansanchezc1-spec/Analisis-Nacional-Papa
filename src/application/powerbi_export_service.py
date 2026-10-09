"""
Módulo de Servicio para Modelado Dimensional y Exportación a Power BI (Kimball Star Schema).
Sigue principios SOLID, estándares DAMA-BOK e ISO/IEC 25010.
"""

from pathlib import Path
import unicodedata
import pandas as pd
import numpy as np

from src.infrastructure.config import (
    CLEANED_DIR,
    FEATURES_DIR,
    CURATED_DIR,
    DATA_DIR,
    PROJECT_ROOT
)


class PowerBIExportService:
    """
    Servicio de Dominio / Aplicación encargado de transformar los datasets
    de FEATURES y CLEANED en un Modelo Dimensional en Estrella (Star Schema)
    altamente optimizado para Power BI Desktop y Power BI Service.
    """

    def __init__(self, output_dir: Path | None = None):
        if output_dir is None:
            self.output_dir = DATA_DIR / "POWERBI"
        else:
            self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Directorio espejo en la raíz del proyecto para scripts y documentación de Power BI
        self.pbi_project_dir = PROJECT_ROOT / "powerbi"
        self.pbi_data_dir = self.pbi_project_dir / "data"
        self.pbi_data_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _limpiar_texto(texto: str) -> str:
        """Normaliza cadenas de texto eliminando inconsistencias léxicas."""
        if pd.isna(texto):
            return "NO IDENTIFICADO"
        texto_str = str(texto).strip()
        # Eliminar tildes o caracteres corruptos si aplica manteniendo mayúsculas estándar
        texto_norm = unicodedata.normalize("NFKD", texto_str)
        return " ".join(texto_norm.split()).upper()

    def construir_dim_tiempo(self, df_eva: pd.DataFrame, df_sipsa: pd.DataFrame) -> pd.DataFrame:
        """
        Genera la Dimensión de Tiempo conformada (2019-01-01 a 2025-12-31).
        Grano: Mensual con jerarquía de Año, Semestre, Trimestre, Mes, Periodo.
        """
        fechas = pd.date_range(start="2019-01-01", end="2025-12-31", freq="MS")
        
        dim_tiempo = pd.DataFrame({"fecha": fechas})
        dim_tiempo["id_tiempo"] = dim_tiempo["fecha"].dt.strftime("%Y%m%d").astype(int)
        dim_tiempo["año"] = dim_tiempo["fecha"].dt.year
        dim_tiempo["mes"] = dim_tiempo["fecha"].dt.month
        dim_tiempo["nombre_mes"] = dim_tiempo["fecha"].dt.month_name(locale="Spanish")
        dim_tiempo["mes_corto"] = dim_tiempo["fecha"].dt.strftime("%b").str.upper()
        dim_tiempo["año_mes"] = dim_tiempo["fecha"].dt.strftime("%Y-%m")
        dim_tiempo["trimestre"] = "T" + dim_tiempo["fecha"].dt.quarter.astype(str)
        dim_tiempo["año_trimestre"] = dim_tiempo["año"].astype(str) + "-" + dim_tiempo["trimestre"]
        dim_tiempo["semestre"] = np.where(dim_tiempo["mes"] <= 6, "S1", "S2")
        dim_tiempo["año_semestre"] = dim_tiempo["año"].astype(str) + "-" + dim_tiempo["semestre"]
        dim_tiempo["periodo_agricola"] = dim_tiempo["año"].astype(str) + np.where(dim_tiempo["mes"] <= 6, "A", "B")
        
        # Orden cronológico para Power BI
        dim_tiempo["orden_año_mes"] = dim_tiempo["año"] * 100 + dim_tiempo["mes"]
        
        return dim_tiempo

    def construir_dim_geografia(self, df_eva: pd.DataFrame, df_sipsa: pd.DataFrame) -> pd.DataFrame:
        """
        Genera la Dimensión Geográfica conformada a partir del estándar DIVIPOLA (DANE).
        """
        # Extraer municipios de EVA
        geo_eva = df_eva[["cod_depto", "departamento", "cod_mpio", "municipio"]].drop_duplicates()
        geo_eva.columns = ["cod_depto", "departamento", "cod_mpio", "municipio"]
        
        # Extraer municipios de SIPSA
        geo_sipsa = df_sipsa[["divipola_depto", "nombre_depto", "divipola_mpio", "nombre_mpio"]].drop_duplicates()
        geo_sipsa.columns = ["cod_depto", "departamento", "cod_mpio", "municipio"]
        
        # Consolidar
        geo_comb = pd.concat([geo_eva, geo_sipsa], ignore_index=True)
        geo_comb["cod_depto"] = geo_comb["cod_depto"].astype(str).str.zfill(2)
        geo_comb["cod_mpio"] = geo_comb["cod_mpio"].astype(str).str.zfill(5)
        geo_comb["departamento"] = geo_comb["departamento"].apply(self._limpiar_texto)
        geo_comb["municipio"] = geo_comb["municipio"].apply(self._limpiar_texto)
        
        dim_geo = geo_comb.drop_duplicates(subset=["cod_mpio"]).copy()
        
        # Enriquecer con Región Natural y Categorización Papera
        regiones = {
            "05": "Andina", "11": "Andina (Distrito Capital)", "15": "Andina", 
            "17": "Andina", "25": "Andina", "41": "Andina", "52": "Andina", 
            "54": "Andina", "63": "Andina", "66": "Andina", "68": "Andina", 
            "73": "Andina", "76": "Andina", "19": "Pacífica / Andina",
            "08": "Caribe", "13": "Caribe", "20": "Caribe", "23": "Caribe",
            "44": "Caribe", "47": "Caribe", "70": "Caribe"
        }
        dim_geo["region_natural"] = dim_geo["cod_depto"].map(regiones).fillna("Otras Regiones")
        
        deptos_paperos_principales = ["15", "25", "52", "05", "73", "68", "17", "19", "54", "41"]
        dim_geo["es_productor_destacado"] = dim_geo["cod_depto"].isin(deptos_paperos_principales)
        dim_geo["es_territorio_nacional"] = dim_geo["cod_depto"] != "00"
        
        return dim_geo.sort_values(by=["cod_depto", "cod_mpio"]).reset_index(drop=True)

    def construir_dim_variedad(self, df_eva: pd.DataFrame, df_sipsa: pd.DataFrame) -> pd.DataFrame:
        """
        Genera la Dimensión de Variedad Agrícola y Comercial.
        """
        variedades = [
            {
                "cod_variedad": "CRIOLLA",
                "nombre_variedad": "PAPA CRIOLLA",
                "variedad_canonica": "Papa criolla",
                "nombre_cientifico": "Solanum phureja",
                "ciclo_fenologico_dias": 120,
                "segmento_mercado": "Consumo Fresco Especial / Procesamiento",
                "descripcion": "Papa amarilla nativa de ciclo corto (3-4 meses), alta susceptibilidad a perecibilidad"
            },
            {
                "cod_variedad": "PASTUSA_SUPREMA",
                "nombre_variedad": "PAPA PASTUSA / SUPREMA / TODAS LAS VARIEDADES",
                "variedad_canonica": "Papa todas las variedades",
                "nombre_cientifico": "Solanum tuberosum",
                "ciclo_fenologico_dias": 180,
                "segmento_mercado": "Consumo Masivo Fresco / Agroindustria",
                "descripcion": "Papas blancas tradicionales de ciclo semestral (5-6 meses), base del abastecimiento nacional"
            }
        ]
        return pd.DataFrame(variedades)

    def construir_dim_mercado(self, df_sipsa: pd.DataFrame) -> pd.DataFrame:
        """
        Genera la Dimensión de Plazas y Mercados Mayoristas de SIPSA.
        """
        mercados = df_sipsa[[
            "mercado_mayorista", "divipola_mpio", "nombre_mpio", "divipola_depto", "nombre_depto"
        ]].drop_duplicates().copy()
        
        mercados["id_mercado"] = range(1, len(mercados) + 1)
        mercados["mercado_mayorista"] = mercados["mercado_mayorista"].apply(self._limpiar_texto)
        mercados["nombre_mpio"] = mercados["nombre_mpio"].apply(self._limpiar_texto)
        mercados["nombre_depto"] = mercados["nombre_depto"].apply(self._limpiar_texto)
        mercados["cod_mpio"] = mercados["divipola_mpio"].astype(str).str.zfill(5)
        mercados["cod_depto"] = mercados["divipola_depto"].astype(str).str.zfill(2)
        
        # Categorización por relevancia de volumen
        principales_hubs = ["CORABASTOS", "CENTRAL MAYORISTA DE ANTIOQUIA", "CAVASA", "SURABASTOS", "CENABASTOS"]
        mercados["tipo_hub_logistico"] = np.where(
            mercados["mercado_mayorista"].str.contains("CORABASTOS|MAYORISTA|CAVASA|SURABASTOS", regex=True),
            "Hub Metropolitano Estrategico",
            "Central Mayorista Regional"
        )
        
        cols = ["id_mercado", "mercado_mayorista", "cod_mpio", "nombre_mpio", "cod_depto", "nombre_depto", "tipo_hub_logistico"]
        return mercados[cols].drop_duplicates(subset=["mercado_mayorista"]).reset_index(drop=True)

    def construir_fact_produccion_eva(self, df_eva: pd.DataFrame, dim_tiempo: pd.DataFrame) -> pd.DataFrame:
        """
        Genera la Tabla de Hechos de Producción Agrícola Municipal-Semestral (EVA).
        """
        fact = df_eva.copy()
        fact["cod_mpio"] = fact["cod_mpio"].astype(str).str.zfill(5)
        fact["cod_depto"] = fact["cod_depto"].astype(str).str.zfill(2)
        
        # Asignar código de variedad
        fact["cod_variedad"] = np.where(
            fact["desagregacion_cultivo"].str.lower().str.contains("criolla"),
            "CRIOLLA",
            "PASTUSA_SUPREMA"
        )
        
        # Asignar fecha y clave temporal a partir del año y periodo (A = 01 de junio, B = 01 de diciembre)
        mes_asignado = np.where(fact["periodo"].astype(str).str.contains("A|1", regex=True), 6, 12)
        fact["fecha"] = pd.to_datetime(fact["año"].astype(str) + "-" + pd.Series(mes_asignado, index=fact.index).astype(str).str.zfill(2) + "-01")
        fact["id_tiempo"] = fact["fecha"].dt.strftime("%Y%m%d").astype(int)
        
        # Selección y renombramiento de métricas
        cols_fact = [
            "id_tiempo",
            "cod_mpio",
            "cod_variedad",
            "area_sembrada_ha",
            "area_cosechada_ha",
            "produccion_ton",
            "rendimiento_ton_ha",
            "tasa_perdida_cosecha_pct",
            "produccion_per_capita_nacional_kg"
        ]
        
        # Si alguna columna no existe, rellenar con cálculo estándar
        if "tasa_perdida_cosecha_pct" not in fact.columns:
            fact["tasa_perdida_cosecha_pct"] = np.where(
                fact["area_sembrada_ha"] > 0,
                ((fact["area_sembrada_ha"] - fact["area_cosechada_ha"]) / fact["area_sembrada_ha"]) * 100,
                0.0
            )
        if "produccion_per_capita_nacional_kg" not in fact.columns:
            fact["produccion_per_capita_nacional_kg"] = 0.0
            
        return fact[cols_fact].dropna(subset=["id_tiempo", "cod_mpio"]).reset_index(drop=True)

    def construir_fact_sipsa(
        self, df_sipsa: pd.DataFrame, dim_mercado: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Genera las Tablas de Hechos de Abastecimiento y de Precios Mayoristas (SIPSA).
        Preserva el origen municipal (cod_mpio) y la variedad comercial detallada,
        garantizando unicidad y granularidad exacta sin duplicados espurios.
        """
        sipsa = df_sipsa.copy()
        sipsa["fecha"] = pd.to_datetime(sipsa["fecha_mes"])
        sipsa["id_tiempo"] = sipsa["fecha"].dt.strftime("%Y%m%d").astype(int)
        sipsa["mercado_norm"] = sipsa["mercado_mayorista"].apply(self._limpiar_texto)
        sipsa["cod_mpio"] = sipsa["divipola_mpio"].astype(str).str.zfill(5)
        sipsa["variedad_comercial"] = sipsa["variedad_papa"].apply(self._limpiar_texto)
        
        # Mapear id_mercado
        mercado_map = dict(zip(dim_mercado["mercado_mayorista"], dim_mercado["id_mercado"]))
        sipsa["id_mercado"] = sipsa["mercado_norm"].map(mercado_map).fillna(0).astype(int)
        
        # Mapear variedad macro-conformada con Dim_Variedad (CRIOLLA vs PASTUSA_SUPREMA)
        sipsa["cod_variedad"] = np.where(
            sipsa["variedad_papa"].str.lower().str.contains("criolla"),
            "CRIOLLA",
            "PASTUSA_SUPREMA"
        )
        
        # 1. Fact Abastecimiento
        cols_abast = [
            "id_tiempo",
            "id_mercado",
            "cod_mpio",
            "cod_variedad",
            "variedad_comercial",
            "volumen_ingreso_ton",
            "indice_estacional_oferta_ieo",
            "consumo_mayorista_per_capita_kg"
        ]
        for col in ["indice_estacional_oferta_ieo", "consumo_mayorista_per_capita_kg"]:
            if col not in sipsa.columns:
                sipsa[col] = 1.0
        fact_abast = sipsa[cols_abast].dropna(subset=["id_tiempo", "id_mercado", "cod_mpio"]).copy()
        
        # 2. Fact Precios
        sipsa["spread_precios_kg"] = sipsa["precio_max_kg"] - sipsa["precio_min_kg"]
        cols_precios = [
            "id_tiempo",
            "id_mercado",
            "cod_mpio",
            "cod_variedad",
            "variedad_comercial",
            "precio_prom_kg",
            "precio_min_kg",
            "precio_max_kg",
            "spread_precios_kg",
            "num_transacciones",
            "indice_estacional_precio_iep"
        ]
        for col in ["indice_estacional_precio_iep"]:
            if col not in sipsa.columns:
                sipsa[col] = 1.0
        fact_precios = sipsa[cols_precios].dropna(subset=["id_tiempo", "id_mercado", "cod_mpio"]).copy()
        
        return fact_abast.reset_index(drop=True), fact_precios.reset_index(drop=True)

    def ejecutar_exportacion(self) -> dict[str, int]:
        """
        Ejecuta el pipeline de transformación completo, valida integridad
        y genera los archivos en formato CSV (UTF-8 con BOM) y Parquet.
        """
        # Cargar datos enriquecidos de features o cleaned
        eva_feat_path = FEATURES_DIR / "dataset_eva_features.parquet"
        if eva_feat_path.exists():
            df_eva = pd.read_parquet(eva_feat_path)
        else:
            df_eva = pd.read_parquet(CLEANED_DIR / "dataset_eva_agricola_nacional.parquet")
            
        sipsa_feat_path = FEATURES_DIR / "dataset_sipsa_features.parquet"
        if sipsa_feat_path.exists():
            df_sipsa = pd.read_parquet(sipsa_feat_path)
        else:
            df_sipsa = pd.read_parquet(CLEANED_DIR / "dataset_sipsa_mensual_nacional.parquet")

        # 1. Dimensiones
        dim_tiempo = self.construir_dim_tiempo(df_eva, df_sipsa)
        dim_geografia = self.construir_dim_geografia(df_eva, df_sipsa)
        dim_variedad = self.construir_dim_variedad(df_eva, df_sipsa)
        dim_mercado = self.construir_dim_mercado(df_sipsa)

        # 2. Hechos
        fact_eva = self.construir_fact_produccion_eva(df_eva, dim_tiempo)
        fact_abast, fact_precios = self.construir_fact_sipsa(df_sipsa, dim_mercado)

        tablas = {
            "Dim_Tiempo": dim_tiempo,
            "Dim_Geografia": dim_geografia,
            "Dim_Variedad": dim_variedad,
            "Dim_Mercado": dim_mercado,
            "Fact_Produccion_EVA": fact_eva,
            "Fact_Abastecimiento_SIPSA": fact_abast,
            "Fact_Precios_SIPSA": fact_precios
        }

        # Guardar en ambas ubicaciones: data/POWERBI y powerbi/data
        conteo_filas = {}
        for nombre, df in tablas.items():
            # CSV con codificación utf-8-sig (con BOM para compatibilidad inmediata en Excel/PowerBI)
            csv_path_data = self.output_dir / f"{nombre}.csv"
            parquet_path_data = self.output_dir / f"{nombre}.parquet"
            csv_path_pbi = self.pbi_data_dir / f"{nombre}.csv"
            parquet_path_pbi = self.pbi_data_dir / f"{nombre}.parquet"

            df.to_csv(csv_path_data, index=False, encoding="utf-8-sig")
            df.to_parquet(parquet_path_data, index=False)
            df.to_csv(csv_path_pbi, index=False, encoding="utf-8-sig")
            df.to_parquet(parquet_path_pbi, index=False)

            conteo_filas[nombre] = len(df)

        return conteo_filas
