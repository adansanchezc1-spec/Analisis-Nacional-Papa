import json
from pathlib import Path

nb_path = Path('docs/report.ipynb')
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

old_source = "".join(nb['cells'][27]['source'])
target_line = "pbi_html = template_html.replace('%%PAYLOAD_JSON%%', payload_json_str)"
replacement = """if '/* %%PAYLOAD_JSON%% */ null' in template_html:
    pbi_html = template_html.replace('/* %%PAYLOAD_JSON%% */ null', payload_json_str)
else:
    pbi_html = template_html.replace('%%PAYLOAD_JSON%%', payload_json_str)"""

if target_line in old_source:
    new_source = old_source.replace(target_line, replacement)
    nb['cells'][27]['source'] = [l + '\n' for l in new_source.splitlines()]

template_path = Path('docs/assets/powerbi_dashboard_template.html')
payload_path = Path('scratch/dashboard_enhanced_payload.json')
with open(template_path, 'r', encoding='utf-8') as f:
    template_html = f.read()
with open(payload_path, 'r', encoding='utf-8') as f:
    payload_json = f.read()

if '/* %%PAYLOAD_JSON%% */ null' in template_html:
    pbi_html = template_html.replace('/* %%PAYLOAD_JSON%% */ null', payload_json)
else:
    pbi_html = template_html.replace('%%PAYLOAD_JSON%%', payload_json)

for out in nb['cells'][27].get('outputs', []):
    if out.get('output_type') == 'display_data' and 'text/html' in out.get('data', {}):
        out['data']['text/html'] = [pbi_html]

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('[OK] Updated Cell 27 in docs/report.ipynb!')
