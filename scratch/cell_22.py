# ==============================================================================
# FIGURA 7: EVOLUCIÓN TEMPORAL DEL PRECIO MAYORISTA MENSUAL CON BANDA DE DISPERSIÓN
# ==============================================================================
df_precio_serie = df_sipsa.groupby('fecha_mes')['precio_prom_kg'].agg(
    precio_medio=('mean'),
    precio_std=('std'),
    p25=(lambda x: x.quantile(0.25)),
    p75=(lambda x: x.quantile(0.75))
).reset_index()

fig, ax = plt.subplots(figsize=(11.5, 5.2), dpi=300)

ax.plot(df_precio_serie['fecha_mes'], df_precio_serie['precio_medio'], color='#1a3a5a', linewidth=2.5, label='Precio Mayorista Promedio Mensual ($/kg)')
ax.fill_between(df_precio_serie['fecha_mes'], df_precio_serie['p25'], df_precio_serie['p75'], color='#2b5b84', alpha=0.25, label='Rango Intercuartílico (P25 - P75)')

# Marcadores de eventos históricos exógenos
ax.axvline(pd.to_datetime('2020-03-01'), color='#000000', linestyle=':', linewidth=1.4)
ax.text(pd.to_datetime('2020-03-01'), 4800, ' Pandemia COVID-19', fontsize=8.5, color='#000000', fontweight='bold', rotation=90, va='top')

ax.axvline(pd.to_datetime('2021-05-01'), color='#000000', linestyle=':', linewidth=1.4)
ax.text(pd.to_datetime('2021-05-01'), 4800, ' Paro Nacional 2021', fontsize=8.5, color='#000000', fontweight='bold', rotation=90, va='top')

ax.axvline(pd.to_datetime('2022-02-01'), color='#d9534f', linestyle=':', linewidth=1.6)
ax.text(pd.to_datetime('2022-02-01'), 4800, ' Guerra Ucrania / Insumos', fontsize=8.5, color='#d9534f', fontweight='bold', rotation=90, va='top')

ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
ax.set_xlabel('Periodo Mensual Continuo (2019–2025)', fontsize=10.5, fontweight='bold', color='#000000')
ax.set_ylabel('Precio Corriente Mayorista ($ COP / kg)', fontsize=10.5, fontweight='bold', color='#000000')
ax.set_ylim(1000, 5200)

# Formato APA 7.ª con Texto Negro Puro
ax.set_title('Figura 7. Evolución histórica del precio mayorista mensual de la papa con banda de dispersión intercuartílica (SIPSA 2019–2025)', fontsize=11.5, fontweight='bold', loc='left', pad=14, color='#000000')
fig.text(0.01, -0.05, 'Nota. Elaboración propia a partir de microdatos de precios mayoristas de SIPSA (DANE, 2025). La banda sombreada representa la dispersión espacial entre plazas de mercado (P25 a P75).', fontsize=9, style='italic', color='#000000')

ax.legend(loc='upper left', frameon=True, fontsize=9)
ax.grid(True, linestyle=':', alpha=0.5, color='#cbd5e0')

plt.tight_layout()
fig7_path = CURATED_DIR / 'reportes_graficos/figura_7_precio_serie_historica.png'
fig.savefig(fig7_path, dpi=300, bbox_inches='tight')
plt.show()
print(f'[OK] Figura 7 guardada en: {fig7_path}')
