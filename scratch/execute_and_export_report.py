import os
import sys
import json
import subprocess
from pathlib import Path
import nbformat
from nbclient import NotebookClient

def execute_and_export():
    root = Path(r"c:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando")
    nb_path = root / "docs" / "report.ipynb"
    html_path = root / "docs" / "report.html"
    
    print(f"[1/3] Leyendo notebook: {nb_path}...")
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
        
    print("[2/3] Ejecutando celdas con el kernel 'analisispapa' (.venv)...")
    client = NotebookClient(
        nb,
        timeout=600,
        kernel_name="analisispapa",
        resources={'metadata': {'path': str(root)}}
    )
    
    try:
        client.execute()
        print(" -> Todas las celdas se ejecutaron con éxito.")
    except Exception as e:
        print(f" [!] Error ejecutando notebook: {e}")
        # Guardar estado parcial si es posible
        with open(nb_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        raise e
        
    print(f" -> Guardando notebook actualizado: {nb_path}...")
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
        
    print(f"[3/3] Exportando a HTML: {html_path}...")
    cmd = [
        "python", "-m", "nbconvert",
        "--to", "html",
        str(nb_path),
        "--output", "report.html",
        "--output-dir", str(root / "docs")
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(root))
    print("STDOUT:", res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)
        
    if html_path.exists():
        size_mb = html_path.stat().st_size / (1024 * 1024)
        print(f"[OK] {html_path} generado exitosamente! Tamaño: {size_mb:.2f} MB")
    else:
        print("[ERROR] El archivo report.html no fue generado.")

if __name__ == "__main__":
    execute_and_export()
