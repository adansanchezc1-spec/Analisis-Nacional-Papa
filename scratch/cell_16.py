# ==============================================================================
# TABLA B: BALANCE PLURIANUAL DE SUPERFICIE, SIEMBRA VS COSECHA Y VARIEDAD (EVA)
# ==============================================================================
col_a = [c for c in df_eva.columns if 'a' in c.lower() and 'o' in c.lower() and len(c) <= 4][0]
eva_var = df_eva.groupby(['desagregacion_cultivo']).agg(
    area_sembrada_ha=('area_sembrada_ha', 'sum'),
    area_cosechada_ha=('area_cosechada_ha', 'sum'),
    produccion_ton=('produccion_ton', 'sum'),
    rendimiento_medio=('rendimiento_ton_ha', 'mean'),
    rendimiento_std=('rendimiento_ton_ha', 'std')
).reset_index()

eva_var['perdida_ha'] = eva_var['area_sembrada_ha'] - eva_var['area_cosechada_ha']
eva_var['efectividad_pct'] = (eva_var['area_cosechada_ha'] / eva_var['area_sembrada_ha']) * 100.0
eva_var['cuota_prod_pct'] = (eva_var['produccion_ton'] / df_eva['produccion_ton'].sum()) * 100.0

table_b_html = '''
<div style="margin: 20px 0; font-family: 'Segoe UI', Tahoma, sans-serif; color: #000000;">
    <div style="font-weight: 800; font-size: 14px; color: #000000; margin-bottom: 8px;">
        Tabla B. Balance integral de siembra, cosecha, tasa de efectividad y productividad agronómica (EVA 2019–2025)
    </div>
    <table style="width: 100%; border-collapse: collapse; font-size: 13px; border: 1.5px solid #000000; color: #000000;">
        <thead>
            <tr style="background: #edf2f7; color: #000000; text-align: right; border-bottom: 2px solid #000000;">
                <th style="padding: 9px 12px; text-align: left; color: #000000; font-weight: 800;">Variedad / Grupo EVA</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Área Sembrada (ha)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Área Cosechada (ha)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Pérdida (ha)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Efectividad (%)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Producción (Ton)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Rendimiento (t/ha)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Cuota (%)</th>
            </tr>
        </thead>
        <tbody>
'''

for _, r in eva_var.iterrows():
    table_b_html += f'''
            <tr style="border-bottom: 1px solid #cbd5e0; text-align: right; color: #000000;">
                <td style="padding: 8px 12px; text-align: left; font-weight: 700; color: #000000;">{r['desagregacion_cultivo']}</td>
                <td style="padding: 8px 12px; color: #000000;">{r['area_sembrada_ha']:,.0f} ha</td>
                <td style="padding: 8px 12px; font-weight: 700; color: #000000;">{r['area_cosechada_ha']:,.0f} ha</td>
                <td style="padding: 8px 12px; color: #dc2626; font-weight: 700;">-{r['perdida_ha']:,.0f} ha</td>
                <td style="padding: 8px 12px; font-weight: 800; color: {'#16a34a' if r['efectividad_pct'] >= 95 else '#ea580c'};">{r['efectividad_pct']:.2f}%</td>
                <td style="padding: 8px 12px; font-weight: 700; color: #000000;">{r['produccion_ton']:,.0f} t</td>
                <td style="padding: 8px 12px; font-weight: 800; color: #000000;">{r['rendimiento_medio']:.2f} ± {r['rendimiento_std']:.1f}</td>
                <td style="padding: 8px 12px; font-weight: 800; color: #000000;">{r['cuota_prod_pct']:.2f}%</td>
            </tr>'''

table_b_html += '''
        </tbody>
    </table>
    <div style="font-size: 11.5px; font-style: italic; color: #000000; margin-top: 8px; font-weight: 500;">
        Nota. Elaboración propia a partir de datos de Evaluaciones Agropecuarias Municipales - EVA (UPRA, 2025). La brecha entre siembra y cosecha refleja una pérdida acumulada de más de 62,000 hectáreas en el periodo 2019–2025.
    </div>
</div>
'''
display(HTML(table_b_html))

