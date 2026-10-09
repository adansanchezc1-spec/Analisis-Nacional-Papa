import json
import re

with open('docs/report.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find DATA = { ... };
match = re.search(r'const DATA = (\{.*?\});\s+const state', html, re.DOTALL)
if match:
    data_str = match.group(1)
    data = json.loads(data_str)
    eva = data['eva']
    tot_prod = sum(r[7] for r in eva)
    tot_as = sum(r[4] for r in eva)
    tot_ac = sum(r[5] for r in eva)
    avg_rend = tot_prod / tot_ac if tot_ac > 0 else 0
    avg_efect = (tot_ac / tot_as) * 100 if tot_as > 0 else 0

    print("=== POWER BI PRO PAYLOAD EN DOCS/REPORT.HTML ===")
    print(f"Producción Acumulada: {tot_prod:,.1f} ton ({tot_prod/1000:,.1f} kt)")
    print(f"Área Sembrada:       {tot_as:,.1f} ha")
    print(f"Área Cosechada:      {tot_ac:,.1f} ha")
    print(f"Rendimiento Medio:   {avg_rend:.2f} t/ha")
    print(f"Efectividad Media:   {avg_efect:.1f}%")
    print(f"Registros EVA:       {len(eva):,}")
    print(f"Registros SIPSA:     {len(data['sipsa']):,}")
else:
    print("[ERROR] No se pudo encontrar el payload en report.html")
