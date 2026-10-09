# ==============================================================================
# TABLA 2: VOLATILIDAD ANUALIZADA DE PRECIOS MAYORISTAS (2019-2025) - TEXTO NEGRO
# ==============================================================================
df_volatilidad = df_sipsa.groupby('año')['precio_prom_kg'].agg(
    precio_promedio=('mean'),
    desviacion_std=('std'),
    cv_porcentaje=(lambda x: (x.std() / x.mean()) * 100.0),
    asimetria=('skew'),
    curtosis=(lambda x: x.kurtosis())
).reset_index()

table2_html = '''
<div style="margin: 20px 0; font-family: 'Segoe UI', Tahoma, sans-serif; color: #000000;">
    <div style="font-weight: 800; font-size: 14px; color: #000000; margin-bottom: 8px;">
        Tabla 2. Volatilidad anualizada y momentos de dispersión estocástica del precio mayorista de la papa (SIPSA 2019–2025)
    </div>
    <table style="width: 100%; border-collapse: collapse; font-size: 13px; border: 1.5px solid #000000; color: #000000;">
        <thead>
            <tr style="background: #edf2f7; color: #000000; text-align: right; border-bottom: 2px solid #000000;">
                <th style="padding: 9px 12px; text-align: center; color: #000000; font-weight: 800;">Año</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Precio Promedio ($/kg)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Desv. Estándar ($\sigma$)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Coef. Variación (CV %)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Asimetría ($S$)</th>
                <th style="padding: 9px 12px; color: #000000; font-weight: 800;">Curtosis ($K$)</th>
                <th style="padding: 9px 12px; text-align: center; color: #000000; font-weight: 800;">Nivel de Riesgo</th>
            </tr>
        </thead>
        <tbody>
'''

for _, r in df_volatilidad.iterrows():
    cv_val = r['cv_porcentaje']
    nivel_riesgo = 'Muy Alto' if cv_val > 21.4 else 'Alto'
    table2_html += f'''
            <tr style="border-bottom: 1px solid #cbd5e0; text-align: right; color: #000000;">
                <td style="padding: 8px 12px; text-align: center; font-weight: bold; color: #000000;">{int(r['año'])}</td>
                <td style="padding: 8px 12px; font-weight: 700; color: #000000;">${r['precio_promedio']:,.2f}</td>
                <td style="padding: 8px 12px; color: #000000;">${r['desviacion_std']:,.2f}</td>
                <td style="padding: 8px 12px; font-weight: 800; color: #000000;">{cv_val:.2f}%</td>
                <td style="padding: 8px 12px; color: #000000;">{r['asimetria']:.2f}</td>
                <td style="padding: 8px 12px; color: #000000;">{r['curtosis']:.2f}</td>
                <td style="padding: 8px 12px; text-align: center; font-weight: 700; color: #000000;">{nivel_riesgo}</td>
            </tr>'''

table2_html += '''
        </tbody>
    </table>
    <div style="font-size: 11.5px; font-style: italic; color: #000000; margin-top: 8px; font-weight: 500;">
        Nota. Elaboración propia a partir de registros de precios mayoristas de SIPSA (DANE, 2025). La asimetría positiva persistente ratifica la frecuencia de picos inflacionarios alcistas.
    </div>
</div>
'''
display(HTML(table2_html))
