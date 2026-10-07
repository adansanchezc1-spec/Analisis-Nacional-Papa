"""
Lector Especializado para la Base Agrícola Primaria EVA (UPRA / MinAgricultura).
Lee el libro Excel oficial de Evaluaciones Agropecuarias Municipales (2019-2025),
manejando candados de lectura en Windows y extrayendo las variedades de papa.
"""

from pathlib import Path
import tempfile
import subprocess
import os
from typing import Optional
import pandas as pd
import numpy as np


class EvaReader:
    """Lector especializado y robusto para microdatos agrícolas de campo (EVA)."""

    COLUMNAS_CANONICAS = [
        "cod_depto",
        "departamento",
        "cod_mpio",
        "municipio",
        "desagregacion_cultivo",
        "cultivo",
        "ciclo_cultivo",
        "grupo_cultivo",
        "subgrupo",
        "año",
        "periodo",
        "area_sembrada_ha",
        "area_cosechada_ha",
        "produccion_ton",
        "rendimiento_ton_ha",
        "nombre_cientifico",
        "cod_cultivo",
        "estado_fisico",
    ]

    def _copiar_archivo_bloqueado(self, file_path: Path) -> Path:
        """Copia el archivo a una ubicación temporal para eludir candados de Windows/Excel."""
        temp_dir = Path(tempfile.gettempdir())
        temp_file = temp_dir / f"eva_read_copy_{os.getpid()}.xlsx"
        
        # Intentar copia con PowerShell para invocar permisos de compartición
        cmd = [
            "powershell",
            "-NoProfile",
            "-Command",
            f"Copy-Item -Path '{file_path}' -Destination '{temp_file}' -Force"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 or not temp_file.exists():
            raise IOError(f"No fue posible copiar el archivo bloqueado: {result.stderr}")
        
        return temp_file

    def read_eva_papa(self, file_path: Path) -> pd.DataFrame:
        """
        Lee la hoja BasePagina del archivo EVA, filtra exclusivamente los registros de papa,
        normaliza las categorías varietales ('PAPA CRIOLLA' y 'PAPA TODAS LAS VARIEDADES')
        y formatea llaves DIVIPOLA con padding estándar.
        """
        temp_copy: Optional[Path] = None
        ruta_lectura = file_path

        # Verificar si el archivo está bloqueado por otro proceso
        try:
            with open(file_path, "rb") as f:
                f.read(1024)
        except (PermissionError, OSError):
            temp_copy = self._copiar_archivo_bloqueado(file_path)
            ruta_lectura = temp_copy

        try:
            # BasePagina tiene 8 filas de metadatos institucionales; las cabeceras inician en fila 9 (skiprows=8)
            df = pd.read_excel(
                ruta_lectura,
                sheet_name="BasePagina",
                skiprows=8,
                usecols=list(range(18)),
                engine="openpyxl"
            )
            df.columns = self.COLUMNAS_CANONICAS
        finally:
            if temp_copy and temp_copy.exists():
                try:
                    temp_copy.unlink()
                except OSError:
                    pass

        # 1. Filtro estricto de cultivo: excluir Papaya, Malanga, etc.
        es_papa = df["cultivo"].astype(str).str.strip().str.upper() == "PAPA"
        df_papa = df[es_papa].copy()

        # 2. Normalización de desagregación cultivo
        def normalizar_variedad(val: str) -> str:
            v_upper = str(val).upper()
            if "CRIOLLA" in v_upper:
                return "PAPA CRIOLLA"
            return "PAPA TODAS LAS VARIEDADES"

        df_papa["desagregacion_cultivo"] = df_papa["desagregacion_cultivo"].apply(normalizar_variedad)

        # 3. Limpieza y formateo DIVIPOLA
        df_papa["cod_depto"] = (
            df_papa["cod_depto"]
            .astype(str)
            .str.replace("'", "", regex=False)
            .str.strip()
            .apply(lambda x: x.split(".")[0] if "." in x else x)
            .str.zfill(2)
        )
        df_papa["cod_mpio"] = (
            df_papa["cod_mpio"]
            .astype(str)
            .str.replace("'", "", regex=False)
            .str.strip()
            .apply(lambda x: x.split(".")[0] if "." in x else x)
            .str.zfill(5)
        )
        df_papa["departamento"] = df_papa["departamento"].astype(str).str.strip().str.upper()
        df_papa["municipio"] = df_papa["municipio"].astype(str).str.strip().str.upper()

        # 4. Formateo y tipado numérico
        df_papa["año"] = pd.to_numeric(df_papa["año"], errors="coerce").astype(int)
        df_papa["periodo"] = df_papa["periodo"].astype(str).str.strip().str.upper()
        for col in ["area_sembrada_ha", "area_cosechada_ha", "produccion_ton", "rendimiento_ton_ha"]:
            df_papa[col] = pd.to_numeric(df_papa[col], errors="coerce").fillna(0.0)

        # 5. Ordenamiento lógico temporal y espacial
        df_papa = df_papa.sort_values(by=["año", "periodo", "cod_depto", "cod_mpio"]).reset_index(drop=True)

        return df_papa
