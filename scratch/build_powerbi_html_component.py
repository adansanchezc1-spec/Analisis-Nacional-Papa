import json
from pathlib import Path

root = Path(r"c:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando")
payload_file = root / "scratch/dashboard_payload.json"
with open(payload_file, "r", encoding="utf-8") as f:
    data_json_str = f.read()

html_code = f"""
<div id="pbi-dashboard-container" style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f1f5f9; padding: 18px; border-radius: 12px; border: 2px solid #0f172a; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); color: #0f172a; max-width: 100%; margin: 15px 0;">

  <!-- TOP HEADER RIBBON (POWER BI STYLE) -->
  <div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; padding: 16px 20px; border-radius: 8px 8px 0 0; display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid #f59e0b; flex-wrap: wrap; gap: 10px;">
    <div style="display: flex; align-items: center; gap: 14px;">
      <div style="background-color: #f59e0b; color: #000000; font-weight: 900; font-size: 16px; padding: 6px 12px; border-radius: 6px; letter-spacing: 0.5px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
        POWER BI PRO
      </div>
      <div>
        <h2 style="margin: 0; font-size: 19px; font-weight: 800; letter-spacing: -0.3px; color: #ffffff;">TABLERO EJECUTIVO Y DRILL-DOWN MULTIDIMENSIONAL</h2>
        <p style="margin: 3px 0 0 0; font-size: 12.5px; color: #e2e8f0; font-weight: 500;">
          Monitoreo Integrado de Producción (EVA) y Precios Mayoristas (SIPSA) | Colombia 2019–2025
        </p>
      </div>
    </div>
    <div style="display: flex; align-items: center; gap: 10px;">
      <button id="pbi-btn-reset" style="background-color: #334155; color: #ffffff; border: 1px solid #64748b; padding: 8px 14px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; transition: all 0.2s ease; display: flex; align-items: center; gap: 6px;" onmouseover="this.style.backgroundColor='#475569'" onmouseout="this.style.backgroundColor='#334155'">
        <span>🔄</span> Restablecer Filtros
      </button>
      <span style="background-color: rgba(255,255,255,0.12); padding: 6px 12px; border-radius: 6px; font-size: 11.5px; font-weight: 600; color: #f8fafc; border: 1px solid rgba(255,255,255,0.2);">
        🟢 Motor Interactivo Activo
      </span>
    </div>
  </div>

  <!-- BREADCRUMB DRILLDOWN NAVIGATION BAR -->
  <div style="background-color: #ffffff; border-left: 2px solid #0f172a; border-right: 2px solid #0f172a; border-bottom: 2px solid #cbd5e1; padding: 10px 18px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
    <div style="display: flex; align-items: center; gap: 8px; font-size: 13.5px; font-weight: 700; color: #0f172a;">
      <span style="color: #475569; font-weight: 600;">Nivel Jerárquico:</span>
      <span id="pbi-bc-nacional" style="color: #0284c7; cursor: pointer; text-decoration: underline; padding: 2px 6px; border-radius: 4px;" title="Ir al nivel Nacional">🇨🇴 Nacional</span>
      <span id="pbi-bc-sep1" style="color: #94a3b8;">&gt;</span>
      <span id="pbi-bc-depto" style="color: #0f172a; padding: 2px 6px; border-radius: 4px;">📍 Todos los Departamentos</span>
      <span id="pbi-bc-sep2" style="color: #94a3b8; display: none;">&gt;</span>
      <span id="pbi-bc-mpio" style="color: #0f172a; padding: 2px 6px; border-radius: 4px; display: none;">🏙️ Municipio</span>
    </div>
    <div style="display: flex; gap: 8px;">
      <button id="pbi-btn-drillup" style="background-color: #0f172a; color: #ffffff; border: none; padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; display: none; align-items: center; gap: 6px;">
        <span>⬆️</span> Subir Nivel (Drill Up)
      </button>
      <div id="pbi-status-indicator" style="font-size: 12px; font-weight: 700; color: #0369a1; background-color: #e0f2fe; padding: 5px 12px; border-radius: 20px; border: 1px solid #bae6fd;">
        Vista: Consolidado Nacional
      </div>
    </div>
  </div>

  <!-- SLICERS RIBBON (FILTROS POWER BI) -->
  <div style="background-color: #f8fafc; border-left: 2px solid #0f172a; border-right: 2px solid #0f172a; border-bottom: 2px solid #cbd5e1; padding: 14px 18px; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px;">
    <!-- Slicer Año -->
    <div>
      <label style="display: block; font-size: 12px; font-weight: 800; color: #0f172a; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 0.3px;">
        📅 Año de Cosecha / Comercialización
      </label>
      <select id="pbi-slicer-anio" style="width: 100%; padding: 8px 12px; font-size: 13px; font-weight: 700; color: #0f172a; background-color: #ffffff; border: 2px solid #0f172a; border-radius: 6px; cursor: pointer; outline: none;">
        <option value="all">Consolidado Plurianual (2019-2025)</option>
        <option value="2019">2019</option>
        <option value="2020">2020</option>
        <option value="2021">2021</option>
        <option value="2022">2022</option>
        <option value="2023">2023</option>
        <option value="2024">2024</option>
        <option value="2025">2025</option>
      </select>
    </div>

    <!-- Slicer Departamento -->
    <div>
      <label style="display: block; font-size: 12px; font-weight: 800; color: #0f172a; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 0.3px;">
        📍 Departamento Productor
      </label>
      <select id="pbi-slicer-depto" style="width: 100%; padding: 8px 12px; font-size: 13px; font-weight: 700; color: #0f172a; background-color: #ffffff; border: 2px solid #0f172a; border-radius: 6px; cursor: pointer; outline: none;">
        <option value="all">Todos los Departamentos (Nacional)</option>
      </select>
    </div>

    <!-- Slicer Variedad -->
    <div>
      <label style="display: block; font-size: 12px; font-weight: 800; color: #0f172a; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 0.3px;">
        🥔 Variedad Comercial
      </label>
      <select id="pbi-slicer-var" style="width: 100%; padding: 8px 12px; font-size: 13px; font-weight: 700; color: #0f172a; background-color: #ffffff; border: 2px solid #0f172a; border-radius: 6px; cursor: pointer; outline: none;">
        <option value="all">Todas las Variedades Comerciales</option>
        <option value="Pastusa">Papa Pastusa</option>
        <option value="R-12">Papa R-12</option>
        <option value="Criolla">Papa Criolla (Amarilla)</option>
        <option value="Diacol Capiro">Papa Diacol Capiro (Industrial)</option>
        <option value="Superior">Papa Superior</option>
        <option value="Tuquerreña">Papa Tuquerreña</option>
        <option value="Otras Variedades">Otras Variedades</option>
      </select>
    </div>
  </div>

  <!-- KPI CARDS CONTAINER -->
  <div style="background-color: #ffffff; border-left: 2px solid #0f172a; border-right: 2px solid #0f172a; border-bottom: 2px solid #cbd5e1; padding: 18px; display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px;">
    <!-- Card 1: Produccion -->
    <div style="background: #ffffff; border: 2px solid #0f172a; border-left: 6px solid #0284c7; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">Producción Total</div>
      <div id="pbi-kpi-prod" style="font-size: 24px; font-weight: 900; color: #0f172a; margin: 4px 0 2px 0;">--</div>
      <div id="pbi-kpi-prod-sub" style="font-size: 11.5px; font-weight: 700; color: #0369a1;">Miles de Toneladas (kt)</div>
    </div>

    <!-- Card 2: Area Cosechada -->
    <div style="background: #ffffff; border: 2px solid #0f172a; border-left: 6px solid #16a34a; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">Área Cosechada</div>
      <div id="pbi-kpi-area" style="font-size: 24px; font-weight: 900; color: #0f172a; margin: 4px 0 2px 0;">--</div>
      <div id="pbi-kpi-area-sub" style="font-size: 11.5px; font-weight: 700; color: #15803d;">Hectáreas Sembradas (ha)</div>
    </div>

    <!-- Card 3: Rendimiento -->
    <div style="background: #ffffff; border: 2px solid #0f172a; border-left: 6px solid #ea580c; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">Rendimiento Ponderado</div>
      <div id="pbi-kpi-rend" style="font-size: 24px; font-weight: 900; color: #0f172a; margin: 4px 0 2px 0;">--</div>
      <div id="pbi-kpi-rend-sub" style="font-size: 11.5px; font-weight: 700; color: #c2410c;">t / ha (Media Ref: 19.8)</div>
    </div>

    <!-- Card 4: Precio Mayorista -->
    <div style="background: #ffffff; border: 2px solid #0f172a; border-left: 6px solid #9333ea; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">Precio Mayorista Prom.</div>
      <div id="pbi-kpi-precio" style="font-size: 24px; font-weight: 900; color: #0f172a; margin: 4px 0 2px 0;">--</div>
      <div id="pbi-kpi-precio-sub" style="font-size: 11.5px; font-weight: 700; color: #7e22ce;">COP / kg en Centrales</div>
    </div>

    <!-- Card 5: Abastecimiento SIPSA -->
    <div style="background: #ffffff; border: 2px solid #0f172a; border-left: 6px solid #d97706; border-radius: 8px; padding: 14px 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
      <div style="font-size: 11px; font-weight: 800; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">Abastecimiento SIPSA</div>
      <div id="pbi-kpi-volumen" style="font-size: 24px; font-weight: 900; color: #0f172a; margin: 4px 0 2px 0;">--</div>
      <div id="pbi-kpi-volumen-sub" style="font-size: 11.5px; font-weight: 700; color: #b45309;">Toneladas Monitoreadas</div>
    </div>
  </div>

  <!-- MAIN VISUALIZATIONS SECTION (2 COLUMNS) -->
  <div style="background-color: #f8fafc; border-left: 2px solid #0f172a; border-right: 2px solid #0f172a; border-bottom: 2px solid #cbd5e1; padding: 18px; display: grid; grid-template-columns: 1fr 1fr; gap: 18px;">

    <!-- VISUAL 1: DRILLDOWN HIERARCHICAL BAR CHART -->
    <div style="background-color: #ffffff; border: 2px solid #0f172a; border-radius: 8px; padding: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); display: flex; flex-direction: column;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">
        <div>
          <h3 id="pbi-v1-title" style="margin: 0; font-size: 14.5px; font-weight: 800; color: #0f172a;">
            📊 Producción por Departamento (Haga clic para hacer Drilldown)
          </h3>
          <p id="pbi-v1-sub" style="margin: 3px 0 0 0; font-size: 11.5px; font-weight: 600; color: #475569;">
            Haga clic sobre una barra departamental para profundizar a nivel municipal
          </p>
        </div>
        <span style="background-color: #fef3c7; color: #92400e; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 4px; border: 1px solid #fde68a;">
          Drill-Down Activo 🔍
        </span>
      </div>
      <div id="pbi-v1-chart-container" style="flex: 1; min-height: 290px; position: relative;">
        <!-- Dynamic Bars inserted via JS -->
      </div>
    </div>

    <!-- VISUAL 2: VARIETY COMPOSITION CHART -->
    <div style="background-color: #ffffff; border: 2px solid #0f172a; border-radius: 8px; padding: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); display: flex; flex-direction: column;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">
        <div>
          <h3 style="margin: 0; font-size: 14.5px; font-weight: 800; color: #0f172a;">
            🥔 Composición por Variedad Comercial
          </h3>
          <p style="margin: 3px 0 0 0; font-size: 11.5px; font-weight: 600; color: #475569;">
            Participación porcentual y volumen en el contexto actual de filtrado
          </p>
        </div>
        <span style="background-color: #e0f2fe; color: #0369a1; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 4px; border: 1px solid #bae6fd;">
          Cross-Filtering ⚡
        </span>
      </div>
      <div id="pbi-v2-chart-container" style="flex: 1; min-height: 290px; position: relative;">
        <!-- Dynamic Variety Bars inserted via JS -->
      </div>
    </div>
  </div>

  <!-- VISUAL 3: MONTHLY TIME SERIES AND HISTORICAL TREND -->
  <div style="background-color: #ffffff; border-left: 2px solid #0f172a; border-right: 2px solid #0f172a; border-bottom: 2px solid #cbd5e1; padding: 18px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px;">
      <div>
        <h3 style="margin: 0; font-size: 14.5px; font-weight: 800; color: #0f172a;">
          📈 Dinámica Mensual y Estacionalidad: Precios Mayoristas vs Volumen Ingresado
        </h3>
        <p style="margin: 3px 0 0 0; font-size: 11.5px; font-weight: 600; color: #475569;">
          Comportamiento plurianual mensual registrado en el Sistema de Información de Precios (SIPSA)
        </p>
      </div>
      <div style="display: flex; gap: 14px; font-size: 11.5px; font-weight: 700;">
        <span style="display: flex; align-items: center; gap: 5px; color: #0284c7;">
          <span style="display: inline-block; width: 12px; height: 12px; background: #0284c7; border-radius: 2px;"></span> Volumen (t)
        </span>
        <span style="display: flex; align-items: center; gap: 5px; color: #ea580c;">
          <span style="display: inline-block; width: 12px; height: 3px; background: #ea580c;"></span> Precio ($/kg)
        </span>
      </div>
    </div>
    <div id="pbi-v3-chart-container" style="height: 180px; width: 100%; position: relative;">
      <!-- Dynamic SVG Spark/Trend inserted via JS -->
    </div>
  </div>

  <!-- VISUAL 4: DETAILED POWER BI MATRIX DATA TABLE -->
  <div style="background-color: #ffffff; border: 2px solid #0f172a; border-top: none; border-radius: 0 0 8px 8px; padding: 18px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px;">
      <div>
        <h3 style="margin: 0; font-size: 14.5px; font-weight: 800; color: #0f172a;">
          📋 Matriz de Auditoría y Detalle Municipal (Power BI Grid)
        </h3>
        <p style="margin: 3px 0 0 0; font-size: 11.5px; font-weight: 600; color: #475569;">
          Registros desagregados con ordenamiento dinámico por columnas y paginación
        </p>
      </div>
      <div style="display: flex; gap: 10px; align-items: center;">
        <input type="text" id="pbi-search-input" placeholder="🔍 Buscar municipio o variedad..." style="padding: 6px 12px; font-size: 12.5px; font-weight: 600; border: 2px solid #0f172a; border-radius: 6px; width: 220px; outline: none; color: #0f172a;" />
        <span id="pbi-table-info" style="font-size: 12px; font-weight: 700; color: #0f172a;">Mostrando 0 registros</span>
      </div>
    </div>

    <!-- TABLE ELEMENT -->
    <div style="overflow-x: auto; border: 2px solid #0f172a; border-radius: 6px;">
      <table style="width: 100%; border-collapse: collapse; font-size: 12.5px; text-align: left; background-color: #ffffff;">
        <thead>
          <tr style="background-color: #0f172a; color: #ffffff; font-weight: 800; text-transform: uppercase; font-size: 11.5px; letter-spacing: 0.3px;">
            <th id="th-depto" style="padding: 10px 14px; border: 1px solid #334155; cursor: pointer;">Departamento ⇕</th>
            <th id="th-mpio" style="padding: 10px 14px; border: 1px solid #334155; cursor: pointer;">Municipio ⇕</th>
            <th id="th-var" style="padding: 10px 14px; border: 1px solid #334155; cursor: pointer;">Variedad ⇕</th>
            <th id="th-anio" style="padding: 10px 14px; border: 1px solid #334155; cursor: pointer; text-align: center;">Año ⇕</th>
            <th id="th-prod" style="padding: 10px 14px; border: 1px solid #334155; cursor: pointer; text-align: right;">Producción (t) ⇕</th>
            <th id="th-area" style="padding: 10px 14px; border: 1px solid #334155; cursor: pointer; text-align: right;">Área (ha) ⇕</th>
            <th id="th-rend" style="padding: 10px 14px; border: 1px solid #334155; cursor: pointer; text-align: right;">Rend. (t/ha) ⇕</th>
            <th id="th-precio" style="padding: 10px 14px; border: 1px solid #334155; cursor: pointer; text-align: right;">Precio ($/kg) ⇕</th>
          </tr>
        </thead>
        <tbody id="pbi-table-body">
          <!-- Populated by JS -->
        </tbody>
      </table>
    </div>

    <!-- PAGINATION CONTROLS -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
      <div style="font-size: 12px; font-weight: 700; color: #0f172a;">
        Página <span id="pbi-current-page">1</span> de <span id="pbi-total-pages">1</span>
      </div>
      <div style="display: flex; gap: 8px;">
        <button id="pbi-btn-prev" style="background-color: #0f172a; color: #ffffff; border: none; padding: 6px 14px; border-radius: 4px; font-size: 12px; font-weight: 700; cursor: pointer;">
          ◀ Anterior
        </button>
        <button id="pbi-btn-next" style="background-color: #0f172a; color: #ffffff; border: none; padding: 6px 14px; border-radius: 4px; font-size: 12px; font-weight: 700; cursor: pointer;">
          Siguiente ▶
        </button>
      </div>
    </div>
  </div>

  <!-- TOOLTIP FLOTANTE -->
  <div id="pbi-tooltip" style="position: fixed; display: none; background: #0f172a; color: #ffffff; padding: 8px 12px; border-radius: 6px; font-size: 11.5px; font-weight: 600; pointer-events: none; z-index: 99999; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 1px solid #475569;">
  </div>

</div>

<!-- EMBEDDED JAVASCRIPT POWER BI ENGINE -->
<script>
(function() {{
  // EMBEDDED PAYLOAD
  const DATA = {data_json_str};

  // APPLICATION STATE
  const state = {{
    hierarchy: 'nacional', // 'nacional' | 'departamento'
    selectedDepto: 'all',
    selectedVar: 'all',
    selectedAnio: 'all',
    searchQuery: '',
    sortCol: 'prod',
    sortAsc: false,
    currentPage: 1,
    rowsPerPage: 10
  }};

  // EXTRACT UNIQUE DEPARTMENTS
  const deptosSet = new Set();
  DATA.eva.forEach(r => deptosSet.add(r[0]));
  const deptoList = Array.from(deptosSet).sort();

  // POPULATE DEPARTMENTS SELECTOR
  const deptoSelect = document.getElementById('pbi-slicer-depto');
  deptoList.forEach(d => {{
    const opt = document.createElement('option');
    opt.value = d;
    opt.textContent = d;
    deptoSelect.appendChild(opt);
  }});

  // ELEMENTS
  const anioSelect = document.getElementById('pbi-slicer-anio');
  const varSelect = document.getElementById('pbi-slicer-var');
  const btnReset = document.getElementById('pbi-btn-reset');
  const btnDrillUp = document.getElementById('pbi-btn-drillup');
  const bcNacional = document.getElementById('pbi-bc-nacional');
  const bcDepto = document.getElementById('pbi-bc-depto');
  const statusIndicator = document.getElementById('pbi-status-indicator');
  const searchInput = document.getElementById('pbi-search-input');
  const btnPrev = document.getElementById('pbi-btn-prev');
  const btnNext = document.getElementById('pbi-btn-next');
  const tooltip = document.getElementById('pbi-tooltip');

  // FORMATTERS
  function fmtNum(n) {{ return n.toLocaleString('es-CO'); }}
  function fmtDec(n, d=1) {{ return Number(n).toLocaleString('es-CO', {{ minimumFractionDigits: d, maximumFractionDigits: d }}); }}

  // TOOLTIP HELPERS
  function showTip(e, text) {{
    tooltip.innerHTML = text;
    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX + 14) + 'px';
    tooltip.style.top = (e.clientY + 14) + 'px';
  }}
  function hideTip() {{
    tooltip.style.display = 'none';
  }}

  // FILTER ENGINE
  function getFilteredData() {{
    // Filter EVA: [depto, mpio, var, anio, prod, area, rend]
    const filteredEVA = DATA.eva.filter(r => {{
      const d = r[0];
      const m = r[1];
      const v = r[2];
      const a = r[3];

      if (state.selectedDepto !== 'all' && d !== state.selectedDepto) return false;
      if (state.selectedVar !== 'all' && v !== state.selectedVar) return false;
      if (state.selectedAnio !== 'all' && a != state.selectedAnio) return false;
      return true;
    }});

    // Filter SIPSA: [depto, var, anio, precio, vol]
    const filteredSIPSA = DATA.sipsa.filter(r => {{
      const d = r[0];
      const v = r[1];
      const a = r[2];

      if (state.selectedDepto !== 'all' && d !== state.selectedDepto) return false;
      if (state.selectedVar !== 'all' && v !== state.selectedVar) return false;
      if (state.selectedAnio !== 'all' && a != state.selectedAnio) return false;
      return true;
    }});

    // Filter Monthly: [depto, anio, mes, precio, vol]
    const filteredMonthly = DATA.monthly.filter(r => {{
      const d = r[0];
      const a = r[1];

      if (state.selectedDepto !== 'all' && d !== state.selectedDepto) return false;
      if (state.selectedAnio !== 'all' && a != state.selectedAnio) return false;
      return true;
    }});

    return {{ eva: filteredEVA, sipsa: filteredSIPSA, monthly: filteredMonthly }};
  }}

  // PRICE LOOKUP HELPER
  const priceMap = new Map();
  DATA.sipsa.forEach(r => {{
    // key: depto_var_anio
    priceMap.set(`${{r[0]}}_${{r[1]}}_${{r[2]}}`, r[3]);
  }});

  // RENDER FUNCTION
  function render() {{
    const {{ eva, sipsa, monthly }} = getFilteredData();

    // 1. UPDATE NAVIGATION & BREADCRUMBS
    if (state.hierarchy === 'nacional') {{
      bcDepto.textContent = state.selectedDepto === 'all' ? '📍 Todos los Departamentos' : `📍 ${{state.selectedDepto}}`;
      bcDepto.style.fontWeight = '700';
      bcDepto.style.color = state.selectedDepto === 'all' ? '#0f172a' : '#0369a1';
      btnDrillUp.style.display = 'none';
      statusIndicator.textContent = state.selectedDepto === 'all' ? 'Vista: Consolidado Nacional' : `Filtro: ${{state.selectedDepto}}`;
      document.getElementById('pbi-v1-title').innerHTML = '📊 Producción por Departamento (Haga clic para hacer Drilldown)';
      document.getElementById('pbi-v1-sub').textContent = 'Haga clic sobre una barra departamental para profundizar a nivel municipal';
    }} else {{
      bcDepto.textContent = `📍 ${{state.selectedDepto}}`;
      bcDepto.style.fontWeight = '800';
      bcDepto.style.color = '#0284c7';
      btnDrillUp.style.display = 'inline-flex';
      statusIndicator.textContent = `Drill-Down: Municipios de ${{state.selectedDepto}}`;
      document.getElementById('pbi-v1-title').innerHTML = `🏙️ Top Municipios de ${{state.selectedDepto}} (Drill-Down Municipal)`;
      document.getElementById('pbi-v1-sub').textContent = 'Haga clic en "Subir Nivel" o "Nacional" para volver a departamentos';
    }}

    // Sincronizar selectores
    deptoSelect.value = state.selectedDepto;
    anioSelect.value = state.selectedAnio;
    varSelect.value = state.selectedVar;

    // 2. CALCULATE KPIS
    let totalProd = 0;
    let totalArea = 0;
    eva.forEach(r => {{
      totalProd += r[4];
      totalArea += r[5];
    }});
    const avgRend = totalArea > 0 ? (totalProd / totalArea) : 0;

    let sumPrecio = 0;
    let countPrecio = 0;
    let totalVolumen = 0;
    sipsa.forEach(r => {{
      sumPrecio += r[3];
      countPrecio++;
      totalVolumen += r[4];
    }});
    const avgPrecio = countPrecio > 0 ? Math.round(sumPrecio / countPrecio) : 0;

    document.getElementById('pbi-kpi-prod').textContent = `${{fmtDec(totalProd / 1000, 1)}} kt`;
    document.getElementById('pbi-kpi-area').textContent = `${{fmtNum(Math.round(totalArea))}} ha`;
    document.getElementById('pbi-kpi-rend').textContent = `${{fmtDec(avgRend, 2)}} t/ha`;
    document.getElementById('pbi-kpi-precio').textContent = avgPrecio > 0 ? `$ ${{fmtNum(avgPrecio)}}` : 'N/D';
    document.getElementById('pbi-kpi-volumen').textContent = `${{fmtNum(Math.round(totalVolumen))}} t`;

    // 3. RENDER VISUAL 1: HIERARCHICAL DRILLDOWN BARS
    const v1Container = document.getElementById('pbi-v1-chart-container');
    v1Container.innerHTML = '';

    let v1Data = [];
    if (state.hierarchy === 'nacional') {{
      // Group by depto
      const dMap = new Map();
      eva.forEach(r => {{
        dMap.set(r[0], (dMap.get(r[0]) || 0) + r[4]);
      }});
      v1Data = Array.from(dMap.entries())
        .map(([name, prod]) => ({{ name, prod }}))
        .sort((a, b) => b.prod - a.prod)
        .slice(0, 8);
    }} else {{
      // Group by municipio in selected depto
      const mMap = new Map();
      eva.filter(r => r[0] === state.selectedDepto).forEach(r => {{
        mMap.set(r[1], (mMap.get(r[1]) || 0) + r[4]);
      }});
      v1Data = Array.from(mMap.entries())
        .map(([name, prod]) => ({{ name, prod }}))
        .sort((a, b) => b.prod - a.prod)
        .slice(0, 10);
    }}

    const maxProd = v1Data.length > 0 ? Math.max(...v1Data.map(d => d.prod)) : 1;

    if (v1Data.length === 0) {{
      v1Container.innerHTML = '<div style="text-align: center; color: #64748b; font-weight: 700; margin-top: 80px;">No se encontraron registros con los filtros seleccionados.</div>';
    }} else {{
      v1Data.forEach(item => {{
        const pct = ((item.prod / maxProd) * 100).toFixed(1);
        const row = document.createElement('div');
        row.style.display = 'flex';
        row.style.alignItems = 'center';
        row.style.marginBottom = '8px';
        row.style.cursor = 'pointer';
        row.style.transition = 'background 0.15s ease';
        row.style.padding = '4px 6px';
        row.style.borderRadius = '4px';

        row.onmouseover = (e) => {{
          row.style.backgroundColor = '#e2e8f0';
          showTip(e, `<strong>${{item.name}}</strong><br/>Producción: ${{fmtNum(Math.round(item.prod))}} t<br/>${{state.hierarchy === 'nacional' ? '👉 Haga clic para ver municipios' : '👉 Municipio principal'}}`);
        }};
        row.onmousemove = (e) => {{
          tooltip.style.left = (e.clientX + 14) + 'px';
          tooltip.style.top = (e.clientY + 14) + 'px';
        }};
        row.onmouseout = () => {{
          row.style.backgroundColor = 'transparent';
          hideTip();
        }};

        // Click handler -> DRILLDOWN!
        row.onclick = () => {{
          if (state.hierarchy === 'nacional') {{
            state.hierarchy = 'departamento';
            state.selectedDepto = item.name;
          }} else {{
            // Filter by search of this municipality
            state.searchQuery = item.name;
            searchInput.value = item.name;
          }}
          state.currentPage = 1;
          render();
        }};

        const label = document.createElement('div');
        label.style.width = '120px';
        label.style.fontSize = '12px';
        label.style.fontWeight = '800';
        label.style.color = '#0f172a';
        label.style.whiteSpace = 'nowrap';
        label.style.overflow = 'hidden';
        label.style.textOverflow = 'ellipsis';
        label.textContent = item.name;

        const barTrack = document.createElement('div');
        barTrack.style.flex = '1';
        barTrack.style.height = '20px';
        barTrack.style.backgroundColor = '#f1f5f9';
        barTrack.style.borderRadius = '4px';
        barTrack.style.overflow = 'hidden';
        barTrack.style.margin = '0 10px';
        barTrack.style.border = '1px solid #cbd5e1';

        const barFill = document.createElement('div');
        barFill.style.width = pct + '%';
        barFill.style.height = '100%';
        barFill.style.backgroundColor = state.hierarchy === 'nacional' ? '#0284c7' : '#0d9488';
        barFill.style.borderRadius = '3px';
        barFill.style.transition = 'width 0.4s ease';

        barTrack.appendChild(barFill);

        const valLabel = document.createElement('div');
        valLabel.style.width = '75px';
        valLabel.style.textAlign = 'right';
        valLabel.style.fontSize = '11.5px';
        valLabel.style.fontWeight = '800';
        valLabel.style.color = '#0f172a';
        valLabel.textContent = `${{fmtDec(item.prod / 1000, 1)}} kt`;

        row.appendChild(label);
        row.appendChild(barTrack);
        row.appendChild(valLabel);
        v1Container.appendChild(row);
      }});
    }}

    // 4. RENDER VISUAL 2: VARIETY COMPOSITION
    const v2Container = document.getElementById('pbi-v2-chart-container');
    v2Container.innerHTML = '';

    const varMap = new Map();
    eva.forEach(r => {{
      varMap.set(r[2], (varMap.get(r[2]) || 0) + r[4]);
    }});
    const v2Data = Array.from(varMap.entries())
      .map(([name, prod]) => ({{ name, prod }}))
      .sort((a, b) => b.prod - a.prod);

    const maxVarProd = v2Data.length > 0 ? Math.max(...v2Data.map(d => d.prod)) : 1;
    const totalVarProd = v2Data.reduce((acc, d) => acc + d.prod, 0);

    const varColors = {{
      'Pastusa': '#0284c7',
      'R-12': '#059669',
      'Criolla': '#d97706',
      'Diacol Capiro': '#7c3aed',
      'Superior': '#db2777',
      'Tuquerreña': '#ea580c',
      'Otras Variedades': '#64748b'
    }};

    v2Data.forEach(item => {{
      const pct = totalVarProd > 0 ? ((item.prod / totalVarProd) * 100).toFixed(1) : 0;
      const widthPct = ((item.prod / maxVarProd) * 100).toFixed(1);
      const isSelected = state.selectedVar === item.name;

      const row = document.createElement('div');
      row.style.display = 'flex';
      row.style.alignItems = 'center';
      row.style.marginBottom = '9px';
      row.style.cursor = 'pointer';
      row.style.padding = '4px 6px';
      row.style.borderRadius = '4px';
      row.style.backgroundColor = isSelected ? '#fef3c7' : 'transparent';
      row.style.border = isSelected ? '1.5px solid #f59e0b' : '1px solid transparent';

      row.onmouseover = (e) => {{
        if (!isSelected) row.style.backgroundColor = '#e2e8f0';
        showTip(e, `<strong>${{item.name}}</strong><br/>Volumen: ${{fmtNum(Math.round(item.prod))}} t<br/>Participación: ${{pct}}%<br/>👉 Clic para filtrar`);
      }};
      row.onmousemove = (e) => {{
        tooltip.style.left = (e.clientX + 14) + 'px';
        tooltip.style.top = (e.clientY + 14) + 'px';
      }};
      row.onmouseout = () => {{
        if (!isSelected) row.style.backgroundColor = 'transparent';
        hideTip();
      }};

      row.onclick = () => {{
        state.selectedVar = state.selectedVar === item.name ? 'all' : item.name;
        state.currentPage = 1;
        render();
      }};

      const label = document.createElement('div');
      label.style.width = '115px';
      label.style.fontSize = '12px';
      label.style.fontWeight = '800';
      label.style.color = '#0f172a';
      label.style.whiteSpace = 'nowrap';
      label.style.overflow = 'hidden';
      label.style.textOverflow = 'ellipsis';
      label.textContent = item.name;

      const barTrack = document.createElement('div');
      barTrack.style.flex = '1';
      barTrack.style.height = '18px';
      barTrack.style.backgroundColor = '#f1f5f9';
      barTrack.style.borderRadius = '4px';
      barTrack.style.overflow = 'hidden';
      barTrack.style.margin = '0 10px';
      barTrack.style.border = '1px solid #cbd5e1';

      const barFill = document.createElement('div');
      barFill.style.width = widthPct + '%';
      barFill.style.height = '100%';
      barFill.style.backgroundColor = varColors[item.name] || '#334155';
      barFill.style.borderRadius = '3px';

      barTrack.appendChild(barFill);

      const valLabel = document.createElement('div');
      valLabel.style.width = '80px';
      valLabel.style.textAlign = 'right';
      valLabel.style.fontSize = '11.5px';
      valLabel.style.fontWeight = '800';
      valLabel.style.color = '#0f172a';
      valLabel.textContent = `${{pct}}% (${{fmtDec(item.prod/1000, 1)}}k)`;

      row.appendChild(label);
      row.appendChild(barTrack);
      row.appendChild(valLabel);
      v2Container.appendChild(row);
    }});

    // 5. RENDER VISUAL 3: MONTHLY TIME SERIES
    const v3Container = document.getElementById('pbi-v3-chart-container');
    v3Container.innerHTML = '';

    // Group monthly data by mes (1 to 12)
    const mData = Array(12).fill(0).map((_, i) => ({{ mes: i + 1, vol: 0, sumP: 0, cntP: 0 }}));
    monthly.forEach(r => {{
      const mIdx = r[2] - 1;
      if (mIdx >= 0 && mIdx < 12) {{
        mData[mIdx].vol += r[4];
        mData[mIdx].sumP += r[3];
        mData[mIdx].cntP++;
      }}
    }});

    const monthNames = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    const maxMVol = Math.max(...mData.map(d => d.vol), 1);
    const avgMPrices = mData.map(d => d.cntP > 0 ? Math.round(d.sumP / d.cntP) : 0);
    const maxMPrice = Math.max(...avgMPrices, 1);

    // Build SVG
    const svgWidth = 850;
    const svgHeight = 170;
    const barW = 34;
    const gap = (svgWidth - 60) / 12;

    let svgHtml = `<svg width="100%" height="100%" viewBox="0 0 ${{svgWidth}} ${{svgHeight}}" preserveAspectRatio="none" style="overflow: visible;">`;

    // Horizontal gridlines
    for (let y = 30; y <= 130; y += 35) {{
      svgHtml += `<line x1="40" y1="${{y}}" x2="${{svgWidth - 20}}" y2="${{y}}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3" />`;
    }}

    // Volume bars
    mData.forEach((d, i) => {{
      const x = 50 + i * gap;
      const barH = (d.vol / maxMVol) * 95;
      const y = 135 - barH;
      const p = avgMPrices[i];

      svgHtml += `
        <rect x="${{x - barW/2}}" y="${{y}}" width="${{barW}}" height="${{barH}}" fill="#0284c7" rx="3" opacity="0.85" style="cursor: pointer;"
              onmouseover="showTipMonth(evt, '${{monthNames[i]}}', ${{Math.round(d.vol)}}, ${{p}})"
              onmouseout="hideTipMonth()"/>
        <text x="${{x}}" y="152" fill="#0f172a" font-size="11" font-weight="800" text-anchor="middle">${{monthNames[i]}}</text>
      `;
    }});

    // Price line path
    let linePath = '';
    const points = [];
    avgMPrices.forEach((p, i) => {{
      const x = 50 + i * gap;
      const y = 135 - (p / maxMPrice) * 95;
      points.push({{ x, y, p }});
      linePath += (i === 0 ? `M ${{x}} ${{y}}` : ` L ${{x}} ${{y}}`);
    }});

    svgHtml += `<path d="${{linePath}}" fill="none" stroke="#ea580c" stroke-width="3" stroke-linecap="round" />`;

    // Price dots
    points.forEach((pt, i) => {{
      svgHtml += `
        <circle cx="${{pt.x}}" cy="${{pt.y}}" r="4.5" fill="#ea580c" stroke="#ffffff" stroke-width="2" style="cursor: pointer;"
                onmouseover="showTipMonth(evt, '${{monthNames[i]}}', ${{Math.round(mData[i].vol)}}, ${{pt.p}})"
                onmouseout="hideTipMonth()" />
      `;
    }});

    svgHtml += `</svg>`;
    v3Container.innerHTML = svgHtml;

    // 6. RENDER VISUAL 4: MATRIX DATA TABLE
    let tableRows = eva.map(r => {{
      const d = r[0];
      const m = r[1];
      const v = r[2];
      const a = r[3];
      const prod = r[4];
      const area = r[5];
      const rend = r[6];
      const pKey = `${{d}}_${{v}}_${{a}}`;
      const precio = priceMap.get(pKey) || 0;
      return {{ d, m, v, a, prod, area, rend, precio }};
    }});

    // Apply search filter
    if (state.searchQuery.trim() !== '') {{
      const q = state.searchQuery.toLowerCase();
      tableRows = tableRows.filter(r => 
        r.d.toLowerCase().includes(q) ||
        r.m.toLowerCase().includes(q) ||
        r.v.toLowerCase().includes(q) ||
        String(r.a).includes(q)
      );
    }}

    // Apply sorting
    tableRows.sort((a, b) => {{
      let valA = a[state.sortCol];
      let valB = b[state.sortCol];
      if (typeof valA === 'string') {{
        return state.sortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
      }} else {{
        return state.sortAsc ? valA - valB : valB - valA;
      }}
    }});

    // Pagination
    const totalRows = tableRows.length;
    const totalPages = Math.max(1, Math.ceil(totalRows / state.rowsPerPage));
    if (state.currentPage > totalPages) state.currentPage = totalPages;

    const startIdx = (state.currentPage - 1) * state.rowsPerPage;
    const pagedRows = tableRows.slice(startIdx, startIdx + state.rowsPerPage);

    document.getElementById('pbi-table-info').textContent = `${{fmtNum(totalRows)}} registros encontrados`;
    document.getElementById('pbi-current-page').textContent = state.currentPage;
    document.getElementById('pbi-total-pages').textContent = totalPages;

    const tbody = document.getElementById('pbi-table-body');
    tbody.innerHTML = '';

    if (pagedRows.length === 0) {{
      tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 20px; font-weight: 700; color: #64748b;">No hay registros para mostrar.</td></tr>';
    }} else {{
      pagedRows.forEach((r, idx) => {{
        const tr = document.createElement('tr');
        tr.style.backgroundColor = idx % 2 === 0 ? '#ffffff' : '#f8fafc';
        tr.style.borderBottom = '1px solid #e2e8f0';
        tr.style.color = '#0f172a';
        tr.style.fontWeight = '600';

        tr.onmouseover = () => tr.style.backgroundColor = '#f1f5f9';
        tr.onmouseout = () => tr.style.backgroundColor = idx % 2 === 0 ? '#ffffff' : '#f8fafc';

        tr.innerHTML = `
          <td style="padding: 8px 12px; border: 1px solid #cbd5e1; font-weight: 800;">${{r.d}}</td>
          <td style="padding: 8px 12px; border: 1px solid #cbd5e1;">${{r.m}}</td>
          <td style="padding: 8px 12px; border: 1px solid #cbd5e1;">${{r.v}}</td>
          <td style="padding: 8px 12px; border: 1px solid #cbd5e1; text-align: center;">${{r.a}}</td>
          <td style="padding: 8px 12px; border: 1px solid #cbd5e1; text-align: right; font-weight: 800; color: #0284c7;">${{fmtNum(Math.round(r.prod))}}</td>
          <td style="padding: 8px 12px; border: 1px solid #cbd5e1; text-align: right;">${{fmtNum(Math.round(r.area))}}</td>
          <td style="padding: 8px 12px; border: 1px solid #cbd5e1; text-align: right; font-weight: 700;">${{fmtDec(r.rend, 1)}}</td>
          <td style="padding: 8px 12px; border: 1px solid #cbd5e1; text-align: right; font-weight: 800; color: #ea580c;">${{r.precio > 0 ? '$ ' + fmtNum(r.precio) : 'N/D'}}</td>
        `;
        tbody.appendChild(tr);
      }});
    }}
  }}

  // MONTH TOOLTIP BRIDGE
  window.showTipMonth = function(e, mes, vol, precio) {{
    const text = `<strong>Mes: ${{mes}}</strong><br/>Volumen SIPSA: ${{fmtNum(vol)}} t<br/>Precio Promedio: ${{precio > 0 ? '$ ' + fmtNum(precio) + ' / kg' : 'N/D'}}`;
    showTip(e, text);
  }};
  window.hideTipMonth = function() {{
    hideTip();
  }};

  // EVENT LISTENERS
  deptoSelect.onchange = (e) => {{
    state.selectedDepto = e.target.value;
    state.hierarchy = state.selectedDepto === 'all' ? 'nacional' : 'departamento';
    state.currentPage = 1;
    render();
  }};

  anioSelect.onchange = (e) => {{
    state.selectedAnio = e.target.value;
    state.currentPage = 1;
    render();
  }};

  varSelect.onchange = (e) => {{
    state.selectedVar = e.target.value;
    state.currentPage = 1;
    render();
  }};

  btnReset.onclick = () => {{
    state.hierarchy = 'nacional';
    state.selectedDepto = 'all';
    state.selectedVar = 'all';
    state.selectedAnio = 'all';
    state.searchQuery = '';
    searchInput.value = '';
    state.sortCol = 'prod';
    state.sortAsc = false;
    state.currentPage = 1;
    render();
  }};

  btnDrillUp.onclick = () => {{
    state.hierarchy = 'nacional';
    state.selectedDepto = 'all';
    state.currentPage = 1;
    render();
  }};

  bcNacional.onclick = () => {{
    state.hierarchy = 'nacional';
    state.selectedDepto = 'all';
    state.currentPage = 1;
    render();
  }};

  searchInput.oninput = (e) => {{
    state.searchQuery = e.target.value;
    state.currentPage = 1;
    render();
  }};

  btnPrev.onclick = () => {{
    if (state.currentPage > 1) {{
      state.currentPage--;
      render();
    }}
  }};

  btnNext.onclick = () => {{
    state.currentPage++;
    render();
  }};

  // TABLE SORTING HANDLERS
  const sortMap = {{
    'th-depto': 'd',
    'th-mpio': 'm',
    'th-var': 'v',
    'th-anio': 'a',
    'th-prod': 'prod',
    'th-area': 'area',
    'th-rend': 'rend',
    'th-precio': 'precio'
  }};

  Object.entries(sortMap).forEach(([thId, colKey]) => {{
    const el = document.getElementById(thId);
    if (el) {{
      el.onclick = () => {{
        if (state.sortCol === colKey) {{
          state.sortAsc = !state.sortAsc;
        }} else {{
          state.sortCol = colKey;
          state.sortAsc = false;
        }}
        render();
      }};
    }}
  }});

  // INITIAL RENDER
  render();

}})();
</script>
"""

with open(root / "scratch/dashboard_component.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print("Generated HTML component in scratch/dashboard_component.html successfully!")
print(f"File size: {len(html_code)/1024:.2f} KB")
