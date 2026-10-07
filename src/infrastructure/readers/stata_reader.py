"""
Lectores de Formatos Binarios Estadísticos: Stata (.dta), SPSS (.sav) y SAS (.sas7bdat).
Utiliza pyreadstat y pandas para lectura optimizada.
"""

from pathlib import Path
from typing import Iterator, Optional
import pandas as pd

from src.infrastructure.readers.base_reader import BaseReader


class StataReader(BaseReader):
    """Lector para archivos Stata (.dta)."""

    def read(self, file_path: Path, chunksize: Optional[int] = 100_000) -> Iterator[pd.DataFrame]:
        try:
            if chunksize:
                reader = pd.read_stata(file_path, chunksize=chunksize, convert_categoricals=False)
                for chunk in reader:
                    yield chunk
            else:
                yield pd.read_stata(file_path, convert_categoricals=False)
        except Exception:
            # Fallback a pyreadstat
            import pyreadstat
            df, _ = pyreadstat.read_dta(str(file_path))
            yield df


class SpssReader(BaseReader):
    """Lector para archivos SPSS (.sav)."""

    def read(self, file_path: Path, chunksize: Optional[int] = None) -> Iterator[pd.DataFrame]:
        import pyreadstat
        df, _ = pyreadstat.read_sav(str(file_path))
        yield df


class SasReader(BaseReader):
    """Lector para archivos SAS (.sas7bdat)."""

    def read(self, file_path: Path, chunksize: Optional[int] = 100_000) -> Iterator[pd.DataFrame]:
        try:
            if chunksize:
                reader = pd.read_sas(file_path, chunksize=chunksize, format="sas7bdat", encoding="latin1")
                for chunk in reader:
                    yield chunk
            else:
                yield pd.read_sas(file_path, format="sas7bdat", encoding="latin1")
        except Exception:
            import pyreadstat
            df, _ = pyreadstat.read_sas7bdat(str(file_path))
            yield df
