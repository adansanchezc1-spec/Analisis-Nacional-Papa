"""
Lector de Archivos CSV y Delimitados por Texto.
Soporta delimitadores variables (';', ',') y codificaciones (latin1, utf-8, utf-8-sig).
"""

from pathlib import Path
from typing import Iterator, Optional
import pandas as pd

from src.infrastructure.readers.base_reader import BaseReader


class CsvReader(BaseReader):
    """Implementación de lector para archivos de texto plano CSV."""

    def __init__(self, delimiter: Optional[str] = None, encoding: Optional[str] = None):
        self.delimiter = delimiter
        self.encoding = encoding

    def _detect_delimiter_and_encoding(self, file_path: Path) -> tuple[str, str]:
        """Detecta de forma heurística el delimitador y codificación más adecuados."""
        encodings_to_try = ["utf-8-sig", "latin1", "utf-8", "cp1252"]
        if self.encoding:
            encodings_to_try = [self.encoding] + encodings_to_try

        for enc in encodings_to_try:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    first_line = f.readline()
                    if ";" in first_line:
                        return ";", enc
                    elif "," in first_line:
                        return ",", enc
            except UnicodeDecodeError:
                continue
        return ";", "latin1"

    def read(self, file_path: Path, chunksize: Optional[int] = 100_000) -> Iterator[pd.DataFrame]:
        sep, enc = self._detect_delimiter_and_encoding(file_path)
        if self.delimiter:
            sep = self.delimiter

        if chunksize:
            reader = pd.read_csv(
                file_path,
                sep=sep,
                encoding=enc,
                chunksize=chunksize,
                low_memory=False,
                on_bad_lines="skip"
            )
            for chunk in reader:
                yield chunk
        else:
            df = pd.read_csv(
                file_path,
                sep=sep,
                encoding=enc,
                low_memory=False,
                on_bad_lines="skip"
            )
            yield df
