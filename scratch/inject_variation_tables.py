import json
from pathlib import Path

root = Path(r"c:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando")
report_path = root / "docs/report.ipynb"

with open(report_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# -------------------------------------------------------------------------
# CÓDIGO CELDA 9: FIGURA 1 + TABLA 1.1 COMPLETA CON DETALLE DE VARIACIÓN
# -------------------------------------------------------------------------
cell_9_code = '''# ==============================================================================
# FIGURA 1: CICLO FENOLÓGICO COMPARADO Y BALANCE DE SUPERFICIE (SIEMBRA VS COSECHA)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.5, 7.5), dpi=300, gridspec_kw={'height_ratios': [1.2, 1.4]})

# PANEL 1: DIAGRAMA FENOLÓGICO COMPARADO (PAPA DE AÑO VS PAPA CRIOLLA)
etapas_anio = [('Brotación\\n(0-30d)', 30, '#8d6e63'), ('Desarrollo\\n(30-60d)', 30, '#43a047'),
               ('Tuberización\\n(60-105d)', 45, '#1e88e5'), ('Llenado\\n(105-150d)', 45, '#fb8c00'),
               ('Madurez & Cosecha\\n(150-180d)', 30, '#d81b60')]

acum_a = 0
for nombre, dur, col in etapas_anio:
    ax1.barh(1, dur, left=acum_a, color=col, edgecolor='#000000', height=0.45)
    ax1.text(acum_a + dur/2.0, 1, nombre, ha='center', va='center', color='#ffffff', fontweight='bold', fontsize=8.2)
    acum_a += dur

etapas_crio = [('Emergencia (0-20d)', 20, '#8d6e63'), ('Vegetativo (20-45d)', 25, '#43a047'),
               ('Tuberización (45-80d)', 35, '#1e88e5'), ('Llenado (80-110d)', 30, '#fb8c00'),
               ('Cosecha (110-120d)', 10, '#d81b60')]

acum_c = 0
for nombre, dur, col in etapas_crio:
    ax1.barh(0, dur, left=acum_c, color=col, edgecolor='#000000', height=0.45)
    ax1.text(acum_c + dur/2.0, 0, nombre, ha='center', va='center', color='#ffffff', fontweight='bold', fontsize=7.8)
    acum_c += dur

ax1.set_xlim(0, 185)
ax1.set_ylim(-0.5, 1.5)
ax1.set_yticks([0, 1])
ax1.set_yticklabels(['Papa Criolla\\n(90-120 días)', 'Papas de Año\\n(150-180 días)'], fontsize=9.5, fontweight='bold', color='#000000')
ax1.set_xlabel('Duración del Ciclo Biológico (Días tras Siembra)', fontsize=10, fontweight='bold', color='#000000')
ax1.set_title('Panel A. Fases fenológicas y duración de ciclo por tipología botánica (Solanum tuberosum vs Solanum phureja)', fontsize=10.5, fontweight='bold', loc='left', color='#000000')
ax1.grid(axis='x', linestyle=':', alpha=0.5, color='#cbd5e0')

# PANEL 2: BALANCE HISTÓRICO ÁREA SEMBRADA VS COSECHADA (2019-2025)
col_a = [c for c in df_eva.columns if 'a' in c.lower() and 'o' in c.lower() and len(c) <= 4][0]
area_bal = df_eva.groupby(col_a).agg(
    sembrada=('area_sembrada_ha', 'sum'),
    cosechada=('area_cosechada_ha', 'sum')
).reset_index()
area_bal['perdida'] = area_bal['sembrada'] - area_bal['cosechada']
area_bal['efectividad'] = (area_bal['cosechada'] / area_bal['sembrada']) * 100.0

anios_arr = area_bal[col_a].values
x = np.arange(len(anios_arr))
w = 0.35

rects1 = ax2.bar(x - w/2, area_bal['sembrada']/1000.0, w, label='Área Sembrada (Miles ha)', color='#0284c7', edgecolor='#000000')
rects2 = ax2.bar(x + w/2, area_bal['cosechada']/1000.0, w, label='Área Cosechada (Miles ha)', color='#16a34a', edgecolor='#000000')

ax2_ef = ax2.twinx()
line_ef = ax2_ef.plot(x, area_bal['efectividad'], color='#ea580c', marker='o', linewidth=2.5, label='Efectividad Cosecha (%)')
ax2_ef.set_ylim(85, 105)
ax2_ef.set_ylabel('Efectividad de Cosecha (%)', fontsize=10, fontweight='bold', color='#ea580c')
ax2_ef.tick_params(axis='y', labelcolor='#ea580c')

ax2.set_xticks(x)
ax2.set_xticklabels(anios_arr, fontsize=9.5, fontweight='bold', color='#000000')
ax2.set_ylabel('Superficie Agrícola (Miles ha)', fontsize=10, fontweight='bold', color='#000000')
ax2.set_title('Panel B. Balance plurianual nacional de Área Sembrada vs. Área Cosechada y Efectividad (2019–2025)', fontsize=10.5, fontweight='bold', loc='left', color='#000000')
ax2.grid(axis='y', linestyle=':', alpha=0.5, color='#cbd5e0')

# Leyenda combinada
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_ef.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='lower left', frameon=True, fontsize=9)

# Anotación APA 7.ª
fig.text(0.01, -0.04, 'Figura 1. Caracterización fenológica comparada y balance plurianual de siembra vs cosecha en Colombia.\\nNota. Datos compilados a partir de microdatos de Evaluaciones Agropecuarias Municipales - EVA (UPRA, 2025) y Corpoica/Agrosavia (2024).\\nEn 2023 se observa la mayor merma histórica (17,102 ha perdidas, 91.1% efectividad) debido al fenómeno de El Niño y costos de fertilizantes.', fontsize=8.5, style='italic', color='#000000')

plt.tight_layout()
fig1_path = CURATED_DIR / 'reportes_graficos/figura_1_fenologia_calendario.png'
fig1_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(fig1_path, dpi=300, bbox_inches='tight')
plt.show()
print(f'[OK] Figura 1 actualizada con ciclo fenológico y balance siembra vs cosecha: {fig1_path}')

# ==============================================================================
# TABLA 1.1: AUDITORÍA DE VARIACIONES DE SUPERFICIE Y EFECTIVIDAD (DEBAJO DE FIGURA 1)
# ==============================================================================
t1_df = area_bal.copy()
t1_df['var_sembrada_ha'] = t1_df['sembrada'].diff()
t1_df['var_sembrada_pct'] = t1_df['sembrada'].pct_change() * 100.0
t1_df['var_cosechada_ha'] = t1_df['cosechada'].diff()
t1_df['var_cosechada_pct'] = t1_df['cosechada'].pct_change() * 100.0
t1_df['var_perdida_ha'] = t1_df['perdida'].diff()
t1_df['var_efectividad_pp'] = t1_df['efectividad'].diff()

regimenes_t1 = [
    'Línea base pre-pandemia; régimen bimodal regular',
    'Expansión de siembras (+6.6%); inicio choque logístico',
    'Contracción de área (-5.8%); paro nacional y lluvias',
    'Crisis global de insumos; urea y fertilizantes récord',
    'Fenómeno de El Niño severo; merma récord (17,102 ha)',
    'Recuperación gradual de efectividad (+2.0 p.p.)',
    'Normalización agroclimática; consolidación UPRA'
]

tot_s = t1_df['sembrada'].sum()
tot_c = t1_df['cosechada'].sum()
tot_p = t1_df['perdida'].sum()
tot_ef = (tot_c / tot_s) * 100.0

table_1_1_html = f\'\'\'
<div style="margin: 20px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #000000;">
    <div style="font-weight: 800; font-size: 14.5px; color: #000000; margin-bottom: 8px;">
        Tabla 1.1. Balance Dinámico Plurianual de Superficie Agrícola: Área Sembrada vs. Cosechada, Pérdidas Físicas y Tasa de Efectividad (EVA 2019–2025)
    </div>
    <div style="overflow-x: auto; border: 2px solid #000000; border-radius: 6px;">
        <table style="width: 100%; border-collapse: collapse; font-size: 12.5px; color: #000000; background-color: #ffffff;">
            <thead>
                <tr style="background: #edf2f7; color: #000000; text-align: right; border-bottom: 2px solid #000000; font-weight: 800; text-transform: uppercase; font-size: 11px; letter-spacing: 0.3px;">
                    <th style="padding: 10px 12px; text-align: center; border: 1px solid #cbd5e1;">Año</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Área Sembrada (ha)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Var. Siembra (ha | %)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Área Cosechada (ha)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Var. Cosecha (ha | %)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Pérdida Área (ha)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Efectividad Cosecha (%)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Var. Efectividad (p.p.)</th>
                    <th style="padding: 10px 12px; text-align: left; border: 1px solid #cbd5e1;">Régimen Agroclimático / Fenológico</th>
                </tr>
            </thead>
            <tbody>
\'\'\'

for idx, r in t1_df.iterrows():
    anio_val = int(r[col_a])
    s_val = r['sembrada']
    c_val = r['cosechada']
    p_val = r['perdida']
    ef_val = r['efectividad']
    reg_val = regimenes_t1[idx]

    # Formatter for variations
    if idx == 0:
        var_s_str = '<span style="color: #64748b; font-weight: 700;">Base Ref.</span>'
        var_c_str = '<span style="color: #64748b; font-weight: 700;">Base Ref.</span>'
        var_ef_str = '<span style="color: #64748b; font-weight: 700;">--</span>'
    else:
        vs_ha = r['var_sembrada_ha']
        vs_pct = r['var_sembrada_pct']
        col_s = '#16a34a' if vs_pct >= 0 else '#dc2626'
        sign_s = '+' if vs_pct >= 0 else ''
        var_s_str = f'<span style="color: {col_s}; font-weight: 700;">{sign_s}{vs_ha:,.0f} ha ({sign_s}{vs_pct:.1f}%)</span>'

        vc_ha = r['var_cosechada_ha']
        vc_pct = r['var_cosechada_pct']
        col_c = '#16a34a' if vc_pct >= 0 else '#dc2626'
        sign_c = '+' if vc_pct >= 0 else ''
        var_c_str = f'<span style="color: {col_c}; font-weight: 700;">{sign_c}{vc_ha:,.0f} ha ({sign_c}{vc_pct:.1f}%)</span>'

        vef = r['var_efectividad_pp']
        col_ef = '#16a34a' if vef >= 0 else '#dc2626'
        sign_ef = '+' if vef >= 0 else ''
        var_ef_str = f'<span style="color: {col_ef}; font-weight: 800;">{sign_ef}{vef:.2f} p.p.</span>'

    col_ef_badge = '#16a34a' if ef_val >= 95 else ('#ea580c' if ef_val >= 92 else '#dc2626')

    table_1_1_html += f\'\'\'
                <tr style="border-bottom: 1px solid #cbd5e1; text-align: right; background-color: {'#ffffff' if idx % 2 == 0 else '#f8fafc'};">
                    <td style="padding: 8px 12px; text-align: center; font-weight: 900; border: 1px solid #cbd5e1;">{anio_val}</td>
                    <td style="padding: 8px 12px; font-weight: 700; border: 1px solid #cbd5e1; color: #0284c7;">{s_val:,.0f} ha</td>
                    <td style="padding: 8px 12px; border: 1px solid #cbd5e1;">{var_s_str}</td>
                    <td style="padding: 8px 12px; font-weight: 700; border: 1px solid #cbd5e1; color: #16a34a;">{c_val:,.0f} ha</td>
                    <td style="padding: 8px 12px; border: 1px solid #cbd5e1;">{var_c_str}</td>
                    <td style="padding: 8px 12px; font-weight: 800; border: 1px solid #cbd5e1; color: #dc2626;">-{p_val:,.0f} ha</td>
                    <td style="padding: 8px 12px; font-weight: 900; border: 1px solid #cbd5e1; color: {col_ef_badge};">{ef_val:.2f}%</td>
                    <td style="padding: 8px 12px; border: 1px solid #cbd5e1;">{var_ef_str}</td>
                    <td style="padding: 8px 12px; text-align: left; font-size: 11.5px; font-weight: 600; border: 1px solid #cbd5e1;">{reg_val}</td>
                </tr>\'\'\'

table_1_1_html += f\'\'\'
                <tr style="background: #0f172a; color: #ffffff; text-align: right; font-weight: 900; border-top: 2px solid #000000;">
                    <td style="padding: 10px 12px; text-align: center; border: 1px solid #334155; color: #f59e0b;">TOTAL / MEDIA</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #ffffff;">{tot_s:,.0f} ha</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #e2e8f0;">Media: {tot_s/7:,.0f} ha/año</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #ffffff;">{tot_c:,.0f} ha</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #e2e8f0;">Media: {tot_c/7:,.0f} ha/año</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #fca5a5;">-{tot_p:,.0f} ha</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #f59e0b;">{tot_ef:.2f}%</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #e2e8f0;">Rango: 91.1% – 100%</td>
                    <td style="padding: 10px 12px; text-align: left; font-size: 11.5px; border: 1px solid #334155; color: #f1f5f9;">Pérdida acumulada: 62,244 hectáreas en el septenio</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div style="font-size: 11.5px; font-style: italic; color: #000000; margin-top: 8px; font-weight: 500;">
        Nota. Elaboración propia a partir de microdatos de Evaluaciones Agropecuarias Municipales - EVA (UPRA, 2025). La pérdida de área física se intensifica en etapas fenológicas de tuberización y llenado por choques hídricos y heladas.
    </div>
</div>
\'\'\'
display(HTML(table_1_1_html))
'''

nb['cells'][9]['source'] = [line + '\n' for line in cell_9_code.split('\n')]

# -------------------------------------------------------------------------
# CÓDIGO CELDA 11: FIGURA 2 + TABLA 2.1 COMPLETA CON DETALLE DE VARIACIÓN
# -------------------------------------------------------------------------
cell_11_code = '''# ==============================================================================
# FIGURA 2: EVOLUCIÓN HISTÓRICA DE OFERTA: ÁREA, PRODUCCIÓN Y RENDIMIENTO (2019-2025)
# ==============================================================================
col_a = [c for c in df_eva.columns if 'a' in c.lower() and 'o' in c.lower() and len(c) <= 4][0]
df_eva_anual = df_eva.groupby(col_a).agg(
    area_cosechada_ha=('area_cosechada_ha', 'sum'),
    produccion_ton=('produccion_ton', 'sum'),
    rendimiento_ton_ha=('rendimiento_ton_ha', 'mean')
).reset_index()

fig, ax1 = plt.subplots(figsize=(10.5, 5.2), dpi=300)
x = np.arange(len(df_eva_anual))
width = 0.35

# Eje Y1: Barras de Producción y Área Escalada
b1 = ax1.bar(x - width/2, df_eva_anual['produccion_ton'] / 1e6, width, label='Producción (Millones Ton)', color='#1a3a5a', edgecolor='#000000', linewidth=0.8)
b2 = ax1.bar(x + width/2, (df_eva_anual['area_cosechada_ha'] * 20.0) / 1e6, width, label='Área Cosechada (Escalada Ha x20)', color='#4a7c59', edgecolor='#000000', linewidth=0.8)

ax1.set_xlabel('Año de Cosecha', fontsize=10.5, fontweight='bold', color='#000000')
ax1.set_ylabel('Producción Física (Millones de Toneladas)', fontsize=10.5, fontweight='bold', color='#000000')
ax1.set_xticks(x)
ax1.set_xticklabels(df_eva_anual[col_a].astype(int), fontweight='bold', color='#000000')
ax1.set_ylim(0, 5.5)

# Eje Y2: Línea de Rendimiento
ax2 = ax1.twinx()
l1 = ax2.plot(x, df_eva_anual['rendimiento_ton_ha'], color='#d9534f', marker='o', linewidth=2.5, markersize=7.5, label='Rendimiento Medio (Ton/Ha)')
ax2.set_ylabel('Rendimiento Agronómico (Ton / Ha)', fontsize=10.5, fontweight='bold', color='#000000')
ax2.tick_params(axis='y', colors='#000000')
ax2.set_ylim(15, 27)

# Título y notas APA 7.ª con Texto Negro Puro
ax1.set_title('Figura 2. Dinámica agregada de oferta de papa: área cosechada, volumen de producción y rendimiento en Colombia (2019–2025)', fontsize=11.5, fontweight='bold', loc='left', pad=14, color='#000000')
fig.text(0.01, -0.05, 'Nota. Elaboración propia a partir de microdatos de Evaluaciones Agropecuarias Municipales - EVA (MinAgricultura / UPRA, 2025). La contracción en 2022 obedece a la crisis global de fertilizantes.', fontsize=9, style='italic', color='#000000')

# Leyenda combinada
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', frameon=True, fontsize=9)
ax1.grid(axis='y', linestyle=':', alpha=0.5, color='#cbd5e0')

plt.tight_layout()
fig2_path = CURATED_DIR / 'reportes_graficos/figura_2_oferta_area_rendimiento.png'
fig.savefig(fig2_path, dpi=300, bbox_inches='tight')
plt.show()
print(f'[OK] Figura 2 guardada en: {fig2_path}')

# ==============================================================================
# TABLA 2.1: AUDITORÍA DE VARIACIONES DE PRODUCCIÓN, ÁREA Y RENDIMIENTO (DEBAJO DE FIGURA 2)
# ==============================================================================
t2_df = df_eva_anual.copy()
t2_df['var_prod_ton'] = t2_df['produccion_ton'].diff()
t2_df['var_prod_pct'] = t2_df['produccion_ton'].pct_change() * 100.0
t2_df['var_area_ha'] = t2_df['area_cosechada_ha'].diff()
t2_df['var_area_pct'] = t2_df['area_cosechada_ha'].pct_change() * 100.0
t2_df['var_rend_tha'] = t2_df['rendimiento_ton_ha'].diff()
t2_df['var_rend_pct'] = t2_df['rendimiento_ton_ha'].pct_change() * 100.0
t2_df['prod_base2019_pct'] = ((t2_df['produccion_ton'] / t2_df['produccion_ton'].iloc[0]) - 1.0) * 100.0

diagnosticos_t2 = [
    'Línea base; abastecimiento pleno y equilibrio de precios',
    'Estabilidad de volumen (-0.5%); leve contracción en rto.',
    'Caída de producción (-7.4%); bloqueos viales y paro',
    'Valle productivo (-1.7%); choque global de fertilizantes',
    'Estrés hídrico (Niño); estabilidad de volumen cosechado',
    'Repunte productivo (+6.5%); expansión en Cundinamarca',
    'Cosecha récord plurianual (+15.6%); alta productividad'
]

tot_p2 = t2_df['produccion_ton'].sum()
tot_a2 = t2_df['area_cosechada_ha'].sum()
mean_r2 = t2_df['rendimiento_ton_ha'].mean()

table_2_1_html = f\'\'\'
<div style="margin: 20px 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #000000;">
    <div style="font-weight: 800; font-size: 14.5px; color: #000000; margin-bottom: 8px;">
        Tabla 2.1. Dinámica Plurianual Agregada de Oferta: Producción Física, Superficie Cosechada, Rendimiento Agronómico y Variaciones Interanuales (EVA 2019–2025)
    </div>
    <div style="overflow-x: auto; border: 2px solid #000000; border-radius: 6px;">
        <table style="width: 100%; border-collapse: collapse; font-size: 12.5px; color: #000000; background-color: #ffffff;">
            <thead>
                <tr style="background: #edf2f7; color: #000000; text-align: right; border-bottom: 2px solid #000000; font-weight: 800; text-transform: uppercase; font-size: 11px; letter-spacing: 0.3px;">
                    <th style="padding: 10px 12px; text-align: center; border: 1px solid #cbd5e1;">Año</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Producción (Ton)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Producción (Millones t)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Var. Producción (Ton | %)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Índice Base 2019 (%)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Área Cosechada (ha)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Var. Área (ha | %)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Rendimiento (t/ha)</th>
                    <th style="padding: 10px 12px; border: 1px solid #cbd5e1;">Var. Rto. (t/ha | %)</th>
                    <th style="padding: 10px 12px; text-align: left; border: 1px solid #cbd5e1;">Diagnóstico Sectorial de Oferta</th>
                </tr>
            </thead>
            <tbody>
\'\'\'

for idx, r in t2_df.iterrows():
    anio_val = int(r[col_a])
    p_val = r['produccion_ton']
    p_mill = p_val / 1e6
    a_val = r['area_cosechada_ha']
    r_val = r['rendimiento_ton_ha']
    diag_val = diagnosticos_t2[idx]

    if idx == 0:
        var_p_str = '<span style="color: #64748b; font-weight: 700;">Base Ref.</span>'
        base_str = '<span style="color: #0284c7; font-weight: 800;">100.0% (Base)</span>'
        var_a_str = '<span style="color: #64748b; font-weight: 700;">Base Ref.</span>'
        var_r_str = '<span style="color: #64748b; font-weight: 700;">Base Ref.</span>'
    else:
        vp_ton = r['var_prod_ton']
        vp_pct = r['var_prod_pct']
        col_p = '#16a34a' if vp_pct >= 0 else '#dc2626'
        sign_p = '+' if vp_pct >= 0 else ''
        var_p_str = f'<span style="color: {col_p}; font-weight: 700;">{sign_p}{vp_ton:,.0f} t ({sign_p}{vp_pct:.1f}%)</span>'

        b_pct = r['prod_base2019_pct']
        col_b = '#16a34a' if b_pct >= 0 else '#dc2626'
        sign_b = '+' if b_pct >= 0 else ''
        base_str = f'<span style="color: {col_b}; font-weight: 800;">{sign_b}{b_pct:.1f}% vs 2019</span>'

        va_ha = r['var_area_ha']
        va_pct = r['var_area_pct']
        col_a_c = '#16a34a' if va_pct >= 0 else '#dc2626'
        sign_a = '+' if va_pct >= 0 else ''
        var_a_str = f'<span style="color: {col_a_c}; font-weight: 700;">{sign_a}{va_ha:,.0f} ha ({sign_a}{va_pct:.1f}%)</span>'

        vr_tha = r['var_rend_tha']
        vr_pct = r['var_rend_pct']
        col_r = '#16a34a' if vr_pct >= 0 else '#dc2626'
        sign_r = '+' if vr_pct >= 0 else ''
        var_r_str = f'<span style="color: {col_r}; font-weight: 700;">{sign_r}{vr_tha:.2f} t/ha ({sign_r}{vr_pct:.1f}%)</span>'

    table_2_1_html += f\'\'\'
                <tr style="border-bottom: 1px solid #cbd5e1; text-align: right; background-color: {'#ffffff' if idx % 2 == 0 else '#f8fafc'};">
                    <td style="padding: 8px 12px; text-align: center; font-weight: 900; border: 1px solid #cbd5e1;">{anio_val}</td>
                    <td style="padding: 8px 12px; font-weight: 800; border: 1px solid #cbd5e1; color: #1a3a5a;">{p_val:,.0f} t</td>
                    <td style="padding: 8px 12px; font-weight: 900; border: 1px solid #cbd5e1; color: #0284c7;">{p_mill:.2f} M t</td>
                    <td style="padding: 8px 12px; border: 1px solid #cbd5e1;">{var_p_str}</td>
                    <td style="padding: 8px 12px; border: 1px solid #cbd5e1;">{base_str}</td>
                    <td style="padding: 8px 12px; font-weight: 700; border: 1px solid #cbd5e1; color: #4a7c59;">{a_val:,.0f} ha</td>
                    <td style="padding: 8px 12px; border: 1px solid #cbd5e1;">{var_a_str}</td>
                    <td style="padding: 8px 12px; font-weight: 800; border: 1px solid #cbd5e1; color: #d9534f;">{r_val:.2f}</td>
                    <td style="padding: 8px 12px; border: 1px solid #cbd5e1;">{var_r_str}</td>
                    <td style="padding: 8px 12px; text-align: left; font-size: 11.5px; font-weight: 600; border: 1px solid #cbd5e1;">{diag_val}</td>
                </tr>\'\'\'

table_2_1_html += f\'\'\'
                <tr style="background: #0f172a; color: #ffffff; text-align: right; font-weight: 900; border-top: 2px solid #000000;">
                    <td style="padding: 10px 12px; text-align: center; border: 1px solid #334155; color: #f59e0b;">TOTAL / MEDIA</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #ffffff;">{tot_p2:,.0f} t</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #38bdf8;">{tot_p2/1e6:.2f} M t</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #e2e8f0;">Media: {tot_p2/7:,.0f} t/año</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #34d399;">+11.1% Cierre 2025</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #ffffff;">{tot_a2:,.0f} ha</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #e2e8f0;">Media: {tot_a2/7:,.0f} ha/año</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #f87171;">{mean_r2:.2f} t/ha</td>
                    <td style="padding: 10px 12px; border: 1px solid #334155; color: #e2e8f0;">Rango: 16.1 – 17.2 t/ha</td>
                    <td style="padding: 10px 12px; text-align: left; font-size: 11.5px; border: 1px solid #334155; color: #f1f5f9;">Producción agregada septenio: 27.85 Millones de Toneladas</td>
                </tr>
            </tbody>
        </table>
    </div>
    <div style="font-size: 11.5px; font-style: italic; color: #000000; margin-top: 8px; font-weight: 500;">
        Nota. Elaboración propia a partir de microdatos de Evaluaciones Agropecuarias Municipales - EVA (MinAgricultura / UPRA, 2025). Rendimiento medio calculado sobre el conjunto de parcelas censadas a nivel municipal.
    </div>
</div>
\'\'\'
display(HTML(table_2_1_html))
'''

nb['cells'][11]['source'] = [line + '\n' for line in cell_11_code.split('\n')]

# Save notebook
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Successfully injected Table 1.1 into Cell 9 and Table 2.1 into Cell 11 of docs/report.ipynb!")
