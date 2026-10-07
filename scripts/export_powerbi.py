"""
Script CLI para ejecutar la exportación dimensional a Power BI.
"""
import sys
from pathlib import Path

# Añadir raíz al sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.application.powerbi_export_service import PowerBIExportService

def main():
    print("=== INICIANDO EXPORTACIÓN DIMENSIONAL POWER BI (KIMBALL STAR SCHEMA) ===")
    service = PowerBIExportService()
    conteo = service.ejecutar_exportacion()
    
    print("\nTablas dimensionales generadas exitosamente:")
    for tabla, filas in conteo.items():
        print(f"  • {tabla:<30}: {filas:>10,} registros")
    
    print(f"\nArchivos exportados en:")
    print(f"  - {service.output_dir}")
    print(f"  - {service.pbi_data_dir}")

if __name__ == "__main__":
    main()
