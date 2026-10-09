# ==============================================================================
# TABLA 1: BALANCE DE OFERTA Y DEMANDA APARENTE MULTIANUAL (2019-2025) - TEXTO NEGRO
# ==============================================================================
trade_stats = {
    2019: {'imp': 58400, 'exp': 2100},
    2020: {'imp': 49200, 'exp': 1800},
    2021: {'imp': 55100, 'exp': 2400},
    2022: {'imp': 68300, 'exp': 3100},
    2023: {'imp': 74500, 'exp': 3800},
    2024: {'imp': 71200, 'exp': 4200},
    2025: {'imp': 73800, 'exp': 4500},
}

balance_data = []
for anio in sorted(df_eva_anual['año'].unique()):
    prod = float(df_eva_anual[df_eva_anual['año'] == anio]['produccion_ton'].values[0])
    imp = trade_stats.get(int(anio), {}).get('imp', 60000)
    exp = trade_stats.get(int(anio), {}).get('exp', 3000)
    dem_ap = prod + imp - exp
    pob = FeaturesService.POBLACION_NACIONAL_DANE.get(int(anio), {}).get('total', 51000000)
    cpc_kg = (dem_ap * 1000.0) / pob
    balance_data.append({
        'año': int(anio),
        'produccion_ton': prod,
        'importaciones_ton': imp,
        'exportaciones_ton': exp,
        'demanda_aparente_ton': dem_ap,
        'poblacion_dane': pob,
        'consumo_per_capita_kg': cpc_kg
    })

df_balance = pd.DataFrame(balance_data)

table_html = '''
<div style="margin: 20px 0; font-family: 'Segoe UI', Tahoma, sans-serif; color: #000000;">
    <div style="font-weight: 800; font-size: 14px; color: #000000; margin-bottom: 8px;">
        Tabla 1. Balance macroeconómico de oferta, comercio exterior y demanda aparente de papa en Colombia (2019–2025)
    </div>
    <table style="width: 100%; border-collapse: collapse; font-size: 13px; border: 1.5px solid #000000; color: #000000;">
        <thead>
            <tr style="background: #edf2f7; color: #000000; text-align: right; border-bottom: 2px solid #000000;">
                <th style="padding: 9px 12px; text-align: center; color: #000000; font-weight: 800;">Año</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Producción EVA (Ton)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Importaciones (Ton)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Exportaciones (Ton)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Demanda Aparente (Ton)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Población DANE</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Consumo Per Cápita (kg/hab/año)</th>
            </tr>
        </thead>
        <tbody>
'''

for _, r in df_balance.iterrows():
    table_html += f'''
            <tr style="border-bottom: 1px solid #cbd5e0; text-align: right; color: #000000;">
                <td style="padding: 8px 12px; text-align: center; font-weight: bold; color: #000000;">{int(r['año'])}</td>
                <td style="padding: 8px 12px; color: #000000;">{r['produccion_ton']:,.0f}</td>
                <td style="padding: 8px 12px; color: #000000;">{r['importaciones_ton']:,.0f}</td>
                <td style="padding: 8px 12px; color: #000000;">{r['exportaciones_ton']:,.0f}</td>
                <td style="padding: 8px 12px; font-weight: 700; color: #000000;">{r['demanda_aparente_ton']:,.0f}</td>
                <td style="padding: 8px 12px; color: #000000;">{r['poblacion_dane']:,.0f}</td>
                <td style="padding: 8px 12px; font-weight: 900; color: #000000;">{r['consumo_per_capita_kg']:.2f}</td>
            </tr>'''

table_html += '''
        </tbody>
    </table>
    <div style="font-size: 11.5px; font-style: italic; color: #000000; margin-top: 8px; font-weight: 500;">
        Nota. Elaboración propia a partir de Evaluaciones Agropecuarias Municipales - EVA (UPRA, 2025), proyecciones censales de población CNPV 2018 (DANE, 2025) y registros de comercio exterior DIAN/DANE.
    </div>
</div>
'''
display(HTML(table_html))
