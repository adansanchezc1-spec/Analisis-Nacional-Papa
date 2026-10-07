# Manual de Implementación y Guía de Usuario: Dashboard Power BI
**Proyecto:** Plataforma Analítica Agropecuaria Colombia — Mercado de la Papa (2019–2025)  
**Fase PDCO:** DEVELOPMENT → OPERATIONS | **SDLC Stage:** Deployment & User Enablement  
**Versión:** 1.0.0 | **Fecha:** Octubre 2026  

---

## 1. Introducción y Recursos del Entregable

Este manual describe el procedimiento para desplegar, conectar y visualizar el **Dashboard Ejecutivo en Power BI** con los hallazgos analíticos consolidados de la papa en Colombia (2019–2025).

Todos los activos del proyecto se encuentran organizados en el repositorio:
```
analisispapamercadoorlando/
├── data/
│   └── POWERBI/                        <-- Datasets listos en CSV (UTF-8 con BOM) y Parquet
│       ├── Dim_Tiempo.csv (y .parquet)
│       ├── Dim_Geografia.csv (y .parquet)
│       ├── Dim_Variedad.csv (y .parquet)
│       ├── Dim_Mercado.csv (y .parquet)
│       ├── Fact_Produccion_EVA.csv (y .parquet)
│       ├── Fact_Abastecimiento_SIPSA.csv (y .parquet)
│       └── Fact_Precios_SIPSA.csv (y .parquet)
├── powerbi/
│   ├── data/                           <-- Copia directa de datos para distribución
│   ├── dax_measures.dax                <-- Catálogo completo de 25+ medidas DAX formuladas
│   ├── power_query_m_scripts.pq        <-- Scripts Power Query M para carga con 1 clic
│   ├── model_schema.json               <-- Definición formal del modelo relacional
│   └── dashboard_blueprint.md          <-- Guía de diseño visual y coordenadas por página
└── scripts/
    └── export_powerbi.py               <-- Script Python automatizado para regenerar datos
```

---

## 2. Requisitos Previos

- **Microsoft Power BI Desktop:** Versión de octubre 2023 o superior (gratuito para Windows).
- Acceso a la ruta local del proyecto: `C:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando\`

---

## 3. Procedimiento de Carga de Datos (Paso a Paso)

### Método Recomendado: Uso de Power Query M (Automatizado)

1. **Abrir Power BI Desktop** e iniciar un nuevo informe en blanco.
2. Hacer clic en **"Transformar datos"** en la cinta superior para abrir el **Editor de Power Query**.
3. **Crear el Parámetro de Ruta:**
   - En el menú superior de Power Query: **Nuevo parámetro**.
   - Nombre: `RutaCarpeta`
   - Tipo: `Texto`
   - Valor actual: `C:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando\data\POWERBI`
   - Clic en **Aceptar**.
4. **Crear las Consultas:**
   - Para cada tabla (`Dim_Tiempo`, `Dim_Geografia`, `Dim_Variedad`, `Dim_Mercado`, `Fact_Produccion_EVA`, `Fact_Abastecimiento_SIPSA`, `Fact_Precios_SIPSA`):
     - Hacer clic en **Nueva consulta** -> **Consulta en blanco**.
     - Abrir el **Editor avanzado**.
     - Copiar y pegar el fragmento de código correspondiente desde `powerbi/power_query_m_scripts.pq`.
     - Renombrar la consulta con el nombre exacto de la tabla.
5. Hacer clic en **"Cerrar y aplicar"** en la esquina superior izquierda. Power BI cargará las 7 tablas en el motor VertiPaq.

---

## 4. Configuración de Relaciones en la Vista de Modelo

En la barra lateral izquierda, ir al icono de **"Vista de modelo"** y verificar o trazar las siguientes relaciones de cardinalidad **Varios a Uno (1:*)** con filtro **Único (One Direction)**:

```
[Dim_Tiempo] (id_tiempo) 1 ──< * [Fact_Produccion_EVA] (id_tiempo)
[Dim_Geografia] (cod_mpio) 1 ──< * [Fact_Produccion_EVA] (cod_mpio)
[Dim_Variedad] (cod_variedad) 1 ──< * [Fact_Produccion_EVA] (cod_variedad)

[Dim_Tiempo] (id_tiempo) 1 ──< * [Fact_Abastecimiento_SIPSA] (id_tiempo)
[Dim_Mercado] (id_mercado) 1 ──< * [Fact_Abastecimiento_SIPSA] (id_mercado)
[Dim_Variedad] (cod_variedad) 1 ──< * [Fact_Abastecimiento_SIPSA] (cod_variedad)

[Dim_Tiempo] (id_tiempo) 1 ──< * [Fact_Precios_SIPSA] (id_tiempo)
[Dim_Mercado] (id_mercado) 1 ──< * [Fact_Precios_SIPSA] (id_mercado)
[Dim_Variedad] (cod_variedad) 1 ──< * [Fact_Precios_SIPSA] (cod_variedad)

[Dim_Geografia] (cod_mpio) 1 ──< * [Dim_Mercado] (cod_mpio)
```

---

## 5. Creación de Tabla de Medidas DAX

Para mantener el modelo ordenado según buenas prácticas:
1. En la cinta de inicio: **Especificar datos**.
2. Nombrar la tabla como `_Medidas`. Clic en Cargar.
3. Copiar las fórmulas desde [powerbi/dax_measures.dax](file:///c:/Users/ADAN/OneDrive/Documentos/analisispapamercadoorlando/powerbi/dax_measures.dax) haciendo clic derecho en `_Medidas` -> **Nueva medida**.
4. Organizar en carpetas de visualización (*Display Folders*):
   - `01_KPIs`
   - `02_Time_Intelligence`
   - `03_Volatilidad`
   - `04_Estacionalidad`
   - `05_Concentración`
   - `06_Simulador`

---

## 6. Ensamble de las 5 Páginas Visuales

Siga el detalle milimétrico especificado en [powerbi/dashboard_blueprint.md](file:///c:/Users/ADAN/OneDrive/Documentos/analisispapamercadoorlando/powerbi/dashboard_blueprint.md):

- **Página 1: Resumen Ejecutivo Macroeconómico**
  - Barra superior de filtros de año y variedad.
  - 5 KPI Cards: Producción Total, Rendimiento Ton/Ha, Abastecimiento Ton, Precio $/Kg, Semáforo de Riesgo.
  - Gráfico combinado (Barras de Producción + Línea de Precio).
  - Top 5 Departamentos paperos.
- **Página 2: Oferta Primaria y Eficiencia Agronómica (EVA)**
  - Mapa coroplético departamental con gradiente verde agro (`#2D6A4F`).
  - Gráfico de dispersión de Área Cosechada vs Rendimiento Ton/Ha.
  - Serie semestral comparativa Criolla vs Pastusa/Suprema.
- **Página 3: Dinámica de Abastecimiento Mayorista (SIPSA)**
  - Donut de concentración de hubs urbanos (Corabastos, Antioquia, Cavasa).
  - Curvas de estacionalidad mensual del IVE de oferta ($Y = 1.0$).
- **Página 4: Precios, Volatilidad e Inflación Sectorial**
  - Serie histórica con bandas de Bollinger $\pm 1\sigma$ (`#1B365D`, `#C1121F`, `#2D6A4F`).
  - Coeficiente de variación ($CV\%$) por año.
  - Spreads intradiarios máximos-mínimos.
- **Página 5: Simulador de Choques de Oferta y Matriz Estratégica (What-If)**
  - Parámetro What-If de choque porcentual en oferta (-30% a +30%).
  - Cálculo interactivo de impacto en precios vía elasticidad $E_p = -0.42$.
  - Matriz con recomendaciones estratégicas tripartitas (Público, Productor, Comercializador).

---

## 7. Regeneración Automatizada de Datos

Si en el futuro se actualizan los archivos crudos de SIPSA o EVA:
```powershell
.\.venv\Scripts\python scripts/export_powerbi.py
```
Y luego en Power BI Desktop presionar el botón **"Actualizar"** en la cinta de inicio. Todo el modelo y los visuales se actualizarán instantáneamente sin requerir ningún cambio estructural.
