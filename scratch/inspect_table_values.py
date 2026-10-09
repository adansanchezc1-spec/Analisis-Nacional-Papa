import json
import re

with open("docs/report.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for idx in [5, 9, 11, 16, 18, 23, 26]:
    cell = nb['cells'][idx]
    print(f"\n==================== CELDA {idx} ====================")
    for out in cell.get('outputs', []):
        if 'data' in out and 'text/html' in out['data']:
            html = "".join(out['data']['text/html'])
            # Quitar tags para ver solo texto y números
            clean = re.sub(r'<[^>]+>', ' ', html)
            clean = " ".join(clean.split())
            print(clean[:500] + "...")
        elif 'text' in out:
            print("".join(out['text'])[:300])
