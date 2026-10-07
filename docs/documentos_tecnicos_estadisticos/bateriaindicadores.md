# Batería de Indicadores de Mercado (KPIs y Métricas Analíticas)

**Proyecto**: Análisis Histórico del Mercado de la Papa en Colombia (2019 - 2025)  
**Fuente**: SIPSA - DANE (Abastecimiento y Precios Agropecuarios) y Proyecciones de Población DANE  
**Estructura**: Clasificación rigurosa en los tres pilares del mercado: **Oferta**, **Demanda** y **Precios**.

---

## 1. Indicadores para el Análisis Crítico de Oferta
*(Producción, Zonas Productoras y Estacionalidad)*

### IND-OF-01: Volumen Total Ofertado (VTO)
- **Fórmula**: $\text{VTO}_{t} = \sum \text{Cantidad de Papa Despachada (Kg o Toneladas) en el periodo } t$
- **Unidad**: Toneladas métricas (t) / Kilogramos (kg).
- **Periodicidad**: Anual, Semestral, Cuatrimestral, Mensual.
- **Objetivo**: Cuantificar la masa total de oferta disponible generada por las zonas productoras.

### IND-OF-02: Tasa de Crecimiento de la Oferta Interanual (TCO)
- **Fórmula**: $\text{TCO}_{t} = \left(\frac{\text{VTO}_{t} - \text{VTO}_{t-1}}{\text{VTO}_{t-1}}\right) \times 100\%$
- **Unidad**: Porcentaje (%).
- **Periodicidad**: Anual o mes homólogo interanual.
- **Objetivo**: Medir la expansión o contracción de la producción agregada nacional entre periodos equivalentes.

### IND-OF-03: Participación de Zonas Productoras (PZP)
- **Fórmula**: $\text{PZP}_{d, t} = \left(\frac{\text{Volumen originado en el departamento/municipio } d}{\text{VTO total nacional}}\right) \times 100\%$
- **Unidad**: Porcentaje (%).
- **Periodicidad**: Anual y Mensual.
- **Objetivo**: Evaluar la contribución de cada cuenca productora líder (Cundinamarca, Boyacá, Nariño, Antioquia, Santander) al volumen total.

### IND-OF-04: Índice de Concentración Espacial de la Oferta (HHI-Oferta)
- **Fórmula**: $\text{HHI-Oferta} = \sum_{d=1}^{N} (\text{PZP}_{d})^2$
- **Unidad**: Puntos (escala 0 a 10,000).
- **Periodicidad**: Anual.
- **Objetivo**: Medir el nivel de concentración geográfica de la producción. Valores $> 2,500$ señalan alta dependencia de pocos territorios.

### IND-OF-05: Índice de Estacionalidad de la Oferta (IEO)
- **Fórmula**: $\text{IEO}_{m} = \left(\frac{\overline{\text{VTO}}_{m}}{\overline{\text{VTO}}_{\text{promedio mensual}}}\right) \times 100$
- **Unidad**: Índice (base 100).
- **Periodicidad**: Mensual (calculado sobre la serie 2019–2025).
- **Objetivo**: Identificar los meses pico de cosecha ($\text{IEO} > 100$) y las épocas de valle/escasez de recolección ($\text{IEO} < 100$).

### IND-OF-06: Amplitud de la Brecha Estacional de Oferta (ABEO)
- **Fórmula**: $\text{ABEO} = \left(\frac{\text{VTO}_{\text{mes máximo}} - \text{VTO}_{\text{mes mínimo}}}{\overline{\text{VTO}}_{\text{mensual}}}\right) \times 100\%$
- **Unidad**: Porcentaje (%).
- **Periodicidad**: Anual.
- **Objetivo**: Dimensionar la severidad de la brecha entre la máxima sobreoferta y la mínima oferta de cada año.

### IND-OF-07: Producción per-cápita (PPC_TON / PPC_KG)
- **Fórmula**: 
  $$\text{PPC\_TON}_{t} = \frac{\text{VTO (Ton)}_{t}}{\text{Población}_{t}}, \quad \text{PPC\_KG}_{t} = \text{PPC\_TON}_{t} \times 1,000$$
- **Unidad**: Ton/hab/año y Kg/hab/año.
- **Periodicidad**: Anual.
- **Desagregación**: Nacional y Departamental de Origen.
- **Objetivo**: Cuantificar la masa física de papa generada por habitante. A nivel departamental mide la vocación exportadora y especialización de cuencas como Boyacá, Cundinamarca y Nariño.

---

## 2. Indicadores para el Análisis Crítico de Demanda
*(Consumo, Segmentos, Macromagnitudes y Tendencias)*

### IND-DM-01: Demanda Aparente (DA)
- **Fórmula**: 
  $$\text{DA}_{t} = \text{Abastecimiento Total Registrado}_{t} + \text{Importaciones}_{t} - \text{Exportaciones}_{t}$$
  *(En el alcance de mercados mayoristas: suma agregada de ingresos de papa a plazas).*
- **Unidad**: Toneladas métricas (t) o Kilogramos (kg).
- **Periodicidad**: Anual y Semestral.
- **Objetivo**: Establecer la masa total neta de papa absorbida por el mercado interno nacional.

### IND-DM-02: Población Colombia (POB_COL)
- **Fórmula**: Dato oficial de Proyecciones de Población DANE a mitad de periodo (Censo CNPV 2018).
- **Unidad**: Número de habitantes.
- **Periodicidad**: Anual (2019: ~49.4M ... 2025: ~53.1M).
- **Objetivo**: Servir como denominador demográfico oficial para normalizaciones de escala per cápita.

### IND-DM-03: Consumo per-cápita en Toneladas (CPC_TON)
- **Fórmula**: 
  $$\text{CPC\_TON}_{t} = \frac{\text{Demanda Aparente (Ton)}_{t}}{\text{Población Colombia}_{t}}$$
- **Unidad**: Toneladas / habitante / año (Ton/hab/año).
- **Periodicidad**: Anual.
- **Objetivo**: Cuantificar el consumo promedio por habitante en unidades macroeconómicas estandarizadas.

### IND-DM-04: Consumo per-cápita en Kilogramos (CPC_KG)
- **Fórmula**: 
  $$\text{CPC\_KG}_{t} = \text{CPC\_TON}_{t} \times 1,000 = \frac{\text{Demanda Aparente (Kg)}_{t}}{\text{Población Colombia}_{t}}$$
- **Unidad**: Kilogramos / habitante / año (Kg/hab/año).
- **Periodicidad**: Anual (con desagregación semestral proyectada anualizada).
- **Objetivo**: Medir la ingesta neta media de papa por persona al año en la dieta familiar colombiana (rango de referencia país: 35 a 60 kg/hab/año).

### IND-DM-05: Volumen Total Absorbido por Plaza Mayorista (VTA-Plaza)
- **Fórmula**: $\text{VTA-Plaza}_{p, t} = \sum \text{Cantidad de Papa Ingresada a la Plaza Mayorista } p \text{ en el periodo } t$
- **Unidad**: Toneladas métricas (t).
- **Periodicidad**: Mensual / Anual.
- **Objetivo**: Medir la escala de consumo y absorción de cada nodo urbano (Corabastos, Cavasa, Mayorista de Antioquia, Mercar, etc.).

### IND-DM-06: Cuota de Demanda por Segmento Comercial (CD-Segmento)
- **Fórmula**: $\text{CD-Segmento}_{s} = \left(\frac{\text{Volumen del Segmento } s}{\text{Volumen Total Demandado}}\right) \times 100\%$
  - Donde $s \in \{\text{Consumo en Fresco / Mesa}, \text{Industrial / Fritura}, \text{Papa Criolla}\}$
- **Unidad**: Porcentaje (%).
- **Periodicidad**: Anual y Semestral.
- **Objetivo**: Caracterizar el destino del consumo de papa según tipo de uso final.

### IND-DM-07: Participación por Variedad en la Demanda (PVD)
- **Fórmula**: $\text{PVD}_{v, t} = \left(\frac{\text{Volumen demandado de la variedad } v \text{ en el periodo } t}{\text{Volumen total de papa demandado en el periodo } t}\right) \times 100\%$
- **Unidad**: Porcentaje (%).
- **Periodicidad**: Anual / Mensual.
- **Objetivo**: Determinar el ranking de preferencia del consumidor por variedad (Pastusa, Capiro, Suprema, Criolla, R-12, etc.).

### IND-DM-08: Tasa de Sustitución Intervarietal (TSI)
- **Fórmula**: $\text{TSI}_{v} = \text{PVD}_{v, t} - \text{PVD}_{v, t-1}$
- **Unidad**: Puntos porcentuales.
- **Periodicidad**: Anual.
- **Objetivo**: Cuantificar el desplazamiento en la preferencia de una variedad frente a otra (e.g., ganancia de cuota de Suprema o Capiro frente a Pastusa).

### IND-DM-09: Coeficiente de Dependencia de Consumo (CDC)
- **Fórmula**: $\text{CDC}_{p, d} = \left(\frac{\text{Volumen recibido en la plaza } p \text{ desde la zona productora } d}{\text{Volumen total recibido en la plaza } p}\right) \times 100\%$
- **Unidad**: Porcentaje (%).
- **Periodicidad**: Anual.
- **Objetivo**: Medir el riesgo de vulnerabilidad de un centro de consumo urbano ante fallas de suministro de una zona productora específica.

---

## 3. Indicadores para el Examen del Comportamiento de Precios
*(Variaciones Temporales y Factores Influyentes)*

### IND-PR-01: Precio Promedio Mayorista Ponderado (PPMP)
- **Fórmula**: $\text{PPMP}_{t} = \frac{\sum (\text{Precio}_{i, t} \times \text{Volumen}_{i, t})}{\sum \text{Volumen}_{i, t}}$
- **Unidad**: COP / Kilogramo (o COP / Bulto de 50 kg).
- **Periodicidad**: Mensual, Semestral, Anual.
- **Objetivo**: Establecer la cotización representativa real del mercado para evitar sesgos de precios extremos.

### IND-PR-02: Variación Temporal de Precios (VTP)
- **Fórmula**: $\text{VTP}_{t} = \left(\frac{\text{PPMP}_{t} - \text{PPMP}_{t-1}}{\text{PPMP}_{t-1}}\right) \times 100\%$
- **Unidad**: Porcentaje (%).
- **Periodicidad**: Mensual (inflación mensual) o Interanual (variación doce meses).
- **Objetivo**: Monitorear el ritmo de encarecimiento o abaratamiento de la papa en el tiempo.

### IND-PR-03: Coeficiente de Volatilidad de Precios (CVP)
- **Fórmula**: $\text{CVP} = \left(\frac{\sigma_{\text{Precio}}}{\mu_{\text{Precio}}}\right) \times 100\%$
- **Unidad**: Porcentaje (%).
- **Periodicidad**: Anual / por variedad / por plaza.
- **Objetivo**: Medir el nivel de riesgo e incertidumbre económica asociado a las fluctuaciones de cotización.

### IND-PR-04: Coeficiente de Sensibilidad Oferta-Precio (CSOP)
- **Fórmula**: $\text{CSOP} = \frac{\% \Delta \text{ Precio}}{\% \Delta \text{ Volumen Ofertado}}$
- **Unidad**: Razón de elasticidad.
- **Periodicidad**: Mensual / Anual.
- **Objetivo**: Determinar qué tan fuertemente reaccionan los precios ante variaciones en la cantidad física que ingresa a las plazas.

### IND-PR-05: Brecha de Precio por Variedad y Mercado (BPVM)
- **Fórmula**: $\text{BPVM}_{v, \text{base}} = \left(\frac{\text{PPMP}_{v} - \text{PPMP}_{\text{base}}}{\text{PPMP}_{\text{base}}}\right) \times 100\%$
- **Unidad**: Porcentaje (%).
- **Periodicidad**: Mensual / Anual.
- **Objetivo**: Medir la prima o castigo de precio de variedades premium (e.g., Criolla, Capiro) frente a la variedad base (Pastusa), o diferenciales de fletes entre ciudades.

### IND-PR-06: Magnitud de Choque Exógeno en Precios (MCEP)
- **Fórmula**: $\text{MCEP}_{\text{evento}} = \left(\frac{\text{PPMP}_{\text{evento}} - \overline{\text{PPMP}}_{\text{histórico homólogo}}}{\overline{\text{PPMP}}_{\text{histórico homólogo}}}\right) \times 100\%$
- **Unidad**: Porcentaje (%).
- **Periodicidad**: Por coyuntura (COVID 2020, Paro 2021, Crisis de Fertilizantes 2022–23, Clima).
- **Objetivo**: Aislar y cuantificar el desvío porcentual en las cotizaciones generado por eventos extraordinarios fuera del ciclo normal de mercado.

---

## 4. Matriz de Síntesis por Eje Analítico

| Código | Indicador | Eje Analítico | Unidad | Niveles de Desagregación Aplicables |
|--------|-----------|---------------|--------|--------------------------------------|
| **IND-OF-01** | Volumen Total Ofertado (VTO) | **Oferta** | Toneladas | Nacional, Departamental, Municipal, Variedad |
| **IND-OF-02** | Crecimiento Interanual (TCO) | **Oferta** | % | Nacional, Departamental, Variedad |
| **IND-OF-03** | Participación Zonas Productoras (PZP) | **Oferta** | % | Departamental, Municipal DIVIPOLA |
| **IND-OF-04** | Concentración Espacial (HHI-Oferta) | **Oferta** | Puntos (0-10k) | Nacional, Por Plaza de Destino |
| **IND-OF-05** | Índice Estacionalidad Oferta (IEO) | **Oferta** | Base 100 | Nacional, Por Variedad, Por Cuenca |
| **IND-OF-06** | Brecha Estacional Oferta (ABEO) | **Oferta** | % | Nacional, Por Variedad |
| **IND-OF-07** | Producción per-cápita (PPC) | **Oferta** | Ton y Kg / hab | Nacional, Departamental de Origen |
| **IND-DM-01** | Demanda Aparente (DA) | **Demanda** | Ton / Kg | Nacional, Por Variedad, Por Segmento |
| **IND-DM-02** | Población Colombia (POB_COL) | **Demanda** | Habitantes | Nacional, Departamental (DANE) |
| **IND-DM-03** | Consumo per-cápita Ton (CPC_TON) | **Demanda** | Ton/hab/año | Nacional, Por Variedad |
| **IND-DM-04** | Consumo per-cápita Kg (CPC_KG) | **Demanda** | Kg/hab/año | Nacional, Por Variedad (Pastusa, Capiro, Criolla) |
| **IND-DM-05** | Volumen Absorbido Plaza (VTA-Plaza) | **Demanda** | Toneladas | Por Central Mayorista, Por Ciudad |
| **IND-DM-06** | Cuota por Segmento (CD-Segmento) | **Demanda** | % | Nacional, Por Plaza Mayorista |
| **IND-DM-07** | Participación por Variedad (PVD) | **Demanda** | % | Nacional, Por Plaza, Por Mes |
| **IND-DM-08** | Sustitución Intervarietal (TSI) | **Demanda** | Puntos % | Nacional, Por Segmento de Uso |
| **IND-DM-09** | Dependencia de Consumo (CDC) | **Demanda** | % | Por Plaza Mayorista $\times$ Depto Origen |
| **IND-PR-01** | Precio Promedio Ponderado (PPMP) | **Precios** | COP/Kg | Nacional, Por Plaza, Por Variedad |
| **IND-PR-02** | Variación Temporal Precios (VTP) | **Precios** | % | Nacional, Por Plaza, Por Variedad |
| **IND-PR-03** | Coeficiente Volatilidad Precios (CVP) | **Precios** | % | Por Variedad, Por Plaza Mayorista |
| **IND-PR-04** | Sensibilidad Oferta-Precio (CSOP) | **Precios** | Elasticidad | Nacional, Por Variedad Líder |
| **IND-PR-05** | Brecha por Variedad/Plaza (BPVM) | **Precios** | % | Por Variedad vs. Base, Por Plaza vs. Centro |
| **IND-PR-06** | Choque Exógeno en Precios (MCEP) | **Precios** | % | Por Evento (COVID, Paro) $\times$ Plaza |

---

## 5. Estimadores Duales: Paramétrico vs. No Paramétrico por Indicador Clave

Para cada indicador, el análisis reportará formalmente los estimadores de ambos escenarios para garantizar una visión completa del mercado:

| Indicador Clave | Escenario 1: Estimador Paramétrico (Supone Normalidad / Transformación) | Escenario 2: Estimador No Paramétrico (Robusto / Distribution-Free) | Intervalo de Confianza (95%) Reportado |
|---|---|---|---|
| **Producción per-cápita (Kg)** | Producción promedio nacional/deptal ($\mu_{\text{PPC}}$) | Producción mediana departamental ($\tilde{x}_{\text{PPC}}$) | • Bootstrap BCa ($B=2,000$) por departamento |
| **Consumo per-cápita (Kg)** | Consumo promedio nacional derivado de $\mu_{\text{DA}}$ | Consumo mediano nacional derivado de $\tilde{x}_{\text{DA}}$ | • Rango empírico per cápita [Mín, Máx, Mediana] |
| **Volumen Ofertado Mensual** | Media aritmética ($\mu$) y Desviación estándar ($\sigma$) tras Log/Box-Cox | Mediana ($\tilde{x}$), Rango Intercuartílico ($\text{IQR}$) y $\text{MAD}$ | • Paramétrico: $t$-Student<br>• No Paramétrico: Bootstrap BCa ($B=2,000$) |
| **Precios Mayoristas Ponderados**| Media ponderada mensual ($\bar{P}$) y Varianza ($\sigma^2$) | Mediana ponderada ($\tilde{P}$) y Percentiles $P_{10} - P_{90}$ | • Paramétrico: $t$-Student<br>• No Paramétrico: Bootstrap BCa ($B=2,000$) |
| **Índice de Estacionalidad (IEO)** | Cociente de medias históricas con Winsorización al 1%-99% | Cociente de medianas históricas por mes calendario | • Bootstrap BCa sobre el cociente de medianas |
| **Concentración Espacial (HHI)** | $\sum (\mu_{\text{Participación}})^2$ | $\sum (\tilde{x}_{\text{Participación}})^2$ normalizada | • Bootstrap BCa sobre los $HHI$ anuales |
