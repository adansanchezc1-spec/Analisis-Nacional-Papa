# Plataforma Analítica del Mercado de la Papa en Colombia (SIPSA 2019–2025)

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/architecture-Clean%20Architecture-brightgreen.svg)](docs/documentos_PDCO/architecture.md)
[![Methodology](https://img.shields.io/badge/methodology-CRISP--DM%207%20Stages-orange.svg)](docs/documentos_PDCO/requirements.md)
[![Quality Standard](https://img.shields.io/badge/governance-DAMA--BOK%20%2F%20ISO%2025010-purple.svg)](docs/documentos_PDCO/development_plan.md)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-black.svg)](https://peps.python.org/pep-0008/)

---

## 1. Visión del Proyecto

Sistema analítico y de ciencia de datos de alto rendimiento diseñado para el examen crítico del mercado de la papa en Colombia durante el periodo 2019–2025, integrando más de 14 millones de registros transaccionales oficiales del **SIPSA (DANE)** y proyecciones demográficas **PPED (DANE)**.

El análisis se estructura en torno a los **Tres Pilares Fundamentales del Mercado**:
1. **Pilar 1: Análisis Crítico de Oferta**: Producción, cuencas productoras, estacionalidad agrícola, ciclos fenológicos (120 vs 180 días) y producción per cápita.
2. **Pilar 2: Análisis Crítico de Demanda**: Volúmenes de abastecimiento, absorción por nodos mayoristas, demanda aparente y consumo per cápita (kg/hab/mes).
3. **Pilar 3: Comportamiento de Precios**: Dinámica temporal, factores influyentes, dispersión de precios mayoristas e índices de estacionalidad (IEP).

---

## 2. Metodología CRISP-DM & Pipeline en 7 Etapas

El ciclo de procesamiento de datos sigue de forma rigurosa las 7 etapas maestras de CRISP-DM:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                   PIPELINE DE 7 ETAPAS CRISP-DM SOBRE ARQUITECTURA LIMPIA         │
├────────────┬──────────┬────────────┬──────────┬────────────┬──────────┬──────────────┤
│ 1.INGESTION│  2. EDA  │3.VALIDATION│4.CLEANING│ 5.FEATURES │ 6. MODEL │7.VISUALIZAT. │
│ Lector     │Medidas   │Regla de Oro│Saneamiento│Métricas   │Inferencia│Renderizado   │
│ Políglota  │Forma,    │Invariante: │Léxico,   │Per Cápita, │Dual:     │300 DPI:      │
│ Dataset    │Cullen &  │Ningún      │Filtros   │IEP, IEO,   │Paramétrica│Cajas,        │
│ Único      │Frey, Box,│Precio Nulo │DIVIPOLA  │Panel       │No Param. │Densidad,     │
│ Mensual    │Correlac. │(NotNull)   │DAMA-BOK  │Mensual     │Bootstrap │Correlación   │
└────────────┴──────────┴────────────┴──────────┴────────────┴──────────┴──────────────┘
```

* **Dataset Único Nacional**: La ingestión unifica los 16 semestres/cuatrimestres crudos en un único dataset con **dimensionalidad temporal mensual continua** (`fecha_mes = 'YYYY-MM-01'`) y granularidad espacial **DIVIPOLA DANE**.
* **Invariante Estricta**: **Cero Precios Nulos** (`precio_prom_kg IS NOT NULL` y `> 0`).

---

## 3. Estructura del Repositorio (Clean Architecture)

```
analisispapamercadoorlando/
├── README.md                      ← [Este archivo] Portada del repositorio y guía rápida
├── requirements.txt               ← Dependencias científicas fijas del entorno
├── metadata.json                  ← Metadatos de gobernanza del proyecto
├── .gitignore                     ← Exclusión de datos pesados (4 GB) y cachés
│
├── data/                          ← Arquitectura Medallion en disco local
│   ├── RAW/                       ← Datos originales inmutables (SIPSA y Demografía)
│   ├── CLEANED/                   ← Capa Plata: Dataset Único Mensual (Parquet)
│   ├── FEATURES/                  ← Capa Oro: Métricas, per cápita y estacionalidad (Parquet)
│   └── CURATED/                   ← Capa Platino: Contrastes estadísticos y tableros (Parquet/PNG)
│
├── notebooks/                     ← Cuadernos interactivos reproducibles (1 por etapa CRISP-DM)
│   ├── 01_ingestion_dataset_unico.ipynb
│   ├── 02_analisis_exploratorio_eda.ipynb
│   ├── 03_validacion_reglas_negocio.ipynb
│   ├── 04_limpieza_y_gobernanza.ipynb
│   ├── 05_ingenieria_de_features.ipynb
│   ├── 06_modelado_e_inferencia_dual.ipynb
│   └── 07_visualizacion_y_tableros.ipynb
│
├── src/                           ← Código fuente de producción (Clean Architecture & PEP 8)
│   ├── domain/                    ← Capa 1: Entidades puras, invariantes y DIVIPOLA
│   ├── infrastructure/            ← Capa 2: Lectores políglotas (CSV, DTA, SAV, SAS) y Parquet
│   ├── application/               ← Capa 3: Servicios de las 7 etapas CRISP-DM
│   └── presentation/              ← Capa 4: Renderizadores Cullen-Frey, Boxplots y Correlación
│
├── tests/                         ← Suite de pruebas unitarias automatizadas (Pytest)
│   ├── test_invariants.py
│   ├── test_divipola.py
│   ├── test_eda.py
│   ├── test_validation.py
│   ├── test_features.py
│   └── test_model.py
│
└── docs/                          ← Repositorio documental completo
    ├── README.md                  ← Índice maestro de documentación
    ├── documentos_PDCO/           ← Requerimientos (SRS), Arquitectura (SAD) y Plan de Desarrollo
    └── documentos_tecnicos_estadisticos/ ← 14 documentos metodológicos, matemáticos y DIVIPOLA
```

---

## 4. Instalación y Configuración del Entorno

### 4.1 Clonar el Repositorio
```bash
git clone https://github.com/usuario/analisispapamercadoorlando.git
cd analisispapamercadoorlando
```

### 4.2 Crear y Activar Entorno Virtual
```bash
python -m venv venv

# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# En Linux / macOS:
source venv/bin/activate
```

### 4.3 Instalar Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. Ejecución del Pipeline y Pruebas

### 5.1 Ejecución de Pruebas Unitarias
El proyecto cuenta con una suite completa de pruebas unitarias para validar las invariantes de negocio, la sanitización DIVIPOLA y la exactitud de los contrastes estadísticos:

```bash
pytest tests/ -v
```

### 5.2 Ejecución de los Cuadernos Jupyter
Todos los cuadernos en `notebooks/` están diseñados para ser ejecutados de forma secuencial y contienen una celda inicial idempotente con `%pip install`:

```bash
jupyter lab
# O alternativamente:
jupyter notebook
```

Secuencia de ejecución recomendada:
1. `notebooks/01_ingestion_dataset_unico.ipynb` $\rightarrow$ Compila `dataset_sipsa_mensual_nacional.parquet`
2. `notebooks/02_analisis_exploratorio_eda.ipynb` $\rightarrow$ Genera diagnóstico Cullen-Frey y boxplots
3. `notebooks/03_validacion_reglas_negocio.ipynb` $\rightarrow$ Audita cero precios nulos bajo DAMA-BOK
4. `notebooks/04_limpieza_y_gobernanza.ipynb` $\rightarrow$ Sanea variedades y resuelve homónimos
5. `notebooks/05_ingenieria_de_features.ipynb` $\rightarrow$ Calcula consumo per cápita y estacionalidad
6. `notebooks/06_modelado_e_inferencia_dual.ipynb` $\rightarrow$ Ejecuta contrastes ANOVA/Welch y Kruskal/BCa
7. `notebooks/07_visualizacion_y_tableros.ipynb` $\rightarrow$ Renderiza el tablero ejecutivo a 300 DPI

---

## 6. Documentación Técnica de Referencia

Para consultar los fundamentos teóricos, metodológicos y de gobernanza:
* [Índice Maestro de Documentación](docs/README.md)
* [Especificación de Requerimientos de Software (SRS)](docs/documentos_PDCO/requirements.md)
* [Documento de Arquitectura de Software y Datos (SAD)](docs/documentos_PDCO/architecture.md)
* [Plan de Desarrollo e Implementación](docs/documentos_PDCO/development_plan.md)
* [Catálogo Oficial DIVIPOLA DANE de Colombia](docs/documentos_tecnicos_estadisticos/catalogo_divipola.md)
* [Plan de Extracción Demográfica DANE PPED](docs/documentos_tecnicos_estadisticos/plan_extraccion_demografia.md)
* [Batería de Pruebas Estadísticas](docs/documentos_tecnicos_estadisticos/bateria_pruebas_estadisticas.md)
* [Manual de Granularidad y Fenología](docs/documentos_tecnicos_estadisticos/manual_granularidad.md)

---

## 7. Licencia y Créditos
* **Autor**: Senior Software Engineer & Data Scientist (`@user_global`)
* **Fuente de Datos**: SIPSA — Departamento Administrativo Nacional de Estadística (DANE)
* **Licencia**: MIT License — Uso Académico y de Investigación Agropecuaria.
