import json
import re

with open("docs/report.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

print("=== REPORTE DE CELDAS DE DOCS/REPORT.IPYNB ===")
for i, cell in enumerate(nb['cells']):
    ctype = cell['cell_type']
    if ctype == 'markdown':
        txt = "".join(cell['source'])
        headers = [line.strip() for line in txt.split("\n") if line.strip().startswith("#") or "<h" in line or "<strong" in line or "<b" in line]
        print(f"\n[Celda {i} - Markdown]:")
        for h in headers[:4]:
            print(f"  {h[:120]}")
    elif ctype == 'code':
        txt = "".join(cell['source'])
        first_lines = [line.strip() for line in txt.split("\n") if line.strip() and not line.strip().startswith("#")]
        print(f"\n[Celda {i} - Code]:")
        for l in first_lines[:2]:
            print(f"  {l[:100]}")
        outputs = cell.get('outputs', [])
        for out in outputs:
            if 'text' in out:
                lines = "".join(out['text']).split("\n")
                print(f"  OUTPUT text: {lines[0][:100]}")
            if 'data' in out:
                if 'text/html' in out['data']:
                    html_snippet = "".join(out['data']['text/html'])
                    titles = re.findall(r'<div[^>]*font-weight:\s*800[^>]*>(.*?)</div>', html_snippet, re.DOTALL)
                    if not titles:
                        titles = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html_snippet, re.DOTALL)
                    if titles:
                        print(f"  OUTPUT HTML: {titles[0].strip()[:100]}")
                    else:
                        print(f"  OUTPUT HTML snippet: {html_snippet[:80].strip()}")
