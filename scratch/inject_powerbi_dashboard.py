import json
from pathlib import Path

root = Path(r"c:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando")
report_nb_path = root / "docs/report.ipynb"

# Read the HTML template
with open(root / "scratch/dashboard_component.html", "r", encoding="utf-8") as f:
    dashboard_html_raw = f.read()

# Replace the static JSON with placeholder %%PAYLOAD_JSON%%
# In dashboard_component.html, the line is: const DATA = {...};
# Let's replace the JSON object after "const DATA = " up to ";\n\n  // APPLICATION STATE"
import re
template_html = re.sub(r'const DATA = .*?;\s*// APPLICATION STATE', 'const DATA = %%PAYLOAD_JSON%%;\n\n  // APPLICATION STATE', dashboard_html_raw, flags=re.DOTALL)

# Let's write this template to docs/assets/powerbi_dashboard_template.html or embed it as a raw string in python
assets_dir = root / "docs/assets"
assets_dir.mkdir(parents=True, exist_ok=True)
template_path = assets_dir / "powerbi_dashboard_template.html"
with open(template_path, "w", encoding="utf-8") as f:
    f.write(template_html)

print(f"Saved template to {template_path} ({len(template_html)/1024:.2f} KB)")

# Now Cell 27 code:
cell_27_code = '''# ==============================================================================
# CELDA 27: TABLERO EJECUTIVO Y DRILL-DOWN INTERACTIVO TIPO POWER BI (HTML5/JS)
# ==============================================================================
import json
from pathlib import Path
from IPython.display import display, HTML

# Normalización y mapeo de variables para el payload multidimensional
def map_var_pbi(v):
    v = str(v).lower()
    if 'pastusa' in v: return 'Pastusa'
    if 'r-12' in v or 'r12' in v: return 'R-12'
    if 'criolla' in v or 'chaucha' in v: return 'Criolla'
    if 'capiro' in v or 'diacol' in v: return 'Diacol Capiro'
    if 'superior' in v: return 'Superior'
    if 'tuquerre' in v: return 'Tuquerreña'
    return 'Otras Variedades'

# Preparación de datos EVA con jerarquía Departamento -> Municipio -> Variedad -> Año
col_a_eva = [c for c in df_eva.columns if 'a' in c.lower() and 'o' in c.lower() and len(c) <= 4][0]
df_eva_temp = df_eva.copy()
df_eva_temp['var_clean'] = df_eva_temp['desagregacion_cultivo'].apply(map_var_pbi)
df_eva_temp['depto_clean'] = df_eva_temp['departamento'].astype(str).str.strip().str.title()
df_eva_temp['mpio_clean'] = df_eva_temp['municipio'].astype(str).str.strip().str.title()

eva_pbi = df_eva_temp.groupby(['depto_clean', 'mpio_clean', 'var_clean', col_a_eva]).agg({
    'produccion_ton': 'sum',
    'area_cosechada_ha': 'sum'
}).reset_index()
eva_pbi['rend'] = (eva_pbi['produccion_ton'] / eva_pbi['area_cosechada_ha'].replace(0, 1)).round(1)
eva_pbi['produccion_ton'] = eva_pbi['produccion_ton'].round(1)
eva_pbi['area_cosechada_ha'] = eva_pbi['area_cosechada_ha'].round(1)

records_eva = eva_pbi[['depto_clean', 'mpio_clean', 'var_clean', col_a_eva, 'produccion_ton', 'area_cosechada_ha', 'rend']].values.tolist()

# Preparación de datos SIPSA (Precios y Volúmenes)
col_a_sipsa = [c for c in df_sipsa.columns if 'a' in c.lower() and 'o' in c.lower() and len(c) <= 4][0]
df_sipsa_temp = df_sipsa.copy()
df_sipsa_temp['var_clean'] = df_sipsa_temp['variedad_papa'].apply(map_var_pbi)
df_sipsa_temp['depto_clean'] = df_sipsa_temp['nombre_depto'].astype(str).str.strip().str.title()

sipsa_prices = df_sipsa_temp.groupby(['depto_clean', 'var_clean', col_a_sipsa]).agg({
    'precio_prom_kg': 'mean',
    'volumen_ingreso_ton': 'sum'
}).reset_index()
sipsa_prices['precio_prom_kg'] = sipsa_prices['precio_prom_kg'].round(0).astype(int)
sipsa_prices['volumen_ingreso_ton'] = sipsa_prices['volumen_ingreso_ton'].round(1)
records_sipsa = sipsa_prices[['depto_clean', 'var_clean', col_a_sipsa, 'precio_prom_kg', 'volumen_ingreso_ton']].values.tolist()

sipsa_monthly = df_sipsa_temp.groupby(['depto_clean', col_a_sipsa, 'mes']).agg({
    'precio_prom_kg': 'mean',
    'volumen_ingreso_ton': 'sum'
}).reset_index()
sipsa_monthly['precio_prom_kg'] = sipsa_monthly['precio_prom_kg'].round(0).astype(int)
sipsa_monthly['volumen_ingreso_ton'] = sipsa_monthly['volumen_ingreso_ton'].round(1)
records_monthly = sipsa_monthly[['depto_clean', col_a_sipsa, 'mes', 'precio_prom_kg', 'volumen_ingreso_ton']].values.tolist()

pbi_payload = {
    'eva': records_eva,
    'sipsa': records_sipsa,
    'monthly': records_monthly
}
payload_json_str = json.dumps(pbi_payload, ensure_ascii=False)

# Carga de la plantilla HTML y reemplazo del payload en memoria
template_file = project_root / 'docs/assets/powerbi_dashboard_template.html'
if not template_file.exists():
    template_file = Path('docs/assets/powerbi_dashboard_template.html')

with open(template_file, 'r', encoding='utf-8') as f:
    template_html = f.read()

pbi_html = template_html.replace('%%PAYLOAD_JSON%%', payload_json_str)

# Inyección directa en el DOM de Jupyter Notebook con capacidades completas de Cross-Filtering
display(HTML(pbi_html))
print(f"[OK] Tablero interactivo Power BI cargado con éxito: {len(records_eva):,} registros EVA y {len(records_sipsa):,} registros SIPSA integrados.")
'''

with open(report_nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Update cell 27
nb['cells'][27]['source'] = [line + '\n' for line in cell_27_code.split('\n')]
nb['cells'][27]['outputs'] = []
nb['cells'][27]['execution_count'] = None

with open(report_nb_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Successfully injected Cell 27 into docs/report.ipynb!")
