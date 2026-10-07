# Manual de Detección y Tratamiento de Anomalías (Outliers)

**Proyecto**: Análisis Histórico del Mercado de la Papa en Colombia (2019 - 2025)  
**Fuente**: Microdatos SIPSA - DANE  
**Estándar de Calidad**: DAMA-BOK (Calidad de Datos, Consistencia y Validez)  

---

## 1. Clasificación Conceptual de Anomalías

En el análisis de series de tiempo agropecuarias, una anomalía o valor atípico no debe eliminarse de forma automática. Se clasifica en dos naturalezas categóricamente distintas:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   TIPOLOGÍA DE VALORES ATÍPICOS                        │
├────────────────────────────────────┬───────────────────────────────────┤
│ TIPO A: ERRORES DE DATOS           │ TIPO B: ANOMALÍAS DE MERCADO      │
│ (Ruido / Falla Técnica)            │ (Eventos Reales de Alta Relevancia│
├────────────────────────────────────┼───────────────────────────────────┤
│ • Errores de digitación en plaza   │ • Desplome de oferta por paros    │
│   (ej. 100,000 kg en un camión de  │   viales (mayo-junio 2021)        │
│   3 toneladas)                     │ • Picos de escasez por heladas    │
│ • Formato de miles con puntos      │   en páramo o sequía severa       │
│   (ej. " 9.000 " interpretado como │ • Ventanas de sobreoferta por     │
│   9 kg en vez de 9,000 kg)         │   cosechas concurrentes récord    │
│ • Cantidades negativas o en cero   │ • Distorsiones puntuales por      │
│ • Códigos DIVIPOLA inexistentes    │   compras institucionales masivas │
├────────────────────────────────────┼───────────────────────────────────┤
│ ACCIÓN: Corregir o Imputar         │ ACCIÓN: Preservar y Marcar (Flag) │
└────────────────────────────────────┴───────────────────────────────────┘
```

---

## 2. Batería de Métodos de Detección de Anomalías

### 2.1 Métodos Univariados

#### A. Rango Intercuartílico (IQR / Criterio de Tukey)
- **Fórmula**:
  $$\text{IQR} = Q_3 - Q_1$$
  $$\text{Límite Inferior Moderado} = Q_1 - 1.5 \times \text{IQR}, \quad \text{Límite Superior Moderado} = Q_3 + 1.5 \times \text{IQR}$$
  $$\text{Límite Inferior Severo} = Q_1 - 3.0 \times \text{IQR}, \quad \text{Límite Superior Severo} = Q_3 + 3.0 \times \text{IQR}$$
- **Uso**: Detección rápida de transacciones con volúmenes atípicos dentro de cada variedad y plaza.

#### B. Z-Score Modificado (Basado en la Mediana y el MAD)
El Z-Score convencional ($\frac{x - \mu}{\sigma}$) se distorsiona fuertemente por la presencia de los mismos outliers. Se utiliza el **Z-Score modificado de Iglewicz y Hoaglin**:
- **Desviación Absoluta de la Mediana (MAD)**:
  $$\text{MAD} = \text{mediana}(|x_i - \tilde{x}|)$$
- **Puntuación modificada ($M_i$)**:
  $$M_i = \frac{0.6745 \times (x_i - \tilde{x})}{\text{MAD}}$$
- **Umbral de Decisión**: Se clasifica como atípico si $|M_i| > 3.5$.

---

### 2.2 Métodos Multivariados y Contextuales

#### A. Isolation Forest (Bosque de Aislamiento)
- **Variables de entrada**: `[Volumen Kg, Precio por Kg, Mes Calendario, Distancia Estimada Km]`.
- **Principio**: Los valores atípicos son escasos y diferentes, por lo que se aíslan en las ramas más cortas de árboles de decisión aleatorios.
- **Puntuación de Anomalía**:
  $$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$
  *Si $s > 0.65$, la transacción se etiqueta como anomalía multivariada.*

#### B. Distancia de Mahalanobis Robusta (MCD - Minimum Covariance Determinant)
- Permite detectar combinaciones anómalas (e.g., volumen moderado pero con precio desorbitado para esa época del año), controlando la matriz de covarianza robusta.

---

## 3. Protocolo de Tratamiento de Valores Atípicos

```mermaid
flowchart TD
    DET["Detección de Valor Atípico (IQR, MAD o Isolation Forest)"] --> EVAL{"Evaluación de Naturaleza:\n¿Es Error de Captura o Realidad de Mercado?"}

    EVAL -->|Error de Formato / Digitación| CORR["1. Corrección Específica\n• Limpiar espacios y puntos de miles\n• Corregir factor de escala (x1000)"]
    CORR --> VAL_CORR{¿Persiste Inválido?}
    VAL_CORR -->|Sí| IMPUT["2. Imputación Controlada\n• Mediana mensual de la variedad en esa plaza\n• Registrar en bitácora de auditoría"]
    VAL_CORR -->|No| RES_OK["Registro Corregido"]

    EVAL -->|Choque Real de Mercado\n(COVID, Paro, Helada)| FLAG["3. Preservación con Etiqueta (Flagging)\n• flag_anomalia_mercado = TRUE\n• motivo: 'Paro Nacional 2021' o 'Helada'\n• Mantener en análisis de choques y estacionalidad"]
    
    FLAG --> WINS{"¿Se requiere para Modelo Paramétrico o Regresión?"}
    WINS -->|Sí| WINS_APPLY["4. Winsorización al percentil 1% y 99%\n(Para estabilizar varianza sin sesgar)"]
    WINS -->|No: Análisis de Descriptivo/Coyuntura| MANT["Mantener valor crudo intacto"]
```

---

## 4. Estrategias de Tratamiento Formalizadas

### 4.1 Limpieza y Corrección Automática
- **Problema de formato en 2024–2025**: Campos con formato ` 9.000 ` o `'0151001`.
  - **Regla**: Eliminar espacios en blanco y comillas simples (`'`). Si el campo contiene un punto que actúa como separador de miles en Colombia (e.g., `9.000` representando 9,000 kg), normalizar a valor entero/flotante `9000.0`.
- **Valores menores o iguales a cero**: Descartar transacciones con `Cant Kg <= 0` e incluirlas en la bitácora de registros inválidos.

### 4.2 Winsorización (Para Estimaciones Sensibles a Colas)
En los análisis donde los valores extremos distorsionan las medias interanuales:
$$x_i^{\text{winsor}} = \begin{cases} P_{01}, & \text{si } x_i < P_{01} \\ x_i, & \text{si } P_{01} \le x_i \le P_{99} \\ P_{99}, & \text{si } x_i > P_{99} \end{cases}$$
*Donde $P_{01}$ y $P_{99}$ son los percentiles 1 y 99 respectivamente calculados dentro de cada combinación de (Año, Variedad).*

### 4.3 Imputación por Mediana Condicional
Si un registro presenta un valor corrompido irreparable pero los demás campos son válidos:
$$\hat{x}_{i} = \text{mediana}\left(\text{Volumen de la variedad } v \text{ en la plaza } p \text{ durante el mes } m\right)$$

---

## 5. Bitácora de Registro y Gobernanza de Anomalías

Cada intervención de corrección o imputación debe registrar los siguientes metadatos de auditoría:

| Campo de Auditoría | Descripción |
|---|---|
| `id_registro` | Identificador único de la fila del microdato. |
| `periodo_archivo` | Archivo SIPSA de origen (e.g., `2021 ( I Semestre).csv`). |
| `variable_afectada` | Campo objetivo (`Cant Kg`, `FechaEncuesta`, etc.). |
| `valor_original` | Valor textual bruto antes de la transformación. |
| `valor_tratado` | Valor numérico final tras la regla de tratamiento. |
| `metodo_deteccion` | `IQR_SEVERO`, `MAD_ZSCORE`, `FORMAT_ERROR`, `REGRESIÓN`. |
| `accion_tomada` | `CORRECCION_FORMATO`, `WINSORIZADO`, `IMPUTADO_MEDIANA`, `FLAG_PRESERVADO`. |
| `justificacion_negocio`| Explicación de la decisión técnica según el contexto del mercado. |
