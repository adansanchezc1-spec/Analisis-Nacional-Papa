
(function() {
  // EMBEDDED PAYLOAD
  const DATA = /* %%PAYLOAD_JSON%% */ null;

  // APPLICATION STATE
  const state = {
    hierarchy: 'nacional', // 'nacional' | 'departamento'
    selectedDepto: 'all',
    selectedVar: 'all',
    selectedAnio: 'all',
    searchQuery: '',
    sortCol: 'prod',
    sortAsc: false,
    currentPage: 1,
    rowsPerPage: 10
  };

  // EXTRACT UNIQUE DEPARTMENTS (ORDERED BY PRODUCTION VOLUME - ECONOMIC HIERARCHY)
  const deptoProdMap = new Map();
  DATA.eva.forEach(r => {
    deptoProdMap.set(r[0], (deptoProdMap.get(r[0]) || 0) + r[7]);
  });
  const deptoList = Array.from(deptoProdMap.keys()).sort((a, b) => deptoProdMap.get(b) - deptoProdMap.get(a));

  // POPULATE DEPARTMENTS SELECTOR
  const deptoSelect = document.getElementById('pbi-slicer-depto');
  deptoList.forEach(d => {
    const opt = document.createElement('option');
    opt.value = d;
    opt.textContent = d;
    deptoSelect.appendChild(opt);
  });

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
  function fmtNum(n) { return Math.round(n).toLocaleString('es-CO'); }
  function fmtDec(n, d=1) { return Number(n).toLocaleString('es-CO', { minimumFractionDigits: d, maximumFractionDigits: d }); }

  // TOOLTIP HELPERS
  function showTip(e, text) {
    tooltip.innerHTML = text;
    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX + 14) + 'px';
    tooltip.style.top = (e.clientY + 14) + 'px';
  }
  function hideTip() {
    tooltip.style.display = 'none';
  }

  // PRICE LOOKUP HELPER: key: depto_var_anio
  const priceMap = new Map();
  DATA.sipsa.forEach(r => {
    priceMap.set(`${r[0]}_${r[1]}_${r[2]}`, r[3]);
  });
  // National price lookup fallback: var_anio
  const natPriceMap = new Map();
  DATA.sipsa.forEach(r => {
    const k = `${r[1]}_${r[2]}`;
    if (!natPriceMap.has(k)) natPriceMap.set(k, []);
    natPriceMap.get(k).push(r[3]);
  });

  function getEstPrice(depto, variedad, anio) {
    const k1 = `${depto}_${variedad}_${anio}`;
    if (priceMap.has(k1)) return priceMap.get(k1);
    const k2 = `${variedad}_${anio}`;
    if (natPriceMap.has(k2)) {
      const arr = natPriceMap.get(k2);
      return Math.round(arr.reduce((a, b) => a + b, 0) / arr.length);
    }
    return 1980; // default estimated price (weighted national average)
  }

  // FILTER ENGINE
  // r in EVA: [depto, mpio, var, anio, areas, areac, efect, prod, rend, pheno]
  function getFilteredData() {
    const filteredEVA = DATA.eva.filter(r => {
      const d = r[0];
      const m = r[1];
      const v = r[2];
      const a = r[3];

      if (state.selectedDepto !== 'all' && d !== state.selectedDepto) return false;
      if (state.selectedVar !== 'all' && v !== state.selectedVar) return false;
      if (state.selectedAnio !== 'all' && a != state.selectedAnio) return false;
      return true;
    });

    // Monthly: [var, anio, mes, precio, vol]
    const filteredMonthly = DATA.monthly.filter(r => {
      const v = r[0];
      const a = r[1];

      if (state.selectedVar !== 'all' && v !== state.selectedVar) return false;
      if (state.selectedAnio !== 'all' && a != state.selectedAnio) return false;
      return true;
    });

    return { eva: filteredEVA, monthly: filteredMonthly };
  }

  // RENDER FUNCTION
  function render() {
    const { eva, monthly } = getFilteredData();

    // 1. UPDATE NAVIGATION & BREADCRUMBS
    if (state.hierarchy === 'nacional') {
      bcDepto.textContent = state.selectedDepto === 'all' ? '📍 Todos los Departamentos' : `📍 ${state.selectedDepto}`;
      bcDepto.style.fontWeight = '700';
      bcDepto.style.color = state.selectedDepto === 'all' ? '#0f172a' : '#0369a1';
      btnDrillUp.style.display = 'none';
      statusIndicator.textContent = state.selectedDepto === 'all' ? 'Vista: Consolidado Nacional' : `Filtro: ${state.selectedDepto}`;
      document.getElementById('pbi-v1-title').innerHTML = '📊 Producción y Efectividad por Depto (Haga clic para Drilldown)';
      document.getElementById('pbi-v1-sub').textContent = 'Haga clic sobre una barra departamental para profundizar a nivel municipal';
    } else {
      bcDepto.textContent = `📍 ${state.selectedDepto}`;
      bcDepto.style.fontWeight = '800';
      bcDepto.style.color = '#0284c7';
      btnDrillUp.style.display = 'inline-flex';
      statusIndicator.textContent = `Drill-Down: Municipios de ${state.selectedDepto}`;
      document.getElementById('pbi-v1-title').innerHTML = `🏙️ Top Municipios de ${state.selectedDepto} (Siembra, Cosecha y Rendimiento)`;
      document.getElementById('pbi-v1-sub').textContent = 'Haga clic en "Subir Nivel" o "Nacional" para volver a departamentos';
    }

    // Sincronizar selectores
    deptoSelect.value = state.selectedDepto;
    anioSelect.value = state.selectedAnio;
    varSelect.value = state.selectedVar;

    // 2. CALCULATE KPIS
    let totalProd = 0;
    let totalAreaS = 0;
    let totalAreaC = 0;
    let phenoSum = 0;
    let sumWeightedPrice = 0;

    eva.forEach(r => {
      const p = r[7];
      const as_ = r[4];
      const ac_ = r[5];
      const pheno = r[9];
      const estP = getEstPrice(r[0], r[2], r[3]);

      totalProd += p;
      totalAreaS += as_;
      totalAreaC += ac_;
      phenoSum += pheno * p;
      sumWeightedPrice += estP * p;
    });

    const avgRend = totalAreaC > 0 ? (totalProd / totalAreaC) : 0;
    const avgEfect = totalAreaS > 0 ? ((totalAreaC / totalAreaS) * 100) : 100;
    const lostArea = Math.max(0, totalAreaS - totalAreaC);
    const avgPheno = totalProd > 0 ? Math.round(phenoSum / totalProd) : (state.selectedVar === 'Papa Criolla' ? 110 : 165);
    const avgPonderadoPrecio = totalProd > 0 ? Math.round(sumWeightedPrice / totalProd) : 1980;

    document.getElementById('pbi-kpi-prod').textContent = `${fmtDec(totalProd / 1000, 1)} kt`;
    document.getElementById('pbi-kpi-areas').textContent = `${fmtNum(totalAreaS)} ha`;
    document.getElementById('pbi-kpi-areac').textContent = `${fmtNum(totalAreaC)} ha`;
    document.getElementById('pbi-kpi-efect').textContent = `Efectividad: ${fmtDec(avgEfect, 1)}% (-${fmtNum(lostArea)} ha)`;
    document.getElementById('pbi-kpi-rend').textContent = `${fmtDec(avgRend, 2)} t/ha`;
    document.getElementById('pbi-kpi-precio').textContent = `$ ${fmtNum(avgPonderadoPrecio)}`;
    document.getElementById('pbi-kpi-pheno').textContent = `${avgPheno} d`;
    document.getElementById('pbi-kpi-pheno-sub').textContent = avgPheno < 130 ? 'Ciclo Corto (S. phureja)' : 'Ciclo Largo (S. tuberosum)';

    // 3. RENDER VISUAL 1: HIERARCHICAL DRILLDOWN BARS
    const v1Container = document.getElementById('pbi-v1-chart-container');
    v1Container.innerHTML = '';

    let v1Data = [];
    if (state.hierarchy === 'nacional') {
      const dMap = new Map();
      eva.forEach(r => {
        const d = r[0];
        if (!dMap.has(d)) dMap.set(d, { prod: 0, areas: 0, areac: 0 });
        const obj = dMap.get(d);
        obj.prod += r[7];
        obj.areas += r[4];
        obj.areac += r[5];
      });
      v1Data = Array.from(dMap.entries())
        .map(([name, vals]) => ({ name, ...vals }))
        .sort((a, b) => b.prod - a.prod)
        .slice(0, 8);
    } else {
      const mMap = new Map();
      eva.filter(r => r[0] === state.selectedDepto).forEach(r => {
        const m = r[1];
        if (!mMap.has(m)) mMap.set(m, { prod: 0, areas: 0, areac: 0 });
        const obj = mMap.get(m);
        obj.prod += r[7];
        obj.areas += r[4];
        obj.areac += r[5];
      });
      v1Data = Array.from(mMap.entries())
        .map(([name, vals]) => ({ name, ...vals }))
        .sort((a, b) => b.prod - a.prod)
        .slice(0, 10);
    }

    const maxProd = v1Data.length > 0 ? Math.max(...v1Data.map(d => d.prod)) : 1;

    if (v1Data.length === 0) {
      v1Container.innerHTML = '<div style="text-align: center; color: #64748b; font-weight: 700; margin-top: 80px;">No se encontraron registros con los filtros seleccionados.</div>';
    } else {
      v1Data.forEach(item => {
        const pct = ((item.prod / maxProd) * 100).toFixed(1);
        const efectItem = item.areas > 0 ? ((item.areac / item.areas) * 100).toFixed(1) : '100.0';

        const row = document.createElement('div');
        row.style.display = 'flex';
        row.style.alignItems = 'center';
        row.style.marginBottom = '8px';
        row.style.cursor = 'pointer';
        row.style.transition = 'background 0.15s ease';
        row.style.padding = '4px 6px';
        row.style.borderRadius = '4px';

        row.onmouseover = (e) => {
          row.style.backgroundColor = '#e2e8f0';
          showTip(e, `<strong>${item.name}</strong><br/>Producción: ${fmtNum(item.prod)} t<br/>Siembra: ${fmtNum(item.areas)} ha | Cosecha: ${fmtNum(item.areac)} ha<br/>Efectividad: ${efectItem}%<br/>${state.hierarchy === 'nacional' ? '👉 Clic para ver municipios' : '👉 Municipio nodal'}`);
        };
        row.onmousemove = (e) => {
          tooltip.style.left = (e.clientX + 14) + 'px';
          tooltip.style.top = (e.clientY + 14) + 'px';
        };
        row.onmouseout = () => {
          row.style.backgroundColor = 'transparent';
          hideTip();
        };

        row.onclick = () => {
          if (state.hierarchy === 'nacional') {
            state.hierarchy = 'departamento';
            state.selectedDepto = item.name;
          } else {
            state.searchQuery = item.name;
            searchInput.value = item.name;
          }
          state.currentPage = 1;
          render();
        };

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

        barTrack.appendChild(barFill);

        const valLabel = document.createElement('div');
        valLabel.style.width = '85px';
        valLabel.style.textAlign = 'right';
        valLabel.style.fontSize = '11.5px';
        valLabel.style.fontWeight = '800';
        valLabel.style.color = '#0f172a';
        valLabel.textContent = `${fmtDec(item.prod / 1000, 1)} kt`;

        row.appendChild(label);
        row.appendChild(barTrack);
        row.appendChild(valLabel);
        v1Container.appendChild(row);
      });
    }

    // 4. RENDER VISUAL 2: VARIETY COMPOSITION AND PHENOLOGY
    const v2Container = document.getElementById('pbi-v2-chart-container');
    v2Container.innerHTML = '';

    const varMap = new Map();
    eva.forEach(r => {
      const v = r[2];
      const pheno = r[9];
      if (!varMap.has(v)) varMap.set(v, { prod: 0, pheno: pheno });
      varMap.get(v).prod += r[7];
    });
    const v2Data = Array.from(varMap.entries())
      .map(([name, obj]) => ({ name, prod: obj.prod, pheno: obj.pheno }))
      .sort((a, b) => b.prod - a.prod);

    const maxVarProd = v2Data.length > 0 ? Math.max(...v2Data.map(d => d.prod)) : 1;
    const totalVarProd = v2Data.reduce((acc, d) => acc + d.prod, 0);

    const varColors = {
      'Papa Criolla': '#d97706',
      'Papa Superior': '#0284c7',
      'Papa Diacol Capiro': '#7c3aed',
      'Papa Única': '#059669',
      'Papa Parda Pastusa': '#475569',
      'Papa Suprema': '#db2777',
      'Papa Rubí': '#dc2626',
      'Papa R-12': '#ea580c',
      'Papa Betina': '#0891b2',
      'Papa Sabanera': '#65a30d',
      'Papa Nevada': '#4f46e5',
      'Papa Morasurco': '#9333ea',
      'Otras Variedades': '#64748b'
    };

    v2Data.forEach(item => {
      const pct = totalVarProd > 0 ? ((item.prod / totalVarProd) * 100).toFixed(1) : '0';
      const widthPct = ((item.prod / maxVarProd) * 100).toFixed(1);
      const isSelected = state.selectedVar === item.name;

      const row = document.createElement('div');
      row.style.display = 'flex';
      row.style.alignItems = 'center';
      row.style.marginBottom = '6px';
      row.style.cursor = 'pointer';
      row.style.padding = '3px 6px';
      row.style.borderRadius = '4px';
      row.style.backgroundColor = isSelected ? '#fef3c7' : 'transparent';
      row.style.border = isSelected ? '1.5px solid #f59e0b' : '1px solid transparent';

      row.onmouseover = (e) => {
        if (!isSelected) row.style.backgroundColor = '#e2e8f0';
        showTip(e, `<strong>${item.name}</strong><br/>Volumen: ${fmtNum(item.prod)} t (${pct}%)<br/>Ciclo Fenológico: ${item.pheno} días<br/>👉 Clic para filtrar este tipo de papa`);
      };
      row.onmousemove = (e) => {
        tooltip.style.left = (e.clientX + 14) + 'px';
        tooltip.style.top = (e.clientY + 14) + 'px';
      };
      row.onmouseout = () => {
        if (!isSelected) row.style.backgroundColor = 'transparent';
        hideTip();
      };

      row.onclick = () => {
        state.selectedVar = state.selectedVar === item.name ? 'all' : item.name;
        state.currentPage = 1;
        render();
      };

      const label = document.createElement('div');
      label.style.width = '125px';
      label.style.fontSize = '11.5px';
      label.style.fontWeight = '800';
      label.style.color = '#0f172a';
      label.style.whiteSpace = 'nowrap';
      label.style.overflow = 'hidden';
      label.style.textOverflow = 'ellipsis';
      label.textContent = item.name;

      const barTrack = document.createElement('div');
      barTrack.style.flex = '1';
      barTrack.style.height = '16px';
      barTrack.style.backgroundColor = '#f1f5f9';
      barTrack.style.borderRadius = '3px';
      barTrack.style.overflow = 'hidden';
      barTrack.style.margin = '0 8px';
      barTrack.style.border = '1px solid #cbd5e1';

      const barFill = document.createElement('div');
      barFill.style.width = widthPct + '%';
      barFill.style.height = '100%';
      barFill.style.backgroundColor = varColors[item.name] || '#334155';
      barFill.style.borderRadius = '2px';

      barTrack.appendChild(barFill);

      const valLabel = document.createElement('div');
      valLabel.style.width = '95px';
      valLabel.style.textAlign = 'right';
      valLabel.style.fontSize = '11px';
      valLabel.style.fontWeight = '800';
      valLabel.style.color = '#0f172a';
      valLabel.textContent = `${pct}% (${item.pheno}d)`;

      row.appendChild(label);
      row.appendChild(barTrack);
      row.appendChild(valLabel);
      v2Container.appendChild(row);
    });

    // 5. RENDER VISUAL 3: MONTHLY TIME SERIES AND PHENOLOGICAL PRICE LAG
    const v3Container = document.getElementById('pbi-v3-chart-container');
    v3Container.innerHTML = '';

    const mData = Array(12).fill(0).map((_, i) => ({ mes: i + 1, vol: 0, sumP: 0, cntP: 0 }));
    monthly.forEach(r => {
      const mIdx = r[2] - 1;
      if (mIdx >= 0 && mIdx < 12) {
        mData[mIdx].vol += r[4];
        mData[mIdx].sumP += r[3];
        mData[mIdx].cntP++;
      }
    });

    const monthNames = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    const maxMVol = Math.max(...mData.map(d => d.vol), 1);
    const avgMPrices = mData.map(d => d.cntP > 0 ? Math.round(d.sumP / d.cntP) : 2650);
    const maxMPrice = Math.max(...avgMPrices, 1);
    const minMPrice = Math.min(...avgMPrices, 1000);

    const svgWidth = 850;
    const svgHeight = 170;
    const barW = 34;
    const gap = (svgWidth - 60) / 12;

    let svgHtml = `<svg width="100%" height="100%" viewBox="0 0 ${svgWidth} ${svgHeight}" preserveAspectRatio="none" style="overflow: visible;">`;

    for (let y = 30; y <= 130; y += 35) {
      svgHtml += `<line x1="40" y1="${y}" x2="${svgWidth - 20}" y2="${y}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3" />`;
    }

    // Volume bars
    mData.forEach((d, i) => {
      const x = 50 + i * gap;
      const barH = (d.vol / maxMVol) * 95;
      const y = 135 - barH;
      const p = avgMPrices[i];

      svgHtml += `
        <rect x="${x - barW/2}" y="${y}" width="${barW}" height="${barH}" fill="#0284c7" rx="3" opacity="0.85" style="cursor: pointer;"
              onmouseover="showTipMonth(evt, '${monthNames[i]}', ${Math.round(d.vol)}, ${p})"
              onmouseout="hideTipMonth()"/>
        <text x="${x}" y="152" fill="#0f172a" font-size="11" font-weight="800" text-anchor="middle">${monthNames[i]}</text>
      `;
    });

    // Price line
    let linePath = '';
    const points = [];
    avgMPrices.forEach((p, i) => {
      const x = 50 + i * gap;
      const normalizedP = (p - minMPrice) / Math.max(1, (maxMPrice - minMPrice));
      const y = 130 - (normalizedP * 90);
      points.push({ x, y, p });
      linePath += (i === 0 ? `M ${x} ${y}` : ` L ${x} ${y}`);
    });

    svgHtml += `<path d="${linePath}" fill="none" stroke="#ea580c" stroke-width="3.5" stroke-linecap="round" />`;

    points.forEach((pt, i) => {
      svgHtml += `
        <circle cx="${pt.x}" cy="${pt.y}" r="4.5" fill="#ea580c" stroke="#ffffff" stroke-width="2" style="cursor: pointer;"
                onmouseover="showTipMonth(evt, '${monthNames[i]}', ${Math.round(mData[i].vol)}, ${pt.p})"
                onmouseout="hideTipMonth()" />
      `;
    });

    svgHtml += `</svg>`;
    v3Container.innerHTML = svgHtml;

    // 6. RENDER VISUAL 4: MATRIX DATA TABLE
    let tableRows = eva.map(r => {
      const d = r[0];
      const m = r[1];
      const v = r[2];
      const a = r[3];
      const areas = r[4];
      const areac = r[5];
      const efect = r[6];
      const prod = r[7];
      const rend = r[8];
      const pheno = r[9];
      const precio = getEstPrice(d, v, a);
      return { d, m, v, pheno, a, areas, areac, efect, prod, rend, precio };
    });

    if (state.searchQuery.trim() !== '') {
      const q = state.searchQuery.toLowerCase();
      tableRows = tableRows.filter(r => 
        r.d.toLowerCase().includes(q) ||
        r.m.toLowerCase().includes(q) ||
        r.v.toLowerCase().includes(q) ||
        String(r.a).includes(q)
      );
    }

    tableRows.sort((a, b) => {
      let valA = a[state.sortCol];
      let valB = b[state.sortCol];
      if (typeof valA === 'string') {
        return state.sortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
      } else {
        return state.sortAsc ? valA - valB : valB - valA;
      }
    });

    const totalRows = tableRows.length;
    const totalPages = Math.max(1, Math.ceil(totalRows / state.rowsPerPage));
    if (state.currentPage > totalPages) state.currentPage = totalPages;

    const startIdx = (state.currentPage - 1) * state.rowsPerPage;
    const pagedRows = tableRows.slice(startIdx, startIdx + state.rowsPerPage);

    document.getElementById('pbi-table-info').textContent = `${fmtNum(totalRows)} registros encontrados`;
    document.getElementById('pbi-current-page').textContent = state.currentPage;
    document.getElementById('pbi-total-pages').textContent = totalPages;

    const tbody = document.getElementById('pbi-table-body');
    tbody.innerHTML = '';

    if (pagedRows.length === 0) {
      tbody.innerHTML = '<tr><td colspan="11" style="text-align: center; padding: 20px; font-weight: 700; color: #64748b;">No hay registros para mostrar con los filtros seleccionados.</td></tr>';
    } else {
      pagedRows.forEach((r, idx) => {
        const tr = document.createElement('tr');
        tr.style.backgroundColor = idx % 2 === 0 ? '#ffffff' : '#f8fafc';
        tr.style.borderBottom = '1px solid #e2e8f0';
        tr.style.color = '#0f172a';
        tr.style.fontWeight = '600';

        tr.onmouseover = () => tr.style.backgroundColor = '#f1f5f9';
        tr.onmouseout = () => tr.style.backgroundColor = idx % 2 === 0 ? '#ffffff' : '#f8fafc';

        tr.innerHTML = `
          <td style="padding: 7px 10px; border: 1px solid #cbd5e1; font-weight: 800;">${r.d}</td>
          <td style="padding: 7px 10px; border: 1px solid #cbd5e1;">${r.m}</td>
          <td style="padding: 7px 10px; border: 1px solid #cbd5e1; font-weight: 700;">${r.v}</td>
          <td style="padding: 7px 10px; border: 1px solid #cbd5e1; text-align: center; font-weight: 800; color: #d97706;">${r.pheno}d</td>
          <td style="padding: 7px 10px; border: 1px solid #cbd5e1; text-align: center;">${r.a}</td>
          <td style="padding: 7px 10px; border: 1px solid #cbd5e1; text-align: right;">${fmtNum(r.areas)}</td>
          <td style="padding: 7px 10px; border: 1px solid #cbd5e1; text-align: right;">${fmtNum(r.areac)}</td>
          <td style="padding: 7px 10px; border: 1px solid #cbd5e1; text-align: right; font-weight: 800; color: ${r.efect >= 95 ? '#16a34a' : '#ea580c'};">${fmtDec(r.efect, 1)}%</td>
          <td style="padding: 7px 10px; border: 1px solid #cbd5e1; text-align: right; font-weight: 800; color: #0284c7;">${fmtNum(r.prod)}</td>
          <td style="padding: 7px 10px; border: 1px solid #cbd5e1; text-align: right; font-weight: 700;">${fmtDec(r.rend, 1)}</td>
          <td style="padding: 7px 10px; border: 1px solid #cbd5e1; text-align: right; font-weight: 800; color: #9333ea;">$ ${fmtNum(r.precio)}</td>
        `;
        tbody.appendChild(tr);
      });
    }
  }

  // MONTH TOOLTIP BRIDGE
  window.showTipMonth = function(e, mes, vol, precio) {
    const text = `<strong>Mes: ${mes}</strong><br/>Volumen SIPSA: ${fmtNum(vol)} t<br/>Precio Promedio: $ ${fmtNum(precio)} / kg`;
    showTip(e, text);
  };
  window.hideTipMonth = function() {
    hideTip();
  };

  // EVENT LISTENERS
  deptoSelect.onchange = (e) => {
    state.selectedDepto = e.target.value;
    state.hierarchy = state.selectedDepto === 'all' ? 'nacional' : 'departamento';
    state.currentPage = 1;
    render();
  };

  anioSelect.onchange = (e) => {
    state.selectedAnio = e.target.value;
    state.currentPage = 1;
    render();
  };

  varSelect.onchange = (e) => {
    state.selectedVar = e.target.value;
    state.currentPage = 1;
    render();
  };

  btnReset.onclick = () => {
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
  };

  btnDrillUp.onclick = () => {
    state.hierarchy = 'nacional';
    state.selectedDepto = 'all';
    state.currentPage = 1;
    render();
  };

  bcNacional.onclick = () => {
    state.hierarchy = 'nacional';
    state.selectedDepto = 'all';
    state.currentPage = 1;
    render();
  };

  searchInput.oninput = (e) => {
    state.searchQuery = e.target.value;
    state.currentPage = 1;
    render();
  };

  btnPrev.onclick = () => {
    if (state.currentPage > 1) {
      state.currentPage--;
      render();
    }
  };

  btnNext.onclick = () => {
    state.currentPage++;
    render();
  };

  // TABLE SORTING HANDLERS
  const sortMap = {
    'th-depto': 'd',
    'th-mpio': 'm',
    'th-var': 'v',
    'th-pheno': 'pheno',
    'th-anio': 'a',
    'th-areas': 'areas',
    'th-areac': 'areac',
    'th-efect': 'efect',
    'th-prod': 'prod',
    'th-rend': 'rend',
    'th-precio': 'precio'
  };

  Object.entries(sortMap).forEach(([thId, colKey]) => {
    const el = document.getElementById(thId);
    if (el) {
      el.onclick = () => {
        if (state.sortCol === colKey) {
          state.sortAsc = !state.sortAsc;
        } else {
          state.sortCol = colKey;
          state.sortAsc = false;
        }
        render();
      };
    }
  });

  // INITIAL RENDER
  render();

})();
