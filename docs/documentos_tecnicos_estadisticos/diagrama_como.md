# Diagrama Metodológico: El "Cómo" del Análisis de Mercado

**Proyecto**: Análisis Histórico del Mercado de la Papa en Colombia (2019 - 2025)  
**Fuente**: Microdatos SIPSA - DANE (Abastecimiento y Precios)  
**Enfoque**: Metodología Tripartita de Análisis de Mercado: **Oferta**, **Demanda** y **Precios**.

---

## 1. Diagrama de Flujo Metodológico Integral

Este diagrama muestra cómo se procesa la información desde los registros brutos del SIPSA hasta la obtención de diagnósticos y conclusiones de negocio, estructurado en los tres pilares del estudio:

```mermaid
flowchart TD
    subgraph INICIO["1. DATOS DE ENTRADA (SIPSA 2019-2025)"]
        D1["Microdatos de Abastecimiento Mayorista\n(Volumen Kg, Fechas, Origen, Destino, Variedad)"]
        D2["Microdatos de Precios Mayoristas\n(Cotizaciones Diarias por Kg y Bulto)"]
        D1 & D2 --> F0["Filtrado del Universo Papa y Estandarización de Variables"]
    end

    subgraph PILARES["2. LOS TRES PILARES ANALÍTICOS"]
        F0 --> P1["PILAR 1: ANÁLISIS CRÍTICO DE OFERTA\n• Producción y volúmenes totales (VTO)\n• Mapeo de cuencas productoras (Deptos/Municipios)\n• Calendario y ciclos de estacionalidad (IEO)"]
        
        F0 --> P2["PILAR 2: ANÁLISIS CRÍTICO DE DEMANDA\n• Capacidad de absorción de plazas mayoristas\n• Segmentos: Fresco vs. Industrial\n• Cuotas por variedad y tendencias de sustitución"]
        
        F0 --> P3["PILAR 3: COMPORTAMIENTO DE PRECIOS\n• Trayectoria y variaciones temporales\n• Volatilidad y dispersión por variedad/plaza\n• Factores influyentes (insumos, paros, clima)"]
    end

    subgraph CRUCE["3. INTERACCIÓN Y CRUCE DE MERCADO"]
        P1 & P2 & P3 --> INT["Análisis de Interacción Oferta - Demanda - Precios\n• Elasticidad y sensibilidad de cotizaciones ante exceso/escasez de oferta\n• Corredores logísticos y vulnerabilidad de plazas consumidoras\n• Cuantificación del impacto de choques exógenos"]
    end

    subgraph SALIDA["4. DIAGNÓSTICO E INTELIGENCIA ESTRATÉGICA"]
        INT --> R1["Diagnóstico de Zonas Productoras y Calendario de Cosechas"]
        INT --> R2["Perfil de Demanda por Segmento y Variedad"]
        INT --> R3["Comportamiento de Precios y Mapa de Riesgos de Mercado"]
        INT --> R4["Recomendaciones Prácticas para Productores y Comerciantes"]
    end

    style INICIO fill:#f8f9fa,stroke:#6c757d,stroke-width:1px
    style PILARES fill:#eef6fc,stroke:#1a73e8,stroke-width:1px
    style CRUCE fill:#fef9e7,stroke:#f1c40f,stroke-width:1px
    style SALIDA fill:#eafaf1,stroke:#2ecc71,stroke-width:1px
```

---

## 2. Diagrama de Relación: Preguntas $\rightarrow$ Indicadores $\rightarrow$ Resultados

Muestra la articulación directa entre las preguntas de investigación formuladas, las métricas calculadas y los resultados obtenidos para cada uno de los tres pilares:

```mermaid
flowchart LR
    subgraph OFERTA["Pilar 1: Oferta"]
        Q_OF["Preguntas de Oferta:\n¿Cuánto se produce?\n¿De qué zonas sale?\n¿Cuáles meses son pico?"] 
        --> I_OF["Indicadores:\nVTO (Volumen Oferta)\nPZP (Part. Cuencas)\nIEO (Estacionalidad)\nHHI (Concentración)"]
        --> R_OF["Resultado:\nMapa de oferta y\ncalendario agrícola"]
    end

    subgraph DEMANDA["Pilar 2: Demanda"]
        Q_DM["Preguntas de Demanda:\n¿Cuánto absorbe cada plaza?\n¿Qué segmentos dominan?\n¿Qué variedades prefieren?"]
        --> I_DM["Indicadores:\nVTA-Plaza (Consumo)\nCD-Segmento (Fresco/Ind)\nPVD (Cuota Variedades)\nTSI (Sustitución)"]
        --> R_DM["Resultado:\nPerfil de consumo y\ntendencias de compra"]
    end

    subgraph PRECIOS["Pilar 3: Precios"]
        Q_PR["Preguntas de Precios:\n¿Cómo varían en el tiempo?\n¿Qué tan volátiles son?\n¿Cómo afectan los choques?"]
        --> I_PR["Indicadores:\nPPMP (Precio Ponderado)\nVTP (Variación Temporal)\nCVP (Volatilidad)\nCSOP (Sensibilidad)\nMCEP (Choque Exógeno)"]
        --> R_PR["Resultado:\nDinámica de cotizaciones\ny factores influyentes"]
    end
```

---

## 3. Diagrama de Formación del Mercado: Interacción Oferta vs. Demanda $\rightarrow$ Precios

```mermaid
graph TD
    subgraph FUERZAS_MERCADO["Determinación del Mercado de la Papa"]
        O["OFERTA DE PAPA\n• Producción de Cuencas (Cundinamarca, Boyacá, Nariño, etc.)\n• Estacionalidad de Cosechas (Ciclos semestrales)\n• Capacidad de Despacho Logístico"]
        
        D["DEMANDA DE PAPA\n• Consumo Urbano en Grandes Plazas (Corabastos, Cavasa, etc.)\n• Demanda Industrial de Procesamiento (Frituras/Congelados)\n• Preferencia de Hogares por Variedades de Mesa"]
    end

    O -->|Volumen Físico Ingresado| EQUIL["MERCADO MAYORISTA DE ENTRADA"]
    D -->|Pedidos y Absorción| EQUIL

    EQUIL --> PRECIO["FORMACIÓN Y COMPORTAMIENTO DE PRECIOS\n• Si Oferta > Demanda -> Caída abrupta de cotizaciones (Sobreoferta)\n• Si Oferta < Demanda -> Presión inflacionaria de precios (Escasez)"]

    FACT_EXOG["FACTORES INFLUYENTES Y CHOQUES\n• Costos de Fertilizantes (2022-2023)\n• Paros y Cierres Viales (2021)\n• Clima: Heladas / Sequías / Lluvias (2023-2024)\n• Confinamiento COVID-19 (2020)"]

    FACT_EXOG -.->|Altera Costos y Cosechas| O
    FACT_EXOG -.->|Distorsiona Flujos| EQUIL
    FACT_EXOG -.->|Impacta Directamente| PRECIO
```

---

## 3.1 Diagrama del Doble Canal de Procesamiento: Paramétrico vs. No Paramétrico

```mermaid
flowchart TD
    INGEST["Datos Depurados de Papa (Silver Layer)"] --> DIAG["Diagnóstico Inicial:\nCullen & Frey Plot | Shapiro-Wilk | Levene / Fligner-Killeen"]

    DIAG --> DEC{¿Distribución Apta para Supuestos?}

    subgraph CANAL_PARAMETRICO["CANAL 1: PROCESAMIENTO PARAMÉTRICO"]
        CP1["Transformación de Datos:\n• Log Natural o Box-Cox\n• Winsorización al 1%-99%"]
        CP2["Métricas Centrales:\n• Media Aritmética (μ) y Desviación (σ)\n• Error Estándar (SE)"]
        CP3["Contraste Interanual:\n• ANOVA One-Way / Welch's ANOVA\n• Post-Hoc: Tukey HSD / Games-Howell"]
        CP4["Inferencia:\n• Intervalos de Confianza t-Student (95%)"]
        CP1 --> CP2 --> CP3 --> CP4
    end

    subgraph CANAL_NOPARAMETRICO["CANAL 2: PROCESAMIENTO NO PARAMÉTRICO"]
        CN1["Tratamiento Robusto:\n• Escala natural intacta\n• Transformación de Rangos R(x)"]
        CN2["Métricas Robustas:\n• Mediana (x̃ = Q2)\n• Rango Intercuartílico (IQR) y MAD"]
        CN3["Contraste Interanual:\n• Kruskal-Wallis (H)\n• Post-Hoc: Dunn con FDR Benjamini-Hochberg"]
        CN4["Inferencia:\n• Bootstrap BCa 95% (B=2,000 réplicas)"]
        CN1 --> CN2 --> CN3 --> CN4
    end

    DEC -->|Sí / Tras normalizar| CANAL_PARAMETRICO
    DEC -->|No / Asimetría severa / Choques| CANAL_NOPARAMETRICO

    CP4 --> SINTESIS["Triangulación y Síntesis Final de Resultados de Mercado"]
    CN4 --> SINTESIS
```

---

## 4. Descripción del Procedimiento Metodológico Paso a Paso

### Paso 1: Depuración y Homologación de Microdatos
- Filtrar la base histórica SIPSA para retener exclusivamente las líneas asociadas al tubérculo de papa.
- Estandarizar nombres comerciales de variedades (Pastusa, Capiro, Suprema, Criolla, R-12, etc.), plazas mayoristas y municipios de origen con código DIVIPOLA.

### Paso 2: Ejecución del Análisis Crítico de Oferta
1. **Volumen**: Agregar el volumen total por año, cuatrimestre/semestre, mes y semana para medir la trayectoria de la producción.
2. **Geografía**: Identificar la matriz de departamentos y municipios emisores para evaluar la concentración de zonas productoras (Índice HHI).
3. **Índice de Estacionalidad**: Calcular el Índice de Estacionalidad de la Oferta (IEO, base 100) para graficar los meses recurrentes de sobreabastecimiento ($>115$) y escasez ($<85$).
4. **Periodos de Producción y Granularidad**: Reconocer los ciclos vegetativos por variedad (papas de año de 5–6 meses vs. papa criolla de 3.5–4 meses), los desfases de cosechas regionales (Altiplano vs. Nariño vs. Antioquia) y analizar los datos en 5 escalas de granularidad temporal (diaria, semanal, mensual, periódica DANE y anual).

### Paso 3: Ejecución del Análisis Crítico de Demanda
1. **Consumo por Plaza**: Cuantificar el volumen absorbido por Corabastos, Cavasa, Central Mayorista de Antioquia, Mercar, etc.
2. **Segmentación**: Separar el volumen demandado por variedades de mesa vs. variedades de aptitud industrial vs. papa criolla.
3. **Tendencias**: Evaluar el crecimiento o caída de la cuota de mercado de cada variedad a lo largo de los 7 años analizados.
4. **Demanda Aparente y Consumo Per-Cápita**: Calcular la demanda aparente agregada y el consumo per cápita anual (en Toneladas y en Kilogramos por habitante) utilizando las proyecciones poblacionales oficiales del DANE (2019–2025).

### Paso 4: Examen del Comportamiento de Precios
1. **Trayectoria Temporal**: Construir las series de precios promedio mensuales ponderados por volumen.
2. **Volatilidad**: Calcular el coeficiente de variación de precios por variedad y por plaza para medir el riesgo de mercado.
3. **Factores Influyentes**: Cruzar los periodos de coyuntura (COVID 2020, Paros 2021, alza de fertilizantes 2022-23, eventos climáticos) contra la cotización media para aislar la magnitud del impacto de cada factor.

### Paso 5: Integración y Generación de Conclusiones
- Cruzar curvas de oferta vs. curvas de precios para obtener la elasticidad real del mercado.
- Generar cuadros de resumen, tablas cruzadas y visualizaciones de tendencias.
- Redactar recomendaciones estratégicas dirigidas a productores, distribuidores y planificadores del sector.
