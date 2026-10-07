# Manual de Formateo, Data Wrangling, Pivoteo y Gobernanza de Datos

**Proyecto**: Análisis Histórico del Mercado de la Papa en Colombia (2019 - 2025)  
**Marco Normativo**: DAMA-BOK (Data Governance, Data Quality, Master Data & Analytics)  
**Estándar de Código**: Clean Code y PEP 8  

---

## 1. Marco de Gobernanza de Datos (DAMA-BOK)

Para garantizar la máxima integridad, trazabilidad y rigor analítico, el manejo de datos del mercado de la papa se rige por las **6 Dimensiones Universales de Calidad de Datos**:

```
┌────────────────────────────────────────────────────────────────────────┐
│             DIMENSIONES DE CALIDAD DE DATOS (DAMA-BOK)                 │
├─────────────────┬──────────────────────────────────────────────────────┤
│ DIMENSIÓN       │ CRITERIO OPERACIONAL EN EL PROYECTO PAPA             │
├─────────────────┼──────────────────────────────────────────────────────┤
│ 1. Completitud  │ 0% de nulos en variables clave (Fecha, Variedad, Kg) │
│ 2. Validez      │ Códigos DIVIPOLA válidos según catálogo DANE oficial │
│ 3. Consistencia │ Suma de volúmenes por variedad = volumen total mes    │
│ 4. Exactitud    │ Volúmenes positivos coincidentes con capacidad carga │
│ 5. Unicidad     │ Eliminación de duplicados de encuesta idénticos      │
│ 6. Trazabilidad │ Linaje explícito: Raw (Bronze) → Silver → Gold       │
└─────────────────┴──────────────────────────────────────────────────────┘
```

### Arquitectura de Linaje de Datos (Medallion Pattern)
```mermaid
flowchart LR
    RAW["1. RAW (Bronze)\n• Archivos originales intactos\n• CSVs, DTAs, SAVs de SIPSA\n• Solo lectura / Inmutable"]
    
    --> SILVER["2. SILVER (Curada / Limpia)\n• Esquema canónico unificado\n• Filtro exclusivo de Papas\n• Limpieza de ' y formatos de miles\n• Normalización léxica y DIVIPOLA"]
    
    --> GOLD["3. GOLD (Analítica / Modelos)\n• Tablas pivote y agregaciones\n• Series de tiempo mensuales\n• Matrices de flujos Origen-Destino\n• Tablas de Indicadores y KPIs"]
```

---

## 2. Manual de Formateo y Estandarización Léxica

### 2.1 Estandarización de Variedades de Papa
Los registros crudos presentan inconsistencias tipográficas entre periodos. Se aplica un **Diccionario de Mapeo Canónico**:

| Texto Crudo en SIPSA | Denominación Canónica Estandarizada | Familia / Segmento |
|---|---|---|
| `Papa suprema`, `PAPA SUPREMA`, `Papa Suprema` | **Papa Suprema** | Consumo en Fresco (Mesa) |
| `Papa pastusa`, `PAPA PASTUSA`, `Papa Pastusa` | **Papa Pastusa** | Consumo en Fresco (Mesa) |
| `Papa diacol capiro`, `Papa capiro`, `Papa capira`, `PAPA CAPIRO` | **Papa Diacol Capiro (Capira)** | Industrial / Fritura |
| `Papa criolla limpia`, `Papa criolla`, `Papa criolla sucia` | **Papa Criolla** | Variedad Especial / Amarilla |
| `Papa r-12 negra`, `Papa r-12`, `Papa parda pastusa` | **Papa R-12 / Negra** | Consumo en Fresco (Mesa) |
| `Papa sabanera`, `Papa tuquerreña`, `Papa rubi`, `Papa betina` | **Otras Papas de Mesa** | Consumo en Fresco (Mesa) |

### 2.2 Normalización de Mercados Mayoristas
| Texto Crudo en SIPSA | Denominación Canónica | Ciudad Principal |
|---|---|---|
| `Bogotá, D.C., Corabastos`, `Corabastos` | **Corabastos** | Bogotá D.C. |
| `Cali, Cavasa`, `Cavasa` | **Cavasa** | Cali (Valle) |
| `Medellín, Central Mayorista de Antioquia`, `Itagüí, Mayorista` | **Central Mayorista de Antioquia** | Medellín (Antioquia) |
| `Armenia, Mercar`, `Mercar` | **Mercar** | Armenia (Quindío) |
| `Pereira, Mercasa` | **Mercasa** | Pereira (Risaralda) |
| `Bucaramanga, Centroabastos` | **Centroabastos** | Bucaramanga (Santander) |

### 2.3 Tratamiento de Códigos DIVIPOLA
- Regla: Extraer solo los caracteres numéricos y rellenar con ceros a la izquierda si procede:
  - `depto_code = cod_depto.str.extract(r'(\d+)')[0].str.zfill(2)`
  - `mpio_code = cod_mpio.str.extract(r'(\d+)')[0].str.zfill(5)`

---

## 3. Procedimiento de Data Wrangling

El flujo funcional de preparación de datos se ejecuta en 5 etapas secuenciales:

```mermaid
flowchart TD
    P1["1. INGESTA ROBUSTA\n• Lectura con encoding='latin-1' y sep=';'\n• Detección automática del esquema (2019-23 vs 2024 vs 2025)"]
    --> P2["2. UNIFICACIÓN DE ESQUEMA\n• Mapeo al estándar canónico\n• Conversión de 'Fecha' a Datetime (DD/MM/AAAA)"]
    --> P3["3. FILTRADO TEMÁTICO\n• Retener exclusivamente Grupo = 'TUBERCULOS' y Alimento = 'PAPA*'"]
    --> P4["4. LIMPIEZA DE MAGNITUDES\n• Limpieza de ' 9.000 ' -> 9000.0\n• Creación de 'volumen_ton' = volumen_kg / 1000"]
    --> P5["5. ENRIQUECIMIENTO TEMPORAL\n• Generar columnas: anio, mes, semana_anio, dia_semana, periodo_dane"]
```

---

## 4. Manual de Pivoteo y Agregaciones Multidimensionales

El análisis analítico de mercado requiere reestructurar los microdatos transaccionales (filas por camión/encuesta) en **matrices pivote bidimensionales**:

### 4.1 Pivoteo 1: Matriz Temporal $\times$ Variedades (Dinámica de Oferta)
- **Filas**: `anio` y `mes`.
- **Columnas**: `variedad_papa` (Pastusa, Capiro, Suprema, Criolla, R-12).
- **Valores**: $\sum \text{volumen\_ton}$.
- **Propósito**: Observar la evolución temporal de cada variedad e identificar cambios en la canasta de mercado.

### 4.2 Pivoteo 2: Matriz Origen $\times$ Destino (Flujos Logísticos de Carga)
- **Filas**: `depto_origen` (Cundinamarca, Boyacá, Nariño, Antioquia, Santander).
- **Columnas**: `mercado_mayorista` (Corabastos, Cavasa, Mayorista Antioquia, Mercar).
- **Valores**: $\sum \text{volumen\_ton}$ y $\%$ de participación.
- **Propósito**: Mapear la matriz insumo-producto espacial y evaluar la vulnerabilidad de cada plaza.

### 4.3 Pivoteo 3: Matriz de Estacionalidad Anual (Para el Cálculo del IEO)
- **Filas**: `mes` (1 a 12).
- **Columnas**: `anio` (2019, 2020, 2021, 2022, 2023, 2024, 2025).
- **Valores**: $\text{volumen\_ton}$ total del mes.
- **Propósito**: Calcular los promedios mensuales históricos que alimentan el Índice de Estacionalidad ($\text{IEO}$, base 100).

### 4.4 Pivoteo 4: Matriz de Segmentos Comerciales
- **Filas**: `anio`.
- **Columnas**: `segmento_consumo` (Fresco / Mesa vs. Industrial / Fritura vs. Papa Criolla).
- **Valores**: $\%$ Cuota de mercado.
- **Propósito**: Contrastar el crecimiento del segmento agroindustrial frente al consumo hogareño tradicional.

### 4.5 Pivoteo 5: Matriz Desagregada Municipal $\times$ Mes (Estacionalidad Microterritorial)
- **Filas**: `depto_origen` y `municipio_origen` (con código DIVIPOLA).
- **Columnas**: `mes` (1 a 12).
- **Valores**: $\sum \text{volumen\_ton}$.
- **Propósito**: Determinar en qué meses específicos despacha cada municipio productor (identificando la sincronía de cosechas a nivel micro).

### 4.6 Pivoteo 6: Matriz de Precios Mayoristas Variedad $\times$ Plaza
- **Filas**: `variedad_papa`.
- **Columnas**: `mercado_mayorista` (Corabastos, Cavasa, Mayorista Antioquia, Mercar).
- **Valores**: Mediana y Media ponderada de precio ($COP/Kg$).
- **Propósito**: Cuantificar las brechas espaciales de precio (primas de flete y concentración de consumo).

---

## 5. Reglas de Calidad y Rigor Operacional

1. **Inmutabilidad de la Capa Raw**: Nunca se modifica, sobreescribe ni renombra ningún archivo dentro de `data/RAW/sipsa/`.
2. **Determinismo y Reproducibilidad**: Cualquier paso de imputación o remoción de duplicados debe estar gobernado por una semilla fija o criterio explícito documentado.
3. **Validación de Balances de Masa**:
   $$\sum \text{Volumen Tablas Pivote} \equiv \sum \text{Volumen Capa Silver Limpia}$$
   Ningún kilogramo de papa puede crearse o destruirse durante los procesos de transformación y pivoteo.
