# Especificación de Requerimientos de Software y Ciencia de Datos (SRS)

**Proyecto**: Plataforma Analítica del Mercado de la Papa en Colombia (SIPSA 2019–2025)  
**Marco Metodológico**: CRISP-DM (Cross-Industry Standard Process for Data Mining) & Marco PDCO (PLAN $\rightarrow$ DEVELOPMENT)  
**Estándares Normativos**: IEEE 830 / ISO/IEC/IEEE 29148, SWEBOK v3 (Cap. 1), DAMA-BOK v2, ISO/IEC 25010  
**Ubicación**: [docs/documentos_PDCO/requirements.md](file:///c:/Users/ADAN/OneDrive/Documentos/analisispapamercadoorlando/docs/documentos_PDCO/requirements.md)  
**Versión**: 2.0.0 | **Fecha**: 2026-10-06  

---

## 1. Introducción y Marco Metodológico CRISP-DM

El proyecto adopta formalmente el estándar internacional **CRISP-DM** como ciclo de vida de ciencia de datos, integrándolo con el marco de ingeniería **PDCO** (Plan, Development, Control, Operations). Todas las especificaciones se organizan en torno a las fases del negocio y un proceso técnico secuencial e iterativo estructurado en **7 etapas maestras**:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                     CICLO DE VIDA CRISP-DM & ETAPAS DEL PROCESO                  │
├────────────┬──────────┬────────────┬──────────┬────────────┬──────────┬──────────────┤
│ 1.INGESTION│  2. EDA  │3.VALIDATION│4.CLEANING│ 5.FEATURES │ 6. MODEL │7.VISUALIZAT. │
│ Dataset    │Forma,    │Reglas de   │Saneamiento│Pivoteo,   │Inferencia│Reportes      │
│ Único      │Tendencia,│Negocio:    │Léxico,   │Granularidad│Dual:     │Ejecutivos    │
│ Mensual    │Cullen-   │Ningún      │Imputación│Mensual,    │Paramétrica│Oferta,      │
│ SIPSA      │Frey, Box │Precio Nulo │Gobernanza│Per Cápita  │No Param. │Demanda, Prec.│
└────────────┴──────────┴────────────┴──────────┴────────────┴──────────┴──────────────┘
```

### 1.1 Contexto de Negocio y Pilares Analíticos
El sistema debe modelar analíticamente los 3 pilares del mercado de la papa en Colombia durante 2019–2025:
* **Pilar 1: Análisis Crítico de Oferta**: Producción, cuencas productoras, estacionalidad agrícola, ciclos fenológicos (120 vs 180 días) y producción per cápita.
* **Pilar 2: Análisis Crítico de Demanda**: Volúmenes de abastecimiento, absorción por nodos mayoristas, demanda aparente y consumo per cápita (kg/hab/año).
* **Pilar 3: Comportamiento de Precios**: Dinámica temporal, factores influyentes, dispersión de precios mayoristas e índices de estacionalidad.

### 1.2 Regla de Ingestión: Dataset Único Nacional SIPSA
A partir de los 16 periodos crudos (archivos semestrales y cuatrimestrales en formatos `.csv`, `.dta`, `.sav`, `.sas`), la etapa de ingestión debe compilar un **único dataset canónico unificado** (`dataset_sipsa_mensual_nacional.parquet`) cuya:
1. **Dimensionalidad primaria es el TIEMPO**: Estandarizado estrictamente a nivel **MENSUAL** (`fecha_mes` en formato `YYYY-MM-01` o `Period('M')`), agregando transacciones intradiarias, semanales, cuatrimestrales y semestrales a una escala temporal homogénea.
2. **Granularidad del ESPACIO**: Códigos oficiales DIVIPOLA (`divipola_depto` de 2 dígitos, `divipola_mpio` de 5 dígitos) y Central Mayorista de destino.
3. **Columnas Objetivo del Análisis**: Volúmenes totales en toneladas, precios promedio por kilogramo, precios mínimos y máximos, grupo de alimento, variedad comercial de papa y origen-destino geográfico.

---

## 2. Requerimientos Funcionales por Etapa CRISP-DM

### Etapa 1: Ingestión (Ingestion)
* **RF-001 [Ingestión Políglota de 16 Periodos]**: El sistema debe leer de forma automatizada los archivos fuente en `data/RAW/sipsa/` soportando formatos `.csv` (con delimitadores `,` y `;`), Stata (`.dta`), SPSS (`.sav`) y SAS (`.sas7bdat`), manejando encodings dispares (`latin1`, `utf-8`, `utf-8-sig`).
* **RF-002 [Resolución de Schema Drift]**: El sistema debe armonizar las 6 variantes de cabeceras identificadas en la documentación técnica mapeándolas al esquema canónico común.
* **RF-003 [Construcción del Dataset Único Mensual]**: El sistema debe consolidar todas las fuentes en una única estructura tabular donde cada fila represente la síntesis **mensual** de una variedad en un mercado mayorista específico.
* **RF-004 [Estandarización de Temporalidad Mensual]**: Las fechas de encuestas diarias o marcas de periodo cuatrimestral/semestral deben transformarse a una dimensión mensual continua sin brechas (`YYYY-MM`).

### Etapa 2: Análisis Exploratorio de Datos (EDA)
* **RF-005 [Medidas de Tendencia Central y Forma]**: El sistema debe computar para cada variedad, mercado y periodo: media aritmética, mediana, moda, varianza, desviación estándar, rango intercuartílico (IQR) y desviación absoluta respecto a la mediana (MAD).
* **RF-006 [Diagnóstico de Asimetría y Curtosis (Cullen & Frey)]**: El sistema debe calcular el sesgo (*skewness*, $S$) y la curtosis (*kurtosis*, $K$) y graficar el mapa empírico de Cullen y Frey ($S^2$ vs $K$) para identificar si los precios y volúmenes siguen distribuciones Normal, Lognormal, Gamma, Weibull o Pareto.
* **RF-007 [Visualización de Distribución por Cajas y Bigotes]**: El sistema debe generar diagramas de caja y bigotes (*boxplots*) interactivos y estáticos por año, mes, mercado y variedad comercial para evidenciar dispersión y rangos intercuartílicos.
* **RF-008 [Matrices de Correlación Básicas]**: El sistema debe calcular y graficar matrices de correlación bivariada de Pearson (lineal) y Spearman (monótona / no paramétrica) entre volúmenes ingresados, precios mayoristas y población.

### Etapa 3: Validación (Validation)
* **RF-009 [Regla de Invarianza: Ningún Precio Nulo]**: El sistema debe verificar y hacer cumplir de forma estricta que **ningún registro en la capa procesada contenga valores de precio nulos** (`precio_prom_kg IS NOT NULL`). Cualquier registro con precio faltante debe ser validado contra el protocolo de no nulidad (descarte documentado en auditoría si no posee trazabilidad comercial o cálculo a partir del rango min-max).
* **RF-010 [Validación de Rangos Físicos y Financieros]**: El sistema debe validar que `precio_prom_kg > 0`, `volumen_ton > 0`, y `precio_min_kg <= precio_prom_kg <= precio_max_kg`.
* **RF-011 [Integridad Referencial DIVIPOLA DANE]**: El sistema debe contrastar todos los códigos de municipio contra el catálogo maestro [docs/documentos_tecnicos_estadisticos/catalogo_divipola.md](file:///c:/Users/ADAN/OneDrive/Documentos/analisispapamercadoorlando/docs/documentos_tecnicos_estadisticos/catalogo_divipola.md), verificando que `divipola_mpio` cumpla el patrón `^[0-9]{5}$` y pertenezca a un departamento válido (`divipola_depto` de 2 dígitos con `zfill(2)`).

### Etapa 4: Limpieza y Saneamiento (Cleaning)
* **RF-012 [Sanitización Léxica y Homogenización]**: El sistema debe convertir textos a mayúsculas sostenidas, remover caracteres de control ASCII y acentos diacríticos en nombres de mercados y alimentos.
* **RF-013 [Desambiguación de Homónimos]**: El sistema debe desambiguar municipios homónimos (*La Unión* en Antioquia `05400`, Nariño `52399` o Valle `76400`) utilizando la llave compuesta de procedencia.
* **RF-014 [Persistencia en Capa CLEANED]**: Los datos validados y saneados deben guardarse en `data/CLEANED/` en formato columnar Apache Parquet.

### Etapa 5: Ingeniería de Características (Features)
* **RF-015 [Acople de Denominadores Demográficos DANE]**: El sistema debe extraer las proyecciones de población de [data/RAW/demografía/PPED-AreaNac-2018-2070.xlsx](file:///c:/Users/ADAN/OneDrive/Documentos/analisispapamercadoorlando/data/RAW/demograf%C3%ADa/PPED-AreaNac-2018-2070.xlsx) y estructurarlas para calcular:
  * Consumo Aparente Mayorista Per Cápita: $c_{m,t} = \frac{I_{m,t} - S_{m,t}}{N_{\text{Cab},m,t}} \times 1000$ (kg/hab/mes).
  * Producción Departamental Per Cápita: $q_{d,t} = \frac{Q_{d,t}}{N_{d,t}}$ (ton/hab/año).
* **RF-016 [Índices de Estacionalidad Mensual]**: El sistema debe computar el Índice Estacional de Precios (IEP) y el Índice Estacional de Oferta (IEO) mediante descomposición clásica de series de tiempo con medias móviles de 12 meses.
* **RF-017 [Etiquetado de Anomalías]**: El sistema debe calcular métricas de Tukey IQR y MAD Z-Score modificado, marcando flags booleanos (`es_outlier_iqr`, `es_outlier_mad`) sin destruir la serie original.
* **RF-018 [Persistencia en Capa FEATURES]**: Los datasets multidimensionales deben guardarse en `data/FEATURES/`.

### Etapa 6: Inferencia Estadística y Modelado (Model)
* **RF-019 [Batería de Pruebas Paramétricas]**: El sistema debe ejecutar:
  * Prueba de homocedasticidad de Levene y Bartlett.
  * Análisis de varianza ANOVA de una vía y prueba robusta de Welch ante heterocedasticidad.
  * Pruebas post-hoc de Tukey HSD y Games-Howell.
  * Intervalos de confianza paramétricos t-Student al 95%.
* **RF-020 [Batería de Pruebas No Paramétricas]**: El sistema debe ejecutar:
  * Prueba de homogeneidad de Fligner-Killeen.
  * Prueba de rangos de Kruskal-Wallis entre años y periodos mensuales.
  * Prueba post-hoc de Dunn con ajuste de valor $p$ por Tasa de Falso Descubrimiento (FDR Benjamini-Hochberg).
  * Intervalos de confianza no paramétricos Bootstrap BCa (Bias-Corrected and Accelerated) al 95% con $B \ge 2,000$ réplicas.
* **RF-021 [Persistencia en Capa CURATED]**: Las tablas con estadísticos, valores $p$, grados de libertad e intervalos deben guardarse en `data/CURATED/`.

### Requerimientos de Producción Primaria y Oferta Agrícola (EVA)
* **RF-024 [Ingestión de Evaluaciones Agropecuarias EVA 2019–2025]**: El sistema debe leer de forma automatizada y resiliente el libro de Evaluaciones Agropecuarias Municipales en `data/RAW/eva/20260526_BaseAgricola20192025.xlsx` (`BasePagina` / `BaseSIPRA`), manejando candados de lectura compartida de Windows (`FILE_SHARE_ALL`) y abstrayendo la ingesta hacia Parquet.
* **RF-025 [Saneamiento y Filtrado de Variedades EVA]**: El sistema debe aislar estrictamente `Cultivo == 'Papa'` excluyendo falsos positivos (Papaya, Malanga, Papayuela), y clasificar los 5,574 registros en sus dos categorías maestras: `PAPA TODAS LAS VARIEDADES` (3,869 registros) y `PAPA CRIOLLA` (1,705 registros).
* **RF-026 [Generación de Dataset Canónico EVA Parquet]**: El sistema debe compilar los datos en `data/CLEANED/dataset_eva_agricola_nacional.parquet` con códigos DIVIPOLA estandarizados a 2 y 5 dígitos, auditando que `Área Cosechada <= Área Sembrada` y `Rendimiento = Producción / Área Cosechada`.
* **RF-027 [Integración Multidimensional EVA-SIPSA-DANE]**: El sistema debe calcular en la capa de Features la Producción Primaria Oficial Per Cápita (cruzada con proyecciones DANE) y estimar el Coeficiente de Transición Campo a Central Mayorista (Volumen SIPSA / Producción EVA).

---

## 3. Requerimientos No Funcionales (RNF) — ISO/IEC 25010 & DAMA-BOK

| ID | Dimensión | Criterio de Aceptación | Métrica |
|:---|:---|:---|:---|
| **RNF-001** | **Integridad de Datos** | La tasa de precios nulos en el dataset SIPSA unificado debe ser estrictamente cero. | $\text{Precios Nulos} = 0\%$ |
| **RNF-002** | **Granularidad Temporal** | Toda transacción debe mapearse a una dimensión mensual `YYYY-MM`. | Registros con fecha mensual no válida = 0 |
| **RNF-003** | **Eficiencia en Memoria** | Uso de lectura por bloques (*chunking*) y tipos categóricos y enteros compactos en Pandas/PyArrow. | Consumo RAM pico $\le 4.0$ GB |
| **RNF-004** | **Calidad de Código** | Adherencia estricta a PEP 8 y Clean Code en todos los archivos `.py` de `src/`. | Puntuación Flake8 con 0 errores críticos |
| **RNF-005** | **Reproducibilidad** | Cuadernos Jupyter con instalación automatizada y ejecución secuencial sin dependencias ocultas. | Ejecución *Restart & Run All* al 100% |
| **RNF-006** | **Rendimiento de E/S** | Uso de formato Parquet con compresión Snappy en capas intermedias. | Reducción de almacenamiento $\ge 70\%$ frente a CSV |

---

## 4. Matriz de Entidades y Columnas del Dataset Único Mensual

El dataset único nacional generado en la etapa de ingestión debe ajustarse al siguiente diccionario de variables:

| Nombre de Columna | Tipo de Dato | Nullable | Restricción / Formato | Rol en el Análisis |
|:---|:---:|:---:|:---|:---|
| `fecha_mes` | `DATE / STRING` | NO | `YYYY-MM-01` | **Eje Dimensional Primario (Tiempo)** |
| `año` | `INT16` | NO | $2019 \le \text{año} \le 2025$ | Dimensión temporal anual |
| `mes` | `INT8` | NO | $1 \le \text{mes} \le 12$ | Dimensión temporal mensual |
| `divipola_depto` | `STRING` | NO | Regex `^[0-9]{2}$` (zfill 2) | Procedencia departamental |
| `nombre_depto` | `STRING` | NO | Mayúsculas sostenidas | Nombre del departamento productor |
| `divipola_mpio` | `STRING` | NO | Regex `^[0-9]{5}$` (zfill 5) | Procedencia municipal (Cuenca) |
| `nombre_mpio` | `STRING` | NO | Mayúsculas sostenidas | Nombre del municipio productor |
| `mercado_mayorista`| `STRING` | NO | Mayúsculas sostenidas | Central de abastos de destino |
| `divipola_mercado` | `STRING` | NO | Regex `^[0-9]{5}$` | DIVIPOLA del nodo consumidor |
| `alimento` | `STRING` | NO | `'PAPA'` | Filtro canónico del producto |
| `variedad_papa` | `STRING` | NO | Capiro, Pastusa, Criolla, etc. | Estratificación comercial |
| `volumen_ingreso_ton`| `FLOAT32`| NO | $> 0$ | Medida de oferta / abastecimiento |
| `precio_prom_kg` | `FLOAT32` | **NO** | $> 0$ (Invariante estricta) | Variable objetivo de precios |
| `precio_min_kg` | `FLOAT32` | **NO** | $> 0$ | Dispersión inferior |
| `precio_max_kg` | `FLOAT32` | **NO** | $\ge \text{precio\_min\_kg}$ | Dispersión superior |
