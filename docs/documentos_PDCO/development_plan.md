# Plan de Desarrollo e Implementación de Software y Ciencia de Datos

**Proyecto**: Plataforma Analítica del Mercado de la Papa en Colombia (SIPSA 2019–2025)  
**Marco de Trabajo**: CRISP-DM & Marco PDCO (Fase **DEVELOPMENT**)  
**Estándares Normativos**: SWEBOK v3, DAMA-BOK v2, ISO/IEC 25010, Clean Architecture, Clean Code, PEP 8  
**Ubicación**: [docs/documentos_PDCO/development_plan.md](file:///c:/Users/ADAN/OneDrive/Documentos/analisispapamercadoorlando/docs/documentos_PDCO/development_plan.md)  
**Versión**: 1.0.0 | **Fecha**: 2026-10-06  

---

## 1. Visión Estratégica del Plan

El presente plan establece la hoja de ruta técnica para implementar la solución analítica del mercado de la papa en Colombia, estructurando el trabajo bajo las **7 etapas del proceso CRISP-DM**:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   SECUENCIA DE LAS 7 ETAPAS CRISP-DM EN DEVELOPMENT              │
├────────────┬──────────┬────────────┬──────────┬────────────┬──────────┬──────────────┤
│ 1.INGESTION│  2. EDA  │3.VALIDATION│4.CLEANING│ 5.FEATURES │ 6. MODEL │7.VISUALIZAT. │
│ Dataset    │Medidas   │Regla Cero  │Saneamiento│Métricas   │Inferencia│Tableros y    │
│ Único      │Forma/Disp│Precios     │Léxico y  │Per Cápita, │Dual:     │Gráficos      │
│ Mensual    │Cullen-   │Nulos       │DIVIPOLA  │IEP, IEO,   │Paramétrica│300 DPI      │
│ SIPSA      │Frey, Box │(Invariante)│(CLEANED) │Lags (FEAT) │No Param. │(CURATED)     │
└────────────┴──────────┴────────────┴──────────┴────────────┴──────────┴──────────────┘
```

La implementación se apoya en una arquitectura dual:
1. **Módulos Reutilizables en `src/`**: Funciones y clases puras, testables y optimizadas en memoria.
2. **Cuadernos Jupyter en `notebooks/`**: Ejecutan cada etapa de forma reproducible con una celda inicial obligatoria de `%pip install`.

---

## 2. Hitos y Entregables por Etapa CRISP-DM

### Hito 1: Etapa de Ingestión (Ingestion) — Construcción de Datasets Únicos (SIPSA y EVA)
* **Objetivo**: Ingerir los 16 periodos crudos de SIPSA y la base agrícola EVA 2019–2025, compilando el **Dataset Único Nacional SIPSA** a nivel mensual y el **Dataset Canónico Agrícola EVA** a nivel semestral.
* **Componentes en `src/`**:
  * `src/infrastructure/readers/factory.py`: Instanciación dinámica del lector según la extensión del archivo.
  * `src/infrastructure/readers/csv_reader.py`, `stata_reader.py`, `spss_reader.py`, `sas_reader.py`.
  * `src/infrastructure/readers/eva_reader.py`: Lector especializado del libro Excel de EVA (`BasePagina`/`BaseSIPRA`).
  * `src/application/ingestion_service.py`: Armonización de SIPSA mensual y extracción de los 5,574 registros de papa de EVA (`Papa todas las variedades` y `Papa criolla`).
* **Cuaderno Asociado**: `notebooks/01_ingestion_dataset_unico.ipynb`.
* **Entregable en Datos**: `data/CLEANED/dataset_sipsa_mensual_nacional.parquet` y `data/CLEANED/dataset_eva_agricola_nacional.parquet`.

---

### Hito 2: Etapa de Análisis Exploratorio de Datos (EDA)
* **Objetivo**: Diagnosticar la estructura profunda de las distribuciones de precios y volúmenes antes de aplicar transformaciones destructivas.
* **Componentes en `src/`**:
  * `src/application/eda_service.py`: Cómputo de medidas de tendencia central (media, mediana, moda), medidas de dispersión (varianza, desviación estándar, IQR, MAD) y medidas de forma (asimetría / *skewness* y curtosis de Fisher).
  * `src/presentation/cullen_frey_plotter.py`: Generación del gráfico de Cullen y Frey ($S^2$ vs $K$) comparando los datos contra las distribuciones teóricas (Normal, Lognormal, Gamma, Weibull).
  * `src/presentation/boxplot_plotter.py`: Construcción de diagramas de caja y bigotes estratificados por año, mes y variedad.
  * `src/presentation/correlation_plotter.py`: Matrices de correlación de Pearson y Spearman entre variables de volumen, precio y población.
* **Cuaderno Asociado**: `notebooks/02_analisis_exploratorio_eda.ipynb`.

---

### Hito 3: Etapa de Validación (Validation)
* **Objetivo**: Asegurar la calidad e integridad referencial de los datos con rigor absoluto bajo directrices **DAMA-BOK**.
* **Componentes en `src/`**:
  * `src/domain/invariants.py`: Implementación de la **Regla de Oro: Ningún precio puede ser nulo** (`precio_prom_kg IS NOT NULL`). Cualquier registro sin precio válido se audita y se excluye del panel de análisis.
  * `src/domain/divipola.py`: Validación de códigos territoriales contra el catálogo maestro oficial [docs/documentos_tecnicos_estadisticos/catalogo_divipola.md](file:///c:/Users/ADAN/OneDrive/Documentos/analisispapamercadoorlando/docs/documentos_tecnicos_estadisticos/catalogo_divipola.md).
  * `src/application/validation_service.py`: Generación de reportes de completitud y consistencia.
* **Cuaderno Asociado**: `notebooks/03_validacion_reglas_negocio.ipynb`.

---

### Hito 4: Etapa de Limpieza y Gobernanza (Cleaning)
* **Objetivo**: Saneamiento de textos, homologación de variedades y persistencia de la capa limpia.
* **Componentes en `src/`**:
  * `src/application/cleaning_service.py`: Eliminación de caracteres especiales, estandarización léxica en mayúsculas, resolución de homónimos (*La Unión* Antioquia vs Nariño vs Valle).
  * `src/infrastructure/writers/parquet_writer.py`: Escritura columnar particionada.
* **Cuaderno Asociado**: `notebooks/04_limpieza_y_gobernanza.ipynb`.
* **Entregable en Datos**: `data/CLEANED/dataset_sipsa_mensual_limpio.parquet`.

---

### Hito 5: Etapa de Ingeniería de Características (Features)
* **Objetivo**: Creación de métricas de mercado avanzadas, estacionalidad y acople demográfico per cápita.
* **Componentes en `src/`**:
  * `src/application/features_service.py`: Cruce con las proyecciones de población DANE de [docs/documentos_tecnicos_estadisticos/plan_extraccion_demografia.md](file:///c:/Users/ADAN/OneDrive/Documentos/analisispapamercadoorlando/docs/documentos_tecnicos_estadisticos/plan_extraccion_demografia.md) para calcular:
    * **Consumo Per Cápita Mensual**: $c_{m,t} = \frac{\text{Ingresos} - \text{Salidas}}{N_{\text{Cab},m,t}} \times 1000$ (kg/hab/mes).
    * **Producción Per Cápita Anual**: $q_{d,t} = \frac{Q_{d,t}}{N_{d,t}}$ (ton/hab/año).
    * **Índices de Estacionalidad**: IEP e IEO mediante descomposición clásica/STL a nivel mensual.
    * **Flags de Anomalías**: Marcado booleano de Tukey IQR y MAD Z-score sin alterar la variabilidad real.
* **Cuaderno Asociado**: `notebooks/05_ingenieria_de_features.ipynb`.
* **Entregable en Datos**: `data/FEATURES/dataset_sipsa_features.parquet`.

---

### Hito 6: Etapa de Modelado e Inferencia Estadística (Model)
* **Objetivo**: Contrastes formales de hipótesis sobre variaciones temporales y espaciales en dos canales estadísticos:
* **Componentes en `src/`**:
  * `src/application/model_service.py`:
    * **Canal Paramétrico**: Prueba de Levene y Bartlett, ANOVA de 1 factor, ANOVA de Welch (robusto ante heterocedasticidad), post-hoc de Tukey HSD y Games-Howell, e intervalos de confianza t-Student al 95%.
    * **Canal No Paramétrico**: Prueba de Fligner-Killeen, prueba de Kruskal-Wallis, contrastes post-hoc de Dunn con ajuste FDR (Benjamini-Hochberg), e Intervalos de Confianza Bootstrap BCa (95%, $B=2,000$ réplicas).
* **Cuaderno Asociado**: `notebooks/06_modelado_e_inferencia_dual.ipynb`.
* **Entregable en Datos**: `data/CURATED/contrastes_estadisticos_anuales.parquet` y `tabla_kpis_consolidados.parquet`.

---

### Hito 7: Etapa de Visualización y Tableros Ejecutivos (Visualization)
* **Objetivo**: Renderizado de figuras de publicación a 300 DPI y síntesis de los 3 pilares del negocio (**Oferta, Demanda y Precios**).
* **Componentes en `src/`**:
  * `src/presentation/reporting_tables.py` y renderizadores en `matplotlib` y `seaborn`.
  * Generación de figuras finales: mapas Cullen-Frey, boxplots interanuales, curvas estacionales de precios y matrices de correlación.
* **Cuaderno Asociado**: `notebooks/07_visualizacion_y_tableros.ipynb`.
* **Entregable en Datos**: `data/CURATED/reportes_graficos/`.

---

## 3. Matriz de Cuadernos Jupyter y Protocolo de Reproducibilidad

Cada cuaderno en `notebooks/` se codificará de forma independiente con un encabezado estándar de instalación idempotente:

| # | Cuaderno Jupyter | Etapa CRISP-DM | Insumos Consumidos | Salidas Generadas |
|---|---|---|---|---|
| 1 | `01_ingestion_dataset_unico.ipynb` | Ingestion | `data/RAW/sipsa/*` (16 periodos) | Dataset unificado con tiempo mensual continuo |
| 2 | `02_analisis_exploratorio_eda.ipynb` | EDA | Dataset consolidado | Gráficos Cullen-Frey, Boxplots, Matrices correlación |
| 3 | `03_validacion_reglas_negocio.ipynb`| Validation | Dataset consolidado | Reporte DAMA-BOK, filtro de cero precios nulos |
| 4 | `04_limpieza_y_gobernanza.ipynb` | Cleaning | Datos validados | `data/CLEANED/dataset_sipsa_mensual_limpio.parquet` |
| 5 | `05_ingenieria_de_features.ipynb` | Features | `CLEANED` + `demografía/` | `data/FEATURES/dataset_sipsa_features.parquet` |
| 6 | `06_modelado_e_inferencia_dual.ipynb`| Model | `data/FEATURES/` | `data/CURATED/contrastes_estadisticos_anuales.parquet` |
| 7 | `07_visualizacion_y_tableros.ipynb`| Visualization | `data/CURATED/` | Figuras a 300 DPI y reporte de los 3 pilares |

### Celda Inicial Obligatoria en Cada Cuaderno:
```python
# ==============================================================================
# CELDA 1 OBLIGATORIA: INSTALACIÓN IDEMPOTENTE DE DEPENDENCIAS EN EL KERNEL
# ==============================================================================
import sys
import subprocess

%pip install --quiet --upgrade pip
%pip install --quiet \
    numpy>=1.24.0 \
    pandas>=2.0.0 \
    scipy>=1.10.0 \
    statsmodels>=0.14.0 \
    scikit-learn>=1.3.0 \
    matplotlib>=3.7.0 \
    seaborn>=0.12.0 \
    openpyxl>=3.1.0 \
    pyreadstat>=1.2.0 \
    fastparquet>=2023.8.0 \
    tabulate>=0.9.0

print(f"Ambiente verificado exitosamente en Python: {sys.version.split()[0]}")
```

---

## 4. Cronograma de Ejecución y Asignación de Recursos

```
┌────────────────────────────────────────────────────────────────────────┐
│                  CRONOGRAMA DE TRABAJO (8 DÍAS HÁBILES)                │
├─────────┬──────────────────────────────────────────────────────────────┤
│ Día 1   │ Setup de src/, tests base y requirements.txt                 │
│ Día 2   │ Hito 1: Ingestion — Lectores políglotas y unificación mensual│
│ Día 3   │ Hito 2: EDA — Cullen-Frey, boxplots y correlaciones          │
│ Día 4   │ Hito 3: Validation — Regla cero precios nulos y DIVIPOLA     │
│ Día 5   │ Hito 4: Cleaning — Saneamiento y guardado en data/CLEANED/   │
│ Día 6   │ Hito 5: Features — Cruce demográfico, per cápita, IEP/IEO    │
│ Día 7   │ Hito 6: Model — ANOVA, Welch, Kruskal, Dunn y Bootstrap BCa  │
│ Día 8   │ Hito 7: Visualization — Tableros 300 DPI y cierre documental │
└─────────┴──────────────────────────────────────────────────────────────┘
```

---

## 5. Control de Calidad y Criterios de Aceptación (DoD)

Para dar por concluido el desarrollo, cada entregable debe cumplir:
1. **Completitud en Precios**: $0\%$ de precios nulos en el dataset consolidado (`precio_prom_kg IS NOT NULL`).
2. **Granularidad Temporal**: Serie de 84 meses consecutivos (2019–2025) sin saltos.
3. **Calidad de Código**: 100% de cumplimiento PEP 8 y Clean Code en los módulos de `src/`.
4. **Reproducibilidad de Cuadernos**: Ejecución secuencial sin errores con *Kernel -> Restart & Run All*.
5. **Trazabilidad Documental**: Sincronización continua de [metadata.json](file:///c:/Users/ADAN/OneDrive/Documentos/analisispapamercadoorlando/metadata.json).
