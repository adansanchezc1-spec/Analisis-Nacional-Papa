import json
from pathlib import Path

nb_path = Path("docs/report.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

print(f"Total cells: {len(nb['cells'])}")
for i, cell in enumerate(nb['cells']):
    ctype = cell['cell_type']
    src = "".join(cell.get('source', []))
    first_lines = src.strip().split("\n")[:2]
    preview = " | ".join(first_lines) if first_lines else "EMPTY"
    print(f"Cell {i:2d} [{ctype:8s}]: {preview[:100]}")
