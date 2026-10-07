"""
Interfaz Base para Lectores de Archivos Políglotas.
Patrón: Factory Method / Strategy.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator, Optional
import pandas as pd


class BaseReader(ABC):
    """Clase base abstracta para lectores de microdatos SIPSA."""

    @abstractmethod
    def read(self, file_path: Path, chunksize: Optional[int] = None) -> Iterator[pd.DataFrame]:
        """
        Lee el archivo especificado en bloques (chunks) o como un único generador.
        Retorna un iterador de DataFrames para optimización estricta de memoria RAM.
        """
        pass
