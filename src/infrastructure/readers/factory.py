"""
Fábrica de Lectores de Archivos Políglotas (Patrón Factory Method).
Desacopla la extensión física del archivo de su estrategia de lectura.
"""

from pathlib import Path
from src.infrastructure.readers.base_reader import BaseReader
from src.infrastructure.readers.csv_reader import CsvReader
from src.infrastructure.readers.stata_reader import StataReader, SpssReader, SasReader


class FileReaderFactory:
    """Factory para instanciar lectores de archivos basados en extensión."""

    @staticmethod
    def get_reader(file_path: Path) -> BaseReader:
        suffix = file_path.suffix.lower()
        if suffix in [".csv", ".txt"]:
            return CsvReader()
        elif suffix == ".dta":
            return StataReader()
        elif suffix == ".sav":
            return SpssReader()
        elif suffix in [".sas7bdat", ".sas"]:
            return SasReader()
        else:
            raise ValueError(f"Formato no soportado por la fábrica: {suffix} en {file_path}")
