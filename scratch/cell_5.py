# ==============================================================================
# TARJETA KPI: MÉTRICAS DESTACADAS DEL MERCADO DE LA PAPA EN COLOMBIA (TEXTO NEGRO)
# ==============================================================================
prod_total_2025 = float(df_eva[df_eva['año'] == 2025]['produccion_ton'].sum())
pob_2025 = FeaturesService.POBLACION_NACIONAL_DANE.get(2025, {}).get('total', 53057212)
cons_per_cap_2025 = (prod_total_2025 * 1000.0) / pob_2025

dept_prod = df_eva.groupby('departamento')['produccion_ton'].sum()
top1_dept_name = dept_prod.idxmax()
top1_dept_share = (dept_prod.max() / dept_prod.sum()) * 100.0

dept_shares = (dept_prod / dept_prod.sum()) * 100.0
hhi_dept = float((dept_shares**2).sum())

mean_price = df_sipsa['precio_prom_kg'].mean()
std_price = df_sipsa['precio_prom_kg'].std()
cv_price = (std_price / mean_price) * 100.0

abast_total_sipsa = df_sipsa.groupby('año')['volumen_ingreso_ton'].sum().mean()

kpi_html = f'''
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px; margin: 20px 0; font-family: 'Segoe UI', Tahoma, sans-serif; color: #000000;">
    <div style="background: #ffffff; border-radius: 10px; padding: 18px 14px; text-align: center; border-left: 6px solid #000000; box-shadow: 0 2px 10px rgba(0,0,0,0.08); border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000;">
        <div style="font-size: 11.5px; text-transform: uppercase; color: #000000; font-weight: 800; letter-spacing: 0.6px;">PRODUCCIÓN NACIONAL (2025)</div>
        <div style="font-size: 24px; font-weight: 900; color: #000000; margin: 8px 0 4px 0;">{prod_total_2025/1e6:.2f} M Ton</div>
        <div style="font-size: 12px; font-weight: 600; color: #000000;">Cosecha en campo (EVA)</div>
    </div>
    <div style="background: #ffffff; border-radius: 10px; padding: 18px 14px; text-align: center; border-left: 6px solid #000000; box-shadow: 0 2px 10px rgba(0,0,0,0.08); border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000;">
        <div style="font-size: 11.5px; text-transform: uppercase; color: #000000; font-weight: 800; letter-spacing: 0.6px;">CONSUMO PER CÁPITA (2025)</div>
        <div style="font-size: 24px; font-weight: 900; color: #000000; margin: 8px 0 4px 0;">{cons_per_cap_2025:.1f} kg/hab</div>
        <div style="font-size: 12px; font-weight: 600; color: #000000;">Demanda aparente anual</div>
    </div>
    <div style="background: #ffffff; border-radius: 10px; padding: 18px 14px; text-align: center; border-left: 6px solid #000000; box-shadow: 0 2px 10px rgba(0,0,0,0.08); border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000;">
        <div style="font-size: 11.5px; text-transform: uppercase; color: #000000; font-weight: 800; letter-spacing: 0.6px;">CUOTA TOP 1 DEPARTAMENTO</div>
        <div style="font-size: 24px; font-weight: 900; color: #000000; margin: 8px 0 4px 0;">{top1_dept_share:.1f}%</div>
        <div style="font-size: 12px; font-weight: 600; color: #000000;">{top1_dept_name} (Líder)</div>
    </div>
    <div style="background: #ffffff; border-radius: 10px; padding: 18px 14px; text-align: center; border-left: 6px solid #000000; box-shadow: 0 2px 10px rgba(0,0,0,0.08); border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000;">
        <div style="font-size: 11.5px; text-transform: uppercase; color: #000000; font-weight: 800; letter-spacing: 0.6px;">CONCENTRACIÓN HHI</div>
        <div style="font-size: 24px; font-weight: 900; color: #000000; margin: 8px 0 4px 0;">{hhi_dept:.0f} pts</div>
        <div style="font-size: 12px; font-weight: 600; color: #000000;">Alta concentración (&gt;1,800)</div>
    </div>
    <div style="background: #ffffff; border-radius: 10px; padding: 18px 14px; text-align: center; border-left: 6px solid #000000; box-shadow: 0 2px 10px rgba(0,0,0,0.08); border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000;">
        <div style="font-size: 11.5px; text-transform: uppercase; color: #000000; font-weight: 800; letter-spacing: 0.6px;">VOLATILIDAD PRECIO (CV)</div>
        <div style="font-size: 24px; font-weight: 900; color: #000000; margin: 8px 0 4px 0;">{cv_price:.1f}%</div>
        <div style="font-size: 12px; font-weight: 600; color: #000000;">Dispersión mayorista global</div>
    </div>
    <div style="background: #ffffff; border-radius: 10px; padding: 18px 14px; text-align: center; border-left: 6px solid #000000; box-shadow: 0 2px 10px rgba(0,0,0,0.08); border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000;">
        <div style="font-size: 11.5px; text-transform: uppercase; color: #000000; font-weight: 800; letter-spacing: 0.6px;">ABASTECIMIENTO PROMEDIO</div>
        <div style="font-size: 24px; font-weight: 900; color: #000000; margin: 8px 0 4px 0;">{abast_total_sipsa/1e6:.2f} M Ton</div>
        <div style="font-size: 12px; font-weight: 600; color: #000000;">Ingreso anual SIPSA</div>
    </div>
</div>
'''
display(HTML(kpi_html))
