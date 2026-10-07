"""
Módulo de Validación y Normalización DIVIPOLA DANE.
Garantiza tipo string y padding estricto:
- Departamento: 2 dígitos (zfill 2)
- Municipio: 5 dígitos (zfill 5)
"""

import re
from typing import Optional
import pandas as pd

from src.domain.exceptions import InvalidDivipolaCodeError


def normalizar_codigo_depto(valor) -> Optional[str]:
    """Sanitiza y normaliza un código departamental a 2 dígitos numéricos."""
    if pd.isna(valor) or valor is None:
        return None
    val_str = str(valor).strip()
    if val_str.endswith(".0"):
        val_str = val_str[:-2]
    digitos = re.sub(r"\D", "", val_str)
    if not digitos:
        return None
    codigo = digitos.zfill(2)
    if len(codigo) != 2:
        return None
    return codigo


def normalizar_codigo_mpio(valor) -> Optional[str]:
    """Sanitiza y normaliza un código municipal a 5 dígitos numéricos."""
    if pd.isna(valor) or valor is None:
        return None
    val_str = str(valor).strip()
    if val_str.endswith(".0"):
        val_str = val_str[:-2]
    digitos = re.sub(r"\D", "", val_str)
    if not digitos:
        return None
    codigo = digitos.zfill(5)
    if len(codigo) != 5:
        return None
    return codigo


def validar_serie_divipola(serie: pd.Series, longitud: int = 5) -> pd.Series:
    """Aplica la normalización vectorizada sobre una columna de Pandas."""
    if longitud == 2:
        return serie.apply(normalizar_codigo_depto)
    elif longitud == 5:
        return serie.apply(normalizar_codigo_mpio)
    else:
        raise ValueError("Longitud de DIVIPOLA soportada: 2 (Depto) o 5 (Municipio).")
