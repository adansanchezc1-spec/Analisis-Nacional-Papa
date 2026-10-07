"""
Servicio de Limpieza, Saneamiento Léxico y Gobernanza de Datos.
Etapa 4 de CRISP-DM: Data Cleaning.
Aplica estandarización de variedades comerciales de papa,
remoción de acentos diacríticos y desambiguación de homónimos territoriales.
"""

import re
import unicodedata
from typing import Dict, Optional
import pandas as pd

from src.infrastructure.config import CLEANED_DIR
from src.infrastructure.writers.parquet_writer import ParquetWriter


class CleaningService:
    """Orquestador de saneamiento léxico y gobernanza DAMA-BOK."""

    # Diccionario de estandarización de variedades comerciales de papa
    MAPEO_VARIEDADES_CANONICAS = {
        "PAPA PASTUSA": "PAPA PASTUSA",
        "PAPA PARDA PASTUSA": "PAPA PARDA PASTUSA",
        "PAPA R-12 NEGRA": "PAPA PARDA PASTUSA",
        "PAPA PARDA": "PAPA PARDA PASTUSA",
        "PAPA SUPREMA": "PAPA PASTUSA SUPREMA",
        "PAPA PASTUSA SUPREMA": "PAPA PASTUSA SUPREMA",
        "PAPA DIACOL CAPIRO": "PAPA CAPIRO",
        "PAPA CAPIRO": "PAPA CAPIRO",
        "PAPA R-12 ROJA": "PAPA CAPIRO",
        "PAPA CRIOLLA": "PAPA CRIOLLA COLOMBIA",
        "PAPA CRIOLLA COLOMBIA": "PAPA CRIOLLA COLOMBIA",
        "PAPA CRIOLLA LIMPIA": "PAPA CRIOLLA COLOMBIA",
        "PAPA CRIOLLA SUCIA": "PAPA CRIOLLA COLOMBIA",
        "PAPA RUBI": "PAPA RUBI",
        "PAPA TUQUERREÑA": "PAPA TUQUERREÑA",
        "PAPA PURACE": "PAPA PURACE",
        "PAPA NEVADA": "PAPA NEVADA",
        "PAPA SAN FELIX": "PAPA SAN FELIX",
        "PAPA ICA-HUILA": "PAPA ICA HUILA",
    }

    def __init__(self, df: pd.DataFrame, output_dir=CLEANED_DIR):
        self.df = df.copy()
        self.output_dir = output_dir

    @staticmethod
    def remover_acentos(texto: str) -> str:
        """Elimina acentos y tildes conservando mayúsculas limpias."""
        if not isinstance(texto, str):
            return ""
        # Descomponer caracteres con tildes
        nfkd = unicodedata.normalize("NFKD", texto)
        sin_tildes = "".join([c for c in nfkd if not unicodedata.combining(c)])
        # Quitar caracteres especiales residuales
        limpio = re.sub(r"[^A-Z0-9\s,\-\.]", "", sin_tildes.upper())
        return " ".join(limpio.split())

    def estandarizar_variedades(self, serie_variedad: pd.Series) -> pd.Series:
        """Homologa nombres de variedades a sus etiquetas canónicas comerciales."""
        def clasificar(val):
            texto = self.remover_acentos(str(val))
            for k, canonica in self.MAPEO_VARIEDADES_CANONICAS.items():
                if k in texto:
                    return canonica
            if "CRIOLLA" in texto:
                return "PAPA CRIOLLA COLOMBIA"
            if "CAPIRO" in texto:
                return "PAPA CAPIRO"
            if "PASTUSA" in texto:
                return "PAPA PASTUSA"
            return "PAPA OTRAS VARIEDADES"

        return serie_variedad.apply(clasificar)

    def ejecutar_limpieza(self) -> pd.DataFrame:
        """Aplica la batería completa de transformaciones de limpieza."""
        df_clean = self.df.copy()

        # 1. Limpieza de texto en atributos categóricos
        for col in ["nombre_depto", "nombre_mpio", "mercado_mayorista"]:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].apply(self.remover_acentos)

        # 2. Homologación de variedades comerciales de papa
        if "variedad_papa" in df_clean.columns:
            df_clean["variedad_papa_original"] = df_clean["variedad_papa"]
            df_clean["variedad_papa"] = self.estandarizar_variedades(df_clean["variedad_papa"])

        # 3. Desambiguación de homónimos territoriales comunes
        # La Unión (05400 Antioquia vs 52399 Nariño vs 76400 Valle)
        if "nombre_mpio" in df_clean.columns and "divipola_depto" in df_clean.columns:
            mask_la_union = df_clean["nombre_mpio"] == "LA UNION"
            df_clean.loc[mask_la_union & (df_clean["divipola_depto"] == "05"), "nombre_mpio"] = "LA UNION (ANT)"
            df_clean.loc[mask_la_union & (df_clean["divipola_depto"] == "52"), "nombre_mpio"] = "LA UNION (NAR)"
            df_clean.loc[mask_la_union & (df_clean["divipola_depto"] == "76"), "nombre_mpio"] = "LA UNION (VAL)"

        # 4. Persistencia en la capa CLEANED
        out_parquet = self.output_dir / "dataset_sipsa_mensual_limpio.parquet"
        ParquetWriter.write(df_clean, out_parquet)

        return df_clean
