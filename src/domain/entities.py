"""
Módulo de Entidades de Dominio.
Contiene dataclasses inmutables y estructuras puras del negocio agropecuario.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass(frozen=True)
class DivipolaTerritory:
    """Entidad territorial oficial DANE."""
    codigo_depto: str
    nombre_depto: str
    codigo_mpio: str
    nombre_mpio: str

    def __post_init__(self):
        if len(self.codigo_depto) != 2 or not self.codigo_depto.isdigit():
            raise ValueError(f"Código de departamento inválido: {self.codigo_depto}. Debe tener 2 dígitos.")
        if len(self.codigo_mpio) != 5 or not self.codigo_mpio.isdigit():
            raise ValueError(f"Código de municipio inválido: {self.codigo_mpio}. Debe tener 5 dígitos.")


@dataclass(frozen=True)
class MonthlyMarketRecord:
    """
    Registro canónico consolidado a nivel MENSUAL del Dataset Único SIPSA.
    Representa la unidad básica de análisis en el eje dimensional temporal.
    """
    fecha_mes: date            # Primer día del mes analizado (YYYY-MM-01)
    año: int                   # Año calendario (2019 - 2025)
    mes: int                   # Mes calendario (1 - 12)
    divipola_depto: str        # Código de 2 dígitos del departamento productor
    nombre_depto: str          # Nombre oficial del departamento productor
    divipola_mpio: str         # Código de 5 dígitos del municipio productor
    nombre_mpio: str           # Nombre oficial del municipio productor
    mercado_mayorista: str     # Central mayorista de destino
    divipola_mercado: str      # Código DIVIPOLA de 5 dígitos del mercado destino
    alimento: str              # Canónico: 'PAPA'
    variedad_papa: str         # Variedad comercial (Pastusa, Capiro, Criolla, etc.)
    volumen_ingreso_ton: float # Volumen agregado ingresado en el mes (toneladas)
    precio_prom_kg: float      # Precio promedio ponderado mensual ($/kg) - INVARIANTE: > 0
    precio_min_kg: float       # Precio mínimo observado en el mes ($/kg)
    precio_max_kg: float       # Precio máximo observado en el mes ($/kg)
    num_transacciones: int     # Conteo de registros transaccionales agregados

    def __post_init__(self):
        if self.precio_prom_kg is None or self.precio_prom_kg <= 0:
            raise ValueError("Regla de Oro violada: precio_prom_kg no puede ser nulo ni <= 0.")
        if self.volumen_ingreso_ton < 0:
            raise ValueError("volumen_ingreso_ton no puede ser negativo.")
        if not (self.precio_min_kg <= self.precio_prom_kg <= self.precio_max_kg):
            raise ValueError(
                f"Incoherencia física: min ({self.precio_min_kg}) <= prom ({self.precio_prom_kg}) <= max ({self.precio_max_kg})"
            )


@dataclass(frozen=True)
class QualityAuditReport:
    """Reporte formal de calidad de datos bajo DAMA-BOK."""
    total_registros_procesados: int
    total_registros_validos: int
    total_precios_nulos_descartados: int
    total_inconsistencias_divipola: int
    pct_completitud_precios: float
    fecha_auditoria: str
