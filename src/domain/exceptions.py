"""
Módulo de Excepciones de Dominio.
Reglas puras de negocio del mercado agropecuario e invariantes de datos.
"""


class DomainError(Exception):
    """Excepción base para violaciones de reglas de dominio."""
    pass


class PriceNullViolationError(DomainError):
    """Violación de la invariante estricta: Ningún precio puede ser nulo o menor o igual a cero."""
    pass


class PhysicalRangeViolationError(DomainError):
    """Violación de coherencia física en cotizaciones (ej. min > prom o prom > max)."""
    pass


class InvalidDivipolaCodeError(DomainError):
    """Violación de formato o longitud en códigos territoriales DIVIPOLA DANE."""
    pass


class SchemaDriftUnresolvedError(DomainError):
    """Error al intentar armonizar una cabecera que no coincide con ninguna variante conocida."""
    pass
