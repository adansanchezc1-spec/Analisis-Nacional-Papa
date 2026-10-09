import json

with open("docs/report.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

print("=== AUDITORIA DE CONTENIDO DEL INFORME (docs/report.ipynb) ===")
for i, cell in enumerate(nb['cells']):
    src = "".join(cell['source'])
    # Buscar palabras clave o indicadores sospechosos
    for kw in ["kg/hab", "Efectividad", "Pérdida", "precio", "rendimiento", "HHI", "Villapinzón", "Tausa", "Criolla", "Pastusa"]:
        if kw.lower() in src.lower():
            # Encontrar frases relevantes
            lines = [l.strip() for l in src.split("\n") if kw.lower() in l.lower() and not l.strip().startswith("#")]
            if lines:
                print(f"\n[Celda {i} ({cell['cell_type']}) - KW: {kw}]:")
                for l in lines[:3]:
                    print(f"  {l[:110]}")
                break
