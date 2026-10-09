import json
from pathlib import Path

nb_path = Path("docs/report.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        src = "".join(cell.get('source', []))
        print(f"=== Markdown Cell {i} ===")
        print(src[:300])
        print("...\n")
