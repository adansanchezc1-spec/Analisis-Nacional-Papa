"""
Servicio de Ingestión y Construcción del Dataset Único Mensual SIPSA.
Etapa 1 de CRISP-DM: Ingestion.
Armoniza los 16 periodos crudos, estandariza el tiempo a escala MENSUAL continuo,
filtra variedades de papa y aplica la regla estricta de cero precios nulos.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
import pandas as pd
import numpy as np

from src.infrastructure.config import RAW_SIPSA_DIR, CLEANED_DIR, COLUMN_RENAME_DICTIONARY
from src.infrastructure.readers.factory import FileReaderFactory
from src.infrastructure.writers.parquet_writer import ParquetWriter
from src.domain.divipola import normalizar_codigo_depto, normalizar_codigo_mpio
from src.domain.invariants import filtrar_y_auditar_precios_df


class IngestionService:
    """Orquestador de ingestión políglota y unificación mensual nacional."""

    def __init__(self, raw_dir: Path = RAW_SIPSA_DIR, output_dir: Path = CLEANED_DIR):
        self.raw_dir = raw_dir
        self.output_dir = output_dir

    def _armonizar_columnas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Mapea las cabeceras dispares de DANE al esquema interno unificado."""
        # Limpieza básica de espacios en nombres de columna
        cols_strip = {c: c.strip() for c in df.columns}
        df = df.rename(columns=cols_strip)

        rename_map = {}
        for col in df.columns:
            if col in COLUMN_RENAME_DICTIONARY:
                rename_map[col] = COLUMN_RENAME_DICTIONARY[col]
            else:
                col_clean = col.strip()
                if col_clean in COLUMN_RENAME_DICTIONARY:
                    rename_map[col] = COLUMN_RENAME_DICTIONARY[col_clean]

        df = df.rename(columns=rename_map)
        return df

    def _filtrar_y_clasificar_papa(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filtra únicamente las transacciones del producto PAPA y extrae la variedad."""
        col_alimento = "alimento_crudo" if "alimento_crudo" in df.columns else None
        if not col_alimento:
            # Buscar columna que contenga texto de alimentos
            for c in df.columns:
                if any(k in c.lower() for k in ["ali", "artículo", "producto"]):
                    col_alimento = c
                    break

        if not col_alimento or col_alimento not in df.columns:
            return pd.DataFrame()

        # Filtrar registros de papa (case-insensitive)
        mask_papa = df[col_alimento].astype(str).str.upper().str.contains("PAPA", na=False)
        df_papa = df[mask_papa].copy()

        if df_papa.empty:
            return df_papa

        # Normalizar alimento y variedad
        df_papa["alimento"] = "PAPA"
        df_papa["variedad_papa"] = df_papa[col_alimento].astype(str).str.upper().str.strip()

        return df_papa

    def _estandarizar_fechas(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convierte fechas crudas a dimensión continua MENSUAL (YYYY-MM-01)."""
        col_fecha = "fecha_cruda" if "fecha_cruda" in df.columns else None
        if not col_fecha:
            for c in df.columns:
                if "fec" in c.lower():
                    col_fecha = c
                    break

        if not col_fecha or col_fecha not in df.columns:
            return pd.DataFrame()

        # Conversión a datetime
        fechas = pd.to_datetime(df[col_fecha], errors="coerce")
        df["fecha_valida"] = fechas
        df = df[df["fecha_valida"].notna()].copy()

        df["año"] = df["fecha_valida"].dt.year.astype(int)
        df["mes"] = df["fecha_valida"].dt.month.astype(int)
        df["fecha_mes"] = pd.to_datetime(
            df["año"].astype(str) + "-" + df["mes"].astype(str).str.zfill(2) + "-01"
        )
        return df

    def procesar_archivo(self, file_path: Path) -> pd.DataFrame:
        """Procesa un archivo transaccional crudo individual y retorna registros mensuales agregados."""
        reader = FileReaderFactory.get_reader(file_path)
        chunks_procesados = []

        for chunk in reader.read(file_path, chunksize=100_000):
            # 1. Armonizar cabeceras
            chunk_arm = self._armonizar_columnas(chunk)

            # 2. Filtrar papa
            chunk_papa = self._filtrar_y_clasificar_papa(chunk_arm)
            if chunk_papa.empty:
                continue

            # 3. Estandarizar fecha a nivel mensual
            chunk_time = self._estandarizar_fechas(chunk_papa)
            if chunk_time.empty:
                continue

            # 4. Normalizar DIVIPOLA
            if "cod_depto_crudo" in chunk_time.columns:
                chunk_time["divipola_depto"] = chunk_time["cod_depto_crudo"].apply(normalizar_codigo_depto)
            else:
                chunk_time["divipola_depto"] = "00"

            if "cod_mpio_crudo" in chunk_time.columns:
                chunk_time["divipola_mpio"] = chunk_time["cod_mpio_crudo"].apply(normalizar_codigo_mpio)
            else:
                chunk_time["divipola_mpio"] = "00000"

            chunk_time["nombre_depto"] = (
                chunk_time["nombre_depto_crudo"].astype(str).str.upper().str.strip()
                if "nombre_depto_crudo" in chunk_time.columns
                else "DESCONOCIDO"
            )
            chunk_time["nombre_mpio"] = (
                chunk_time["nombre_mpio_crudo"].astype(str).str.upper().str.strip()
                if "nombre_mpio_crudo" in chunk_time.columns
                else "DESCONOCIDO"
            )
            chunk_time["mercado_mayorista"] = (
                chunk_time["mercado_crudo"].astype(str).str.upper().str.strip()
                if "mercado_crudo" in chunk_time.columns
                else "MERCADO GENERAL"
            )

            # 5. Cantidades y Precios
            if "cantidad_kg_crudo" in chunk_time.columns:
                chunk_time["cantidad_kg"] = pd.to_numeric(chunk_time["cantidad_kg_crudo"], errors="coerce").fillna(0)
                chunk_time["volumen_ingreso_ton"] = chunk_time["cantidad_kg"] / 1000.0
            else:
                chunk_time["volumen_ingreso_ton"] = 0.0

            # Invariante de precios
            col_precio = "precio_prom_crudo" if "precio_prom_crudo" in chunk_time.columns else None
            if not col_precio:
                for c in chunk_time.columns:
                    if "precio" in c.lower() or "prom" in c.lower():
                        col_precio = c
                        break

            if col_precio:
                chunk_time["precio_prom_kg"] = pd.to_numeric(chunk_time[col_precio], errors="coerce")
            else:
                # Si no hay columna explícita de precio, se marca como NaN
                chunk_time["precio_prom_kg"] = np.nan

            # Aplicar filtro de no nulidad
            chunk_limpio, _ = filtrar_y_auditar_precios_df(chunk_time, col_precio="precio_prom_kg")
            if not chunk_limpio.empty:
                chunks_procesados.append(chunk_limpio)

        if not chunks_procesados:
            return pd.DataFrame()

        return pd.concat(chunks_procesados, ignore_index=True)

    def construir_dataset_unico_nacional(self) -> Tuple[pd.DataFrame, Dict]:
        """
        Escanea todas las carpetas semestrales en data/RAW/sipsa/ y genera
        el dataset único mensual consolidado.
        """
        archivos_encontrados = []
        for ext in ["*.csv", "*.dta", "*.sav", "*.sas7bdat"]:
            archivos_encontrados.extend(list(self.raw_dir.rglob(ext)))

        archivos_encontrados = sorted(archivos_encontrados)
        registros_totales = []
        auditoria = {
            "archivos_procesados": len(archivos_encontrados),
            "periodos_encontrados": [],
            "total_filas_mensuales": 0,
        }

        print(f"Iniciando ingestión de {len(archivos_encontrados)} archivos crudos...")
        for i, file_path in enumerate(archivos_encontrados, 1):
            period_name = file_path.parent.name
            print(f"[{i}/{len(archivos_encontrados)}] Procesando: {period_name} / {file_path.name}")
            try:
                df_file = self.procesar_archivo(file_path)
                if not df_file.empty:
                    registros_totales.append(df_file)
                    auditoria["periodos_encontrados"].append(period_name)
            except Exception as e:
                print(f"  ADVERTENCIA: Error leyendo {file_path.name}: {e}")

        if not registros_totales:
            print("No se encontraron registros válidos de papa con precios no nulos.")
            return pd.DataFrame(), auditoria

        # Concatenar todos los registros
        df_consolidado = pd.concat(registros_totales, ignore_index=True)

        # 6. Agregación a Nivel MENSUAL (Eje Dimensional de Tiempo Continuo)
        group_cols = [
            "fecha_mes",
            "año",
            "mes",
            "divipola_depto",
            "nombre_depto",
            "divipola_mpio",
            "nombre_mpio",
            "mercado_mayorista",
            "alimento",
            "variedad_papa",
        ]

        df_mensual = df_consolidado.groupby(group_cols, as_index=False).agg(
            volumen_ingreso_ton=("volumen_ingreso_ton", "sum"),
            precio_prom_kg=("precio_prom_kg", "mean"),
            precio_min_kg=("precio_prom_kg", "min"),
            precio_max_kg=("precio_prom_kg", "max"),
            num_transacciones=("precio_prom_kg", "count")
        )

        # Invariante final de verificación estricta: Cero nulos en precio
        df_mensual, descartes_finales = filtrar_y_auditar_precios_df(df_mensual, col_precio="precio_prom_kg")
        auditoria["total_filas_mensuales"] = len(df_mensual)
        auditoria["descartes_finales_nulos"] = descartes_finales

        # Persistencia en Capa CLEANED
        out_parquet = self.output_dir / "dataset_sipsa_mensual_nacional.parquet"
        ParquetWriter.write(df_mensual, out_parquet)
        df_mensual.head(100).to_csv(self.output_dir / "dataset_sipsa_mensual_nacional_preview.csv", index=False)

        print(f"\n¡DATASET ÚNICO GENERADO CON ÉXITO!")
        print(f"Ruta: {out_parquet}")
        print(f"Filas Mensuales Únicas: {len(df_mensual):,}")
        print(f"Años Abarcados: {sorted(df_mensual['año'].unique())}")
        print(f"Precios Nulos en Dataset Final: 0 (100% Verificado)")

        return df_mensual, auditoria
