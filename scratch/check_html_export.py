with open('docs/report.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = [
    'Área Sembrada', 'Área Cosechada', 'Efectividad (%)',
    'Ciclo Fenológico', 'Solanum phureja', 'Solanum tuberosum',
    'Papa Criolla', 'Papa Superior', 'Papa Diacol Capiro', 'Papa Única',
    'Papa Parda Pastusa', 'Papa Suprema', 'Papa R-12', 'Papa Betina',
    'Papa Rubí', 'Papa Nevada', 'Papa Sabanera', 'Papa Morasurco',
    'POWER BI PRO', 'Drill-Down Activo'
]

print("=== VERIFICACIÓN EN DOCS/REPORT.HTML ===")
for chk in checks:
    print(f"[{'OK' if chk in html else 'FAIL'}] {chk}")
