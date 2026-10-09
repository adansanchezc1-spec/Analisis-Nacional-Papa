# ==============================================================================
# FIGURA 8 (CRUCIAL): CRUCE SIMULTÁNEO NORMALIZADO: IVE DE ABASTECIMIENTO VS IVE DE PRECIO
# ==============================================================================
sipsa_mes_dual = df_sipsa.groupby(['año', 'mes']).agg(
    vol_medio=('volumen_ingreso_ton', 'sum'),
    prec_medio=('precio_prom_kg', 'mean')
).reset_index()

vol_global_mean = sipsa_mes_dual['vol_medio'].mean()
prec_global_mean = sipsa_mes_dual['prec_medio'].mean()

ive_dual = sipsa_mes_dual.groupby('mes').agg(
    vol_mes=('vol_medio', 'mean'),
    prec_mes=('prec_medio', 'mean')
).reset_index()

ive_dual['ive_abastecimiento'] = (ive_dual['vol_mes'] / vol_global_mean) * 100.0
ive_dual['ive_precio'] = (ive_dual['prec_mes'] / prec_global_mean) * 100.0

r_pearson = np.corrcoef(ive_dual['ive_abastecimiento'], ive_dual['ive_precio'])[0, 1]

fig, ax = plt.subplots(figsize=(11, 5.4), dpi=300)

l_oferta = ax.plot(ive_dual['mes'], ive_dual['ive_abastecimiento'], color='#1e88e5', marker='s', linewidth=2.5, markersize=7.5, label='IVE Abastecimiento (Oferta Mayorista)')
l_precio = ax.plot(ive_dual['mes'], ive_dual['ive_precio'], color='#d9534f', marker='o', linewidth=2.5, markersize=7.5, label='IVE Precios (Cotización Mayorista)')

ax.axhline(100.0, color='#000000', linestyle='--', linewidth=1.4, alpha=0.85, label='Nivel Base Anual (Base 100)')

ax.set_xticks(range(1, 13))
ax.set_xticklabels(meses_labels, fontweight='bold', color='#000000')
ax.set_xlabel('Mes del Año (Ciclo Estacional Consolidado)', fontsize=10.5, fontweight='bold', color='#000000')
ax.set_ylabel('Número Índice Normalizado (Base 100)', fontsize=10.5, fontweight='bold', color='#000000')
ax.set_ylim(75, 135)

# Formato APA 7.ª con Texto Negro Puro
ax.set_title('Figura 8. Cruce simultáneo normalizado del IVE de abastecimiento frente al IVE de precios mayoristas: Evidencia empírica de la ley de oferta y demanda en Colombia (2019–2025)', fontsize=11.5, fontweight='bold', loc='left', pad=14, color='#000000')
fig.text(0.01, -0.05, f'Nota. Elaboración propia a partir de microdatos de SIPSA (DANE, 2025). La correlación bivariada de Pearson entre oferta y precio es r = {r_pearson:.3f}, demostrando la severa elasticidad precio negativa del mercado papero nacional.', fontsize=9, style='italic', color='#000000')

ax.legend(loc='upper right', frameon=True, fontsize=9)
ax.grid(True, linestyle=':', alpha=0.5, color='#cbd5e0')

plt.tight_layout()
fig8_path = CURATED_DIR / 'reportes_graficos/figura_8_cruce_estacional_oferta_precio.png'
fig.savefig(fig8_path, dpi=300, bbox_inches='tight')
plt.show()
print(f'[OK] Figura 8 guardada en: {fig8_path}')
