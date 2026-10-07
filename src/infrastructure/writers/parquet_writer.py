"""
Escritor y Serializador de Datos Columnar Apache Parquet.
Optimiza compresión (Snappy), tipos de datos y preserva metadatos.
"""

from pathlib import Path
from typing import Optional, List
import pandas as pd


class ParquetWriter:
    """Manejador de persistencia columnar Parquet para capas Medallion."""

    @staticmethod
    def write(
        df: pd.DataFrame,
        output_path: Path,
        partition_cols: Optional[List[str]] = None,
        compression: str = "snappy"
    ) -> Path:
        """Escribe un DataFrame en formato Parquet asegurando la creación del directorio padre."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(
            output_path,
            index=False,
            partition_cols=partition_cols,
            compression=compression,
            engine="pyarrow"
        )
        return output_path
