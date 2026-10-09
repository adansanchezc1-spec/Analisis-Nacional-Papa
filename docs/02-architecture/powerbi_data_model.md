# Especificación de Arquitectura y Modelo Dimensional de Power BI
**Proyecto:** Plataforma Analítica Agropecuaria Colombia — Mercado de la Papa (2019–2025)  
**Fase PDCO:** PLAN → DEVELOPMENT | **SDLC Stage:** Design & Data Engineering  
**Estándar:** DAMA-BOK v2 (Cap. 10: Data Warehousing & Business Intelligence) | SWEBOK v3  
**Versión:** 1.0.0 | **Fecha:** Octubre 2026  

---

## 1. Visión General y Propósito

El presente documento formaliza la arquitectura dimensional en estrella (*Kimball Star Schema*) desarrollada para el consumo analítico en **Power BI Desktop**, **Power BI Service** y **Microsoft Fabric**. Integra de forma armónica y conformada tres fuentes heterogéneas:
1. **Evaluaciones Agropecuarias Municipales (EVA / MinAgricultura / UPRA):** Producción, rendimientos y áreas agrícolas semestrales-municipales.
2. **Sistema de Información de Precios y Abastecimiento del Sector Agropecuario (SIPSA / DANE):** Dinámica transaccional mensual de volúmenes mayoristas y cotizaciones de precios en plazas de mercado.
3. **Censo Nacional de Población y Vivienda (CNPV / DANE):** Proyecciones demográficas nacionales y per cápita.

---

## 2. Diagrama de Arquitectura de Datos y Pipeline ETL

```mermaid
flowchart TD
    subgraph Fuentes_Primarias["Capa RAW (Ingestión)"]
        F1["Excel EVA MinAgricultura (2019-2025)"]
        F2["Microdatos SIPSA DANE (2019-2025)"]
        F3["Catálogo DIVIPOLA & CNPV DANE"]
    end

    subgraph Pipeline_Medallion["Capa CLEANED & FEATURES"]
        C1["Limpieza Léxica y Armonización DIVIPOLA"]
        C2["Features: Índices Estacionales (IVE/IEP), Consumo Per Cápita"]
        C3["Validación de Invariantes: Cero Precios Nulos"]
    end

    subgraph Capa_Dimensional["Capa POWER BI (Star Schema - Kimball)"]
        DT["Dim_Tiempo (84 meses)"]
        DG["Dim_Geografia (481 mpios)"]
        DV["Dim_Variedad (2 canónicas)"]
        DM["Dim_Mercado (34 plazas)"]
        FE["Fact_Produccion_EVA (5,574 filas)"]
        FA["Fact_Abastecimiento_SIPSA (86,054 filas)"]
        FP["Fact_Precios_SIPSA (86,054 filas)"]
    end

    subgraph Capa_Presentacion["Capa de Presentación (Power BI Desktop / Service)"]
        P1["Pág 1: Resumen Ejecutivo y Monitor Macro"]
        P2["Pág 2: Oferta y Geografía Productiva"]
        P3["Pág 3: Abastecimiento y Red Mayorista"]
        P4["Pág 4: Precios y Volatilidad"]
        P5["Pág 5: Simulador What-If y Estrategia"]
    end

    F1 & F2 & F3 --> C1 --> C2 --> C3
    C3 --> DT & DG & DV & DM
    C3 --> FE & FA & FP
    DT & DG & DV & DM --> FE & FA & FP
    FE & FA & FP --> P1 & P2 & P3 & P4 & P5
```

---

## 3. Diagrama Entidad-Relación Dimensional (Mermaid ERD)

```mermaid
erDiagram
    Dim_Tiempo ||--o{ Fact_Produccion_EVA : "filtra por fecha"
    Dim_Geografia ||--o{ Fact_Produccion_EVA : "filtra por municipio"
    Dim_Variedad ||--o{ Fact_Produccion_EVA : "filtra por variedad"

    Dim_Tiempo ||--o{ Fact_Abastecimiento_SIPSA : "filtra por fecha"
    Dim_Mercado ||--o{ Fact_Abastecimiento_SIPSA : "filtra por plaza"
    Dim_Variedad ||--o{ Fact_Abastecimiento_SIPSA : "filtra por variedad"
    Dim_Geografia ||--o{ Fact_Abastecimiento_SIPSA : "ubica procedencia municipal"

    Dim_Tiempo ||--o{ Fact_Precios_SIPSA : "filtra por fecha"
    Dim_Mercado ||--o{ Fact_Precios_SIPSA : "filtra por plaza"
    Dim_Variedad ||--o{ Fact_Precios_SIPSA : "filtra por variedad"

    Dim_Geografia ||--o{ Dim_Mercado : "ubica geográficamente"

    Dim_Tiempo {
        int id_tiempo PK
        date fecha
        int año
        int mes
        string nombre_mes
        string año_mes
        string periodo_agricola
    }

    Dim_Geografia {
        string cod_mpio PK
        string municipio
        string cod_depto
        string departamento
        string region_natural
        boolean es_productor_destacado
    }

    Dim_Variedad {
        string cod_variedad PK
        string nombre_variedad
        string variedad_canonica
        string nombre_cientifico
        int ciclo_fenologico_dias
        string segmento_mercado
    }

    Dim_Mercado {
        int id_mercado PK
        string mercado_mayorista
        string cod_mpio FK
        string municipio
        string departamento
        string tipo_hub_logistico
    }

    Fact_Produccion_EVA {
        int id_tiempo FK
        string cod_mpio FK
        string cod_variedad FK
        float area_sembrada_ha
        float area_cosechada_ha
        float produccion_ton
        float rendimiento_ton_ha
        float tasa_perdida_cosecha_pct
    }

    Fact_Abastecimiento_SIPSA {
        int id_tiempo FK
        int id_mercado FK
        string cod_variedad FK
        float volumen_ingreso_ton
        float indice_estacional_oferta_ieo
        float consumo_mayorista_per_capita_kg
    }

    Fact_Precios_SIPSA {
        int id_tiempo FK
        int id_mercado FK
        string cod_variedad FK
        float precio_prom_kg
        float precio_min_kg
        float precio_max_kg
        float spread_precios_kg
        int num_transacciones
        float indice_estacional_precio_iep
    }
```

---

## 4. Matriz Bus de Arquitectura Dimensional (Grano y Conformance)

| Tabla de Hechos | Grano del Registro | Dim_Tiempo | Dim_Geografia | Dim_Variedad | Dim_Mercado |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`Fact_Produccion_EVA`** | Municipio - Semestre - Variedad | **X** (Semestral) | **X** (Municipio) | **X** | - |
| **`Fact_Abastecimiento_SIPSA`** | Mercado - Mes - Variedad | **X** (Mensual) | Mediante Dim_Mercado | **X** | **X** |
| **`Fact_Precios_SIPSA`** | Mercado - Mes - Variedad | **X** (Mensual) | Mediante Dim_Mercado | **X** | **X** |

---

## 5. Decisiones de Diseño e Ingeniería de Software

### ADR-003: Esquema en Estrella Desacoplado vs. Tabla Ancha Desnormalizada
- **Contexto:** Las fuentes EVA y SIPSA presentan naturalezas de reporte y granos temporales distintos (semestral agrícola vs. transaccional mayorista mensual).
- **Decisión:** Implementar un esquema Kimball multitable con dimensiones compartidas (*conformed dimensions*) en lugar de un único dataframe plano desnormalizado.
- **Consecuencias Positivas:**
  1. Rendimiento óptimo en el motor tabular VertiPaq de Power BI gracias a la compresión por diccionario.
  2. Evita la duplicación masiva de datos y errores de agregación (problema de doble conteo o *fan-out traps*).
  3. Escalabilidad inmediata para añadir nuevas dimensiones (clima, insumos, comercio exterior).

### ADR-004: Separación de Hechos de Abastecimiento y Hechos de Precios
- **Contexto:** Aunque SIPSA contiene volumen y precio en el mismo reporte, las operaciones analíticas sobre precios requieren ponderaciones y cálculos no aditivos (medias, percentiles, spreads), mientras que los volúmenes son aditivos directos.
- **Decisión:** Desacoplar `Fact_Abastecimiento_SIPSA` y `Fact_Precios_SIPSA` manteniendo claves idénticas.
- **Consecuencias:** Claridad de modelado, medidas DAX más legibles y optimización de memoria.

---

## 6. Validación de Principios SOLID
- **Single Responsibility (SRP):** El módulo `PowerBIExportService` tiene como única responsabilidad transformar y serializar los datasets limpios al formato dimensional de BI.
- **Open/Closed (OCP):** Nuevas dimensiones pueden ser incorporadas sin alterar los métodos constructores existentes de hechos.
- **Dependency Inversion (DIP):** Las rutas de entrada y salida se desacoplan mediante la configuración global de `src/infrastructure/config.py`.
