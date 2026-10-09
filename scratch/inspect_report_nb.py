import json

with open("docs/report.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Total celdas: {len(nb['cells'])}")
for i, cell in enumerate(nb['cells']):
    ctype = cell['cell_type']
    src = "".join(cell['source'])
    title = src.strip().split("\n")[0][:80] if src.strip() else "(vacia)"
    print(f"Celda {i:2d} [{ctype:8s}]: {title}")
