# Blueprint y Guía de Construcción Visual del Dashboard en Power BI
**Proyecto:** Plataforma Analítica Agropecuaria Colombia — Mercado de la Papa (2019–2025)  
**Marco de Trabajo:** SWEBOK v3 | DAMA-BOK v2 | ISO/IEC 25010 | Marco PDCO  
**Resolución Base:** 16:9 Canvas (1280 x 720 px o 1920 x 1080 px)  
**Estilo Visual:** Ejecutivo Corporativo / Agronómico Premium

---

## 1. Sistema de Diseño Global y Paleta Cromática

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SISTEMA CROMÁTICO CORPORATIVO                          │
├─────────────────────┬───────────────┬───────────────────────────────────────┤
│ Rol Visual          │ Color Hex     │ Aplicación en el Dashboard            │
├─────────────────────┼───────────────┼───────────────────────────────────────┤
│ Primario Ejecutivo  │ #1B365D       │ Encabezados, títulos, tarjetas KPI    │
│ Primario Agro       │ #2D6A4F       │ Barras de producción, área cosechada  │
│ Secundario Tierra   │ #8B5E3C       │ Precios mayoristas, Papa Pastusa      │
│ Acento / Criolla    │ #D4A373       │ Papa Criolla, llamadas a la acción    │
│ Alerta / Riesgo     │ #C1121F       │ Alta volatilidad (CV > 35%), caídas   │
│ Neutro Fondo        │ #F8F9FA       │ Fondo del lienzo (Canvas Background)  │
│ Neutro Contenedor   │ #FFFFFF       │ Tarjetas y contenedores (Borde 1px)   │
│ Texto Principal     │ #212529       │ Tipografía regular (Segoe UI Semibold)│
└─────────────────────┴───────────────┴───────────────────────────────────────┘
```

- **Tipografía:** Segoe UI (Familia nativa Power BI).
  - Títulos de Página: 18–20 pt (Bold)
  - Títulos de Visuales: 12 pt (Semibold)
  - Cifras en Tarjetas KPI: 24–28 pt (Bold)
  - Etiquetas y Ejes: 9–10 pt (Regular)
- **Contenedores:** Visuales dentro de tarjetas rectangulares blancas con esquinas redondeadas (Radio: 8px) y sombra tenue (Drop Shadow: 20% opacidad, Blur 4px).

---

## 2. Barra Superior Persistente de Filtros y Navegación

En todas las páginas, la franja superior (`Y: 0`, `Height: 85 px`) contiene:
1. **Logotipo / Título:** *"OBSERVATORIO NACIONAL DE LA PAPA | COLOMBIA 2019-2025"*
2. **Segmentadores (Slicers) en Menú Desplegable:**
   - **Año:** Lista desplegable / botones horizontales (`2019` a `2025`).
   - **Variedad:** Botones de alternancia (`Todas`, `Papa Criolla`, `Papa Pastusa / Suprema`).
   - **Departamento:** Lista desplegable jerárquica (`Dim_Geografia[departamento]`).
   - **Central Mayorista:** Lista desplegable (`Dim_Mercado[mercado_mayorista]`).
3. **Botón de Restablecimiento de Filtros** (Bookmark "Limpiar Filtros").

---

## 3. Arquitectura de Páginas del Reporte

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                 ESTRUCTURA DE NAVEGACIÓN DEL DASHBOARD                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  [1. RESUMEN EJECUTIVO] ──> [2. OFERTA Y PRODUCCIÓN]                        │
│             │                                                               │
│             ├───> [3. ABASTECIMIENTO MAYORISTA]                             │
│             │                                                               │
│             ├───> [4. PRECIOS Y VOLATILIDAD]                                │
│             │                                                               │
│             └───> [5. SIMULADOR Y RECOMENDACIONES]                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### PÁGINA 1: Resumen Ejecutivo y Monitor Macroeconómico

**Objetivo:** Brindar a viceministros, directores gremiales y gerentes una vista 360° en 5 segundos.

#### Fila 1: Tarjetas KPI Estratégicas (`Y: 100`, `Height: 110 px`)
- **Card 1: Producción Total**  
  - Métrica: `[Producción Total Ton]`  
  - Subtexto dinámico: `[Variación Interanual Producción YoY %]` con formato condicional (Verde si > 0, Rojo si < 0).
- **Card 2: Eficiencia Agrícola**  
  - Métrica: `[Rendimiento Promedio Ponderado Ton_Ha]`  
  - Meta de referencia: `20.0 Ton/Ha` (Benchmark nacional).
- **Card 3: Abastecimiento Centrales**  
  - Métrica: `[Abastecimiento Mayorista Total Ton]`  
  - Subtexto: `[Variación Interanual Abastecimiento YoY %]`.
- **Card 4: Precio Mayorista Ponderado**  
  - Métrica: `[Precio Promedio Ponderado $/Kg]`  
  - Subtexto: `[Inflación Interanual Precio YoY %]`.
- **Card 5: Semáforo de Riesgo Sectorial**  
  - Métrica: `[Semáforo de Volatilidad de Precios]`  
  - Color dinámico según CV% (<20% Verde, 20-35% Amarillo, >35% Rojo).

#### Fila 2: Visuales Principales (`Y: 225`, `Height: 460 px`)
- **Visual Izquierdo (Ancho 60%): Gráfico de Líneas y Columnas Agrupadas**  
  - *Título:* "Balance Multianual: Producción Cosechada vs. Precio Mayorista Promedio (2019–2025)"
  - Eje X: `Dim_Tiempo[año]`
  - Eje Y Columna: `[Producción Total Ton]` (Color: `#2D6A4F`)
  - Eje Y Línea: `[Precio Promedio Ponderado $/Kg]` (Color: `#8B5E3C`)
- **Visual Derecho Superior (Ancho 40%): Gráfico de Barras Horizontales**  
  - *Título:* "Top 5 Departamentos por Aporte a la Oferta Nacional"
  - Eje Y: `Dim_Geografia[departamento]`
  - Eje X: `[Producción Total Ton]` (Data labels activadas con `% del total`).
- **Visual Derecho Inferior: Matriz de Alerta Temprana**  
  - Variedad | Producción Ton | Abastecimiento Ton | Precio $/Kg | CV Volatilidad | Estado

---

### PÁGINA 2: Oferta Primaria y Geografía Productiva (EVA 2019–2025)

**Objetivo:** Profundizar en las zonas de cultivo, superficie sembrada y brechas de rendimiento agronómico.

#### Visuales:
1. **Mapa de Formas Coroplético / Mapa Relleno (Izquierda 50%):**
   - Ubicación: `Dim_Geografia[departamento]`
   - Saturación de color: `[Producción Total Ton]` (Gradiente: Verde claro `#D8F3DC` a Verde oscuro `#081C15`).
   - Tooltip: Departamento, `[Producción Total Ton]`, `[Área Cosechada Total Ha]`, `[Rendimiento Promedio Ponderado Ton_Ha]`, `[Tasa de Pérdida Cosecha %]`.
2. **Gráfico de Dispersión / Cuadrante de Rendimiento (Derecha Superior 50%):**
   - Eje X: `[Área Cosechada Total Ha]`
   - Eje Y: `[Rendimiento Promedio Ponderado Ton_Ha]`
   - Tamaño de burbuja: `[Producción Total Ton]`
   - Leyenda: `Dim_Geografia[region_natural]`
   - Líneas de referencia: Rendimiento promedio nacional (19.8 Ton/Ha).
3. **Gráfico de Barras Apiladas (Derecha Inferior):**
   - Eje X: `Dim_Tiempo[año_semestre]`
   - Eje Y: `[Producción Total Ton]`
   - Leyenda: `Dim_Variedad[nombre_variedad]` (Contraste Criolla vs Pastusa/Suprema).

---

### PÁGINA 3: Abastecimiento Mayorista y Dinámica de Demanda (SIPSA)

**Objetivo:** Monitorear el flujo comercial, concentración en hubs urbanos y estacionalidad de llegada.

#### Visuales:
1. **Gráfico de Donut / Treemap (Izquierda 35%):**
   - Categoría: `Dim_Mercado[mercado_mayorista]` (Top 5 + Otros)
   - Valores: `[Abastecimiento Mayorista Total Ton]`
   - Resalta la hegemonía de Corabastos (Bogotá) y Central Mayorista de Antioquia (Medellín).
2. **Gráfico de Líneas - Curvas Estacionales Mensuales (Centro-Derecha 65%):**
   - Eje X: `Dim_Tiempo[nombre_mes]` (Ordenado cronológicamente por `mes` 1 a 12).
   - Eje Y: `[IVE Abastecimiento Promedio]`
   - Leyenda: `Dim_Tiempo[año]`
   - Línea constante: `Y = 1.0` (Línea de equilibrio estacional).
   - Callout visual: Meses de sobreoferta (Julio–Agosto, Noviembre–Diciembre) vs meses de escasez (Marzo–Abril).
3. **Tabla Detallada con Barras de Datos Integradas:**
   - Mercado Mayorista | Volumen Ingreso Ton | Participación % | Consumo Mayorista Per Cápita | Tendencia YoY

---

### PÁGINA 4: Precios, Volatilidad e Inflación Sectorial

**Objetivo:** Análisis econométrico del comportamiento de precios, dispersión y riesgos de mercado.

#### Visuales:
1. **Gráfico de Líneas con Bandas de Volatilidad (Superior 60% del alto):**
   - Eje X: `Dim_Tiempo[año_mes]`
   - Serie Central: `[Precio Promedio Ponderado $/Kg]` (Línea sólida `#1B365D`)
   - Serie Superior: `[Banda Superior Volatilidad (+1 Sigma)]` (Línea punteada `#C1121F`)
   - Serie Inferior: `[Banda Inferior Volatilidad (-1 Sigma)]` (Línea punteada `#2D6A4F`)
   - Área sombreada entre bandas representando el intervalo de confianza empírico.
2. **Gráfico de Barras Agrupadas - Coeficiente de Variación Anual (Inferior Izquierda):**
   - Eje X: `Dim_Tiempo[año]`
   - Eje Y: `[Coeficiente de Variación Precio CV%]`
   - Formato condicional: Barras rojas en años de choque (2020 post-pandemia y 2022 crisis de fertilizantes).
3. **Gráfico de Cascada o Rango Máximo-Mínimo (Inferior Derecha):**
   - `[Spread de Precios Max_Min $/Kg]` por plaza mayorista para visualizar márgenes de intermediación.

---

### PÁGINA 5: Simulador de Choques de Oferta y Matriz Estratégica (What-If)

**Objetivo:** Herramienta interactiva para proyectar el impacto de eventos climáticos o económicos y evaluar recomendaciones de política sectorial.

#### Componentes Interactivos:
1. **Panel de Parámetros What-If (Izquierda 30%):**
   - Slider de Entrada: `Parámetro Choque de Oferta` (-30% a +30%, paso de 5%).
   - Texto Explicativo del Modelo: "Basado en Elasticidad Precio de la Demanda Inelástica ($E_p = -0.42$). Un choque negativo del 10% en oferta genera un incremento del 23.8% en precios al consumidor."
2. **Tarjetas de Impacto Proyectado (Centro Superior):**
   - Precio Actual: `[Precio Promedio Ponderado $/Kg]`
   - Impacto Estimado: `[Impacto Simulado en Precio %]`
   - Precio Proyectado: `[Precio Simulado $/Kg]`
3. **Gráfico Comparativo Pre-Choque vs Post-Choque (Centro Inferior):**
   - Columnas comparativas por variedad mostrando el nuevo nivel de precios simulado.
4. **Matriz Tripartita de Recomendaciones Estratégicas (Derecha 40%):**
   - Tarjetas de texto desplegables con recomendaciones categorizadas:
     - 🏛️ **Sector Público (MinAgricultura / UPRA):** Fondo de estabilización de precios y distritos de riego tecnificados.
     - 👨‍🌾 **Productores (Fedepapa):** Escalonamiento de siembras para mitigar valles del IVE y compras asociativas de fertilizantes.
     - 🏬 **Comercializadores / Agroindustria:** Coberturas financieras forward y almacenamiento refrigerado post-cosecha.

---

## 4. Checklist de Validación Técnica en Power BI

- [x] Modelo en estrella estricto sin relaciones circulares ni bidireccionales ambiguas.
- [x] Claves numéricas enteras para tiempo (`id_tiempo`), mercado (`id_mercado`) y texto normalizado para geografía (`cod_mpio`).
- [x] Nombres de medidas intuitivos entre corchetes `[Medida]` sin espacios en nombres de columnas de tablas de hechos.
- [x] Tablas de hechos sin columnas calculadas pesadas (todas las agregaciones delegadas a DAX dinámico).
- [x] Formatos numéricos y símbolos monetarios estándar aplicados (`$#,##0` y `#,##0.00`).
- [x] Jerarquías drill-down configuradas en Geografía (Departamento -> Municipio) y Tiempo (Año -> Semestre -> Trimestre -> Mes).
