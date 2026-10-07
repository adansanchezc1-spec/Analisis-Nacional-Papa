# Catálogo Maestro de Codificación DIVIPOLA — Colombia (DANE)

**Proyecto**: Análisis Crítico del Mercado de la Papa en Colombia (SIPSA 2019–2025)  
**Documento**: Diccionario y Catálogo Geográfico de Referencia Oficial  
**Fase PDCO**: PLAN → DEVELOPMENT  
**Fuente Base**: Departamento Administrativo Nacional de Estadística (DANE) — División Político-Administrativa de Colombia (DIVIPOLA)  
**Estándar**: DAMA-BOK (Gestión de Datos Maestros y de Referencia) / ISO/IEC 25010  

---

## 1. Fundamentos y Estructura Jerárquica del Código DIVIPOLA

El estándar **DIVIPOLA** es el sistema único y oficial de codificación territorial de Colombia establecido por el DANE para identificar de forma unívoca las entidades territoriales, unidades administrativas y asentamientos humanos del país.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   JERARQUÍA DEL CÓDIGO DIVIPOLA DANE                  │
├──────────────────────┬───────────────────────┬─────────────────────────┤
│ DEPARTAMENTO (DP)    │ MUNICIPIO (DPMP)      │ CENTRO POBLADO (DPCP)   │
│ Longitud: 2 dígitos  │ Longitud: 5 dígitos   │ Longitud: 8 dígitos     │
│ Ejemplo: 25          │ Ejemplo: 25875        │ Ejemplo: 25875001       │
│ Cundinamarca         │ Villapinzón           │ Inspección / Cabecera   │
└──────────────────────┴───────────────────────┴─────────────────────────┘
```

### 1.1 Reglas de Conformación del Código:
1. **Código de Departamento (`DP`)**: 2 dígitos numéricos que van del `'05'` al `'99'`.
2. **Código de Municipio (`DPMP`)**: 5 dígitos numéricos conformados por:
   * Los 2 primeros dígitos corresponden al Departamento (`DP`).
   * Los 3 últimos dígitos corresponden al orden cronológico de creación o asignación municipal (`MP`).
   * Las capitales de departamento terminan canónicamente en `'001'` (ej. `'11001'` Bogotá, D.C.; `'05001'` Medellín; `'52001'` Pasto; `'15001'` Tunja).
3. **Representación Computacional Obligatoria**:
   * **Tipo de dato**: `STRING` / `VARCHAR(5)` (NUNCA numérico entero o float, para evitar la pérdida del cero a la izquierda en departamentos `'05'` Antioquia y `'08'` Atlántico).

---

## 2. Catálogo Oficial de los 33 Departamentos de Colombia

Colombia cuenta con 32 departamentos y 1 Distrito Capital autónomo. A continuación se presenta el directorio completo de los 33 códigos departamentales, su capital y su rol en la cadena productiva y comercial de la papa:

| Código DP | Nombre Departamento Oficial DANE | Capital Oficial | Código Capital | Región Geográfica | Rol en la Cadena de la Papa |
|:---:|:---|:---|:---:|:---|:---|
| **05** | ANTIOQUIA | Medellín | `05001` | Andina Occidental | **Cuenca Productora Principal** (Oriente y Norte) / Nodo Consumidor |
| **08** | ATLÁNTICO | Barranquilla | `08001` | Caribe | **Nodo Consumidor Neto Mayorista** (Granabastos) |
| **11** | BOGOTÁ, D.C. | Bogotá, D.C. | `11001` | Andina Centro | **Nodo Consumidor Máximo de Colombia** (Corabastos) |
| **13** | BOLÍVAR | Cartagena de Indias | `13001` | Caribe | **Nodo Consumidor Neto Mayorista** (Bazurto) |
| **15** | BOYACÁ | Tunja | `15001` | Andina Centro | **Cuenca Productora Principal** (Altiplano Cundiboyacense) |
| **17** | CALDAS | Manizales | `17001` | Andina Eje Cafetero | Producción Secundaria (Zona Alta) / Consumidor (Centrogalerías) |
| **18** | CAQUETÁ | Florencia | `18001` | Amazonía | Consumidor Neto Periférico |
| **19** | CAUCA | Popayán | `19001` | Andina Sur | **Cuenca Productora Secundaria** (Silvia, Totoró) / Consumidor |
| **20** | CESAR | Valledupar | `20001` | Caribe | Consumidor Neto Mayorista (Mercabastos) |
| **23** | CÓRDOBA | Montería | `23001` | Caribe | Consumidor Neto Mayorista |
| **25** | CUNDINAMARCA | Bogotá, D.C. (Sede) | `25001` | Andina Centro | **Cuenca Productora Principal** (Sabana Centro, Ubaté, Almeidas) |
| **27** | CHOCÓ | Quibdó | `27001` | Pacífica | Consumidor Neto Periférico |
| **41** | HUILA | Neiva | `41001` | Andina Sur | Producción Secundaria / Nodo Consumidor (Surabastos) |
| **44** | LA GUAJIRA | Riohacha | `44001` | Caribe | Consumidor Neto |
| **47** | MAGDALENA | Santa Marta | `47001` | Caribe | Consumidor Neto Mayorista |
| **50** | META | Villavicencio | `50001` | Orinoquía | Consumidor Mayorista Clave (Cavipetrol / Central de Abastos) |
| **52** | NARIÑO | Pasto | `52001` | Andina Sur | **Cuenca Productora Principal** (Nudo de los Pastos / Ipiales / Túquerres) |
| **54** | NORTE DE SANTANDER | Cúcuta | `54001` | Andina Oriental | **Cuenca Productora Secundaria** (Pamplona, Silos, Mutiscua) / Consumidor |
| **63** | QUINDÍO | Armenia | `63001` | Andina Eje Cafetero | Consumidor Mayorista (Mercar) |
| **66** | RISARALDA | Pereira | `66001` | Andina Eje Cafetero | Consumidor Mayorista Estratégico (Mercasa) |
| **68** | SANTANDER | Bucaramanga | `68001` | Andina Oriental | **Cuenca Productora** (Berlín, Tona, Cerrito) / Consumidor (Centroabastos) |
| **70** | SUCRE | Sincelejo | `70001` | Caribe | Consumidor Neto |
| **73** | TOLIMA | Ibagué | `73001` | Andina Centro | **Cuenca Productora** (Murillo, Cajamarca) / Consumidor (Plaza La 21) |
| **76** | VALLE DEL CAUCA | Cali | `76001` | Pacífica / Andina | **Nodo Consumidor Máximo del Occidente** (Cavasa, Santa Elena) |
| **81** | ARAUCA | Arauca | `81001` | Orinoquía | Consumidor Neto Periférico |
| **85** | CASANARE | Yopal | `85001` | Orinoquía | Consumidor Neto |
| **86** | PUTUMAYO | Mocoa | `86001` | Amazonía | Consumidor Neto (Abastecido por Nariño) |
| **88** | SAN ANDRÉS Y PROVIDENCIA | San Andrés | `88001` | Insular | Consumidor Insular (Transporte Marítimo/Aéreo) |
| **91** | AMAZONAS | Leticia | `91001` | Amazonía | Consumidor Aislado |
| **94** | GUAINÍA | Inírida | `94001` | Amazonía | Consumidor Aislado |
| **95** | GUAVIARE | San José del Guaviare| `95001` | Orinoquía/Amazonía| Consumidor Neto |
| **97** | VAUPÉS | Mitú | `97001` | Amazonía | Consumidor Aislado |
| **99** | VICHADA | Puerto Carreño | `99001` | Orinoquía | Consumidor Aislado |

---

## 3. Directorio Municipal: Nodos Consumidores y Centrales Mayoristas SIPSA

Los mercados mayoristas monitoreados por el SIPSA operan en municipios cabecera con códigos DIVIPOLA de 5 dígitos específicos:

| Código DPMP | Municipio / Distrito | Departamento | Central Mayorista / Mercado SIPSA | Rol en el Abastecimiento |
|:---:|:---|:---|:---|:---|
| `11001` | **BOGOTÁ, D.C.** | Bogotá, D.C. | Corabastos / Paloquemao / Plaza Las Flores | Mayor centro de concentración y redistribución de Colombia |
| `05001` | **MEDELLÍN** | Antioquia | Plaza Minorista José María Villa | Centro de consumo masivo del Valle de Aburrá |
| `05360` | **ITAGÜÍ** | Antioquia | Central Mayorista de Antioquia (CMA) | Principal receptor del Oriente Antioqueño, Nariño y Altiplano |
| `76001` | **CALI** | Valle del Cauca | Santa Elena / Alameda / Siloé | Centro de consumo y distribución del suroccidente |
| `76130` | **CANDELARIA** | Valle del Cauca | CAVASA (Central de Abastecimientos del Valle) | Central mayorista abastecida por Nariño y Cundinamarca |
| `08001` | **BARRANQUILLA** | Atlántico | Barranquillita | Centro mayorista de distribución urbana en la Costa Atlántica |
| `08758` | **SOLEDAD** | Atlántico | Granabastos (Gran Central de Abastos del Caribe)| Principal puerto seco y despensa mayorista de la Costa Norte |
| `68001` | **BUCARAMANGA** | Santander | Centroabastos / Plaza San Francisco | Centro receptor de Santander, Boyacá y Norte de Santander |
| `54001` | **CÚCUTA** | Norte de Santander | Cenabastos / Nueva Sexta | Mercado fronterizo abastecido por Mutiscua, Pamplona y Boyacá |
| `66001` | **PEREIRA** | Risaralda | MERCASA | Nodo logístico del Eje Cafetero y Chocó |
| `17001` | **MANIZALES** | Caldas | Centrogalerías | Mercado regional abastecido por Cundinamarca y Boyacá |
| `63001` | **ARMENIA** | Quindío | MERCAR | Mercado de concentración del Quindío y norte del Valle |
| `73001` | **IBAGUÉ** | Tolima | Plaza La 21 / Plaza La 14 / Plaza El Jardín | Mercado receptor de Murillo, Cajamarca y Sabana de Bogotá |
| `41001` | **NEIVA** | Huila | SURABASTOS | Centro logístico del Alto Magdalena |
| `52001` | **PASTO** | Nariño | El Potrerillo / Los Dos Puentes | Mayor centro de acopio y salida de la cuenca sur hacia el país |
| `15001` | **TUNJA** | Boyacá | Plaza de Mercado del Sur | Centro de acopio central de la cuenca boyacense |
| `15759` | **SOGAMOSO** | Boyacá | Plaza de Mercado Sugamuxi | Centro de acopio de Sugamuxi y Tota |
| `15238` | **DUITAMA** | Boyacá | Plaza Mayorista de Duitama | Centro de acopio de Tundama y norte de Boyacá |
| `50001` | **VILLAVICENCIO** | Meta | Central de Abastos de Villavicencio (Cavipetrol) | Puerta de entrada y consumo para los Llanos Orientales |
| `13001` | **CARTAGENA** | Bolívar | Mercado de Bazurto | Consumo masivo costero |
| `47001` | **SANTA MARTA** | Magdalena | Mercado Público de Santa Marta | Consumo masivo turístico y residencial |
| `20001` | **VALLEDUPAR** | Cesar | Mercabastos | Centro de consumo del Cesar y sur de La Guajira |
| `23001` | **MONTERÍA** | Córdoba | Mercado del Sur | Centro de consumo de las sabanas de Córdoba y Sucre |
| `19001` | **POPAYÁN** | Cauca | Las Palmas / Plaza del Barrio Bolívar | Mercado de distribución del Cauca |

---

## 4. Directorio Completo de Cuencas Paperas de Colombia (Municipios Productores)

Las 4 regiones productoras de papa en Colombia concentran el 95% de la oferta nacional. A continuación se desglosan todos los municipios productores con su código DIVIPOLA DANE de 5 dígitos, subregión y variedades cultivadas:

### 4.1 Departamento de CUNDINAMARCA (`DP = '25'`)
*Concentra aproximadamente el 37% de la producción nacional.*

| Código DPMP | Municipio | Subregión Agrícola | Variedades Principales | Destino Primario |
|:---:|:---|:---|:---|:---|
| `25875` | **VILLAPINZÓN** | Almeidas / Valle de Ubaté | Diacol Capiro, Pastusa Suprema, Parda Pastusa | Corabastos, Industria de Chips |
| `25175` | **CHOCONTÁ** | Almeidas | Diacol Capiro, Pastusa Suprema, Criolla | Corabastos, Abasto Regional |
| `25899` | **ZIPAQUIRÁ** | Sabana Centro | Pastusa Suprema, Diacol Capiro, Criolla | Corabastos, Paloquemao |
| `25793` | **TAUSA** | Sabana Centro / Ubaté | Diacol Capiro, Pastusa Suprema | Corabastos, Industria |
| `25769` | **SUBACHOQUE** | Sabana Occidente | Pastusa Suprema, Parda Pastusa, Criolla | Corabastos, Mercados Especializados |
| `25154` | **CARMEN DE CARUPA** | Valle de Ubaté | Diacol Capiro, Suprema, Parda Pastusa | Corabastos, Bucaramanga |
| `25843` | **UBATÉ (VILLA DE SAN DIEGO)**| Valle de Ubaté | Pastusa Suprema, Capiro | Centro de Acopio y Comercio |
| `25745` | **SIMIJACA** | Valle de Ubaté | Pastusa Suprema, Capiro | Mercado Regional Boyacá-Cundinamarca |
| `25269` | **FACATATIVÁ** | Sabana Occidente | Pastusa Suprema, Criolla | Corabastos, Industria de Fritos |
| `25430` | **MADRID** | Sabana Occidente | Pastusa Suprema | Corabastos |
| `25473` | **MOSQUERA** | Sabana Occidente | Pastusa Suprema, Capiro | Agroindustria de Congelados |
| `25740` | **SIBATÉ** | Soacha / Sabana Sur | Parda Pastusa, Suprema, Criolla | Corabastos, Bogotá Sur |
| `25530` | **PASCA** | Sumapaz | Parda Pastusa, Criolla Colombia | Corabastos, Llano |
| `25322` | **GUASCA** | Guavio | Criolla Colombia, Pastusa Suprema, Tuquerreña| Corabastos, Paloquemao |
| `25736` | **SESQUILÉ** | Almeidas | Pastusa Suprema, Capiro | Corabastos |
| `25772` | **SUESCA** | Almeidas | Pastusa Suprema, Capiro | Corabastos |
| `25200` | **COGUA** | Sabana Centro | Pastusa Suprema, Capiro | Corabastos |
| `25486` | **NEMOCÓN** | Sabana Centro | Pastusa Suprema, Criolla | Corabastos |
| `25407` | **LENGUAZAQUE** | Valle de Ubaté | Capiro, Suprema | Ubaté, Corabastos |
| `25224` | **CUCUNUBÁ** | Valle de Ubaté | Capiro, Parda Pastusa | Ubaté, Corabastos |
| `25307` | **GUATAVITA** | Guavio | Criolla, Suprema | Corabastos |
| `25758` | **SOPÓ** | Sabana Centro | Suprema, Criolla | Corabastos |
| `25754` | **SOACHA** | Soacha | Criolla, Parda Pastusa | Corabastos |
| `25386` | **LA CALERA** | Guavio | Criolla Colombia, Parda Pastusa | Mercados Bogotá |

---

### 4.2 Departamento de BOYACÁ (`DP = '15'`)
*Concentra aproximadamente el 27% de la producción nacional.*

| Código DPMP | Municipio | Subregión Agrícola | Variedades Principales | Destino Primario |
|:---:|:---|:---|:---|:---|
| `15861` | **VENTAQUEMADA** | Centro Boyacá | Pastusa Suprema, Diacol Capiro, Criolla | Corabastos, Plaza del Sur Tunja |
| `15646` | **SAMACÁ** | Centro Boyacá | Diacol Capiro, Suprema, Rubí | Corabastos, Centroabastos |
| `15740` | **SIACHOQUE** | Centro Boyacá | Pastusa Suprema, Parda Pastusa, Criolla | Tunja, Corabastos |
| `15764` | **SORACÁ** | Centro Boyacá | Pastusa Suprema, Parda Pastusa, Criolla | Tunja, Corabastos |
| `15814` | **TOCA** | Centro Boyacá | Diacol Capiro, Pastusa Suprema | Corabastos, Costa Atlántica |
| `15187` | **CHIVATÁ** | Centro Boyacá | Pastusa Suprema, Criolla | Tunja, Bucaramanga |
| `15204` | **CÓMBITA** | Centro Boyacá | Pastusa Suprema, Capiro | Tunja, Bucaramanga |
| `15047` | **AQUITANIA** | Sugamuxi | Pastusa Suprema, Parda Pastusa, Criolla | Sogamoso, Llanos Orientales |
| `15516` | **PAIPA** | Tundama | Pastusa Suprema, Capiro | Duitama, Bucaramanga |
| `15051` | **ARCABUCO** | Ricaurte | Criolla Colombia, Parda Pastusa | Tunja, Moniquirá |
| `15632` | **SABOYÁ** | Occidente Boyacá | Pastusa Suprema, Capiro | Chiquinquirá, Corabastos |
| `15600` | **RÁQUIRA** | Ricaurte | Suprema, Criolla | Ubaté, Chiquinquirá |
| `15162` | **CERINZA** | Tundama | Pastusa Suprema, Parda Pastusa | Duitama, Costa Atlántica |
| `15693` | **SANTA ROSA DE VITERBO** | Tundama | Pastusa Suprema, Criolla | Duitama, Bucaramanga |
| `15469` | **MONIQUIRÁ** | Ricaurte | Criolla | Barbosa, Bucaramanga |
| `15455` | **MIRAFLORES** | Lengupá | Criolla | Tunja, Yopal |
| `15514` | **PACHAVITA** | Neira | Criolla | Garagoa, Bogotá |
| `15837` | **TUTA** | Tundama | Suprema, Capiro | Duitama, Tunja |
| `15476` | **MOTAVITA** | Centro Boyacá | Pastusa Suprema | Tunja |
| `15531` | **PESCA** | Sugamuxi | Parda Pastusa, Suprema, Criolla | Sogamoso, Bogotá |

---

### 4.3 Departamento de NARIÑO (`DP = '52'`)
*Concentra aproximadamente el 20% de la producción nacional (Núcleo de mayor rendimiento por hectárea).*

| Código DPMP | Municipio | Subregión Agrícola | Variedades Principales | Destino Primario |
|:---:|:---|:---|:---|:---|
| `52838` | **TÚQUERRES** | Sabana de Túquerres | Diacol Capiro, Pastusa Suprema, Parda Pastusa | Cali (CAVASA), Potrerillo, Medellín |
| `52356` | **IPIALES** | Exprovincia de Obando | Diacol Capiro, Suprema, Parda Pastusa | CAVASA, Corabastos, Ecuador |
| `52317` | **GUACHUCAL** | Altiplano de Túquerres | Diacol Capiro, Suprema | CAVASA, CMA Medellín |
| `52560` | **PUPIALES** | Exprovincia de Obando | Pastusa Suprema, Capiro, Criolla | Ipiales, Cali |
| `52227` | **CUMBAL** | Sabana de Túquerres | Diacol Capiro, Parda Pastusa | Ipiales, Cali |
| `52224` | **CUASPUD (CARLOSAMA)**| Exprovincia de Obando | Diacol Capiro, Suprema | Ipiales, CAVASA |
| `52022` | **ALDANA** | Exprovincia de Obando | Pastusa Suprema, Capiro | Ipiales, Cali |
| `52207` | **CONTADERO** | Exprovincia de Obando | Pastusa Suprema, Criolla | Pasto, Ipiales |
| `52320` | **GUALMATÁN** | Exprovincia de Obando | Suprema, Parda Pastusa | Ipiales, Cali |
| `52352` | **ILES** | Exprovincia de Obando | Suprema, Parda Pastusa | Pasto, Potrerillo |
| `52506` | **OSPINA** | Sabana de Túquerres | Diacol Capiro, Suprema | Túquerres, CAVASA |
| `52720` | **SAPUYES** | Sabana de Túquerres | Diacol Capiro, Suprema | Túquerres, CAVASA |
| `52885` | **YACUANQUER** | Centro Nariño | Pastusa Suprema, Criolla | Potrerillo Pasto |
| `52786` | **TANGUA** | Centro Nariño | Criolla, Pastusa Suprema | Potrerillo Pasto |
| `52381` | **LA FLORIDA** | Galeras / Occidente | Criolla, Pastusa Suprema | Pasto |
| `52203` | **COLÓN (GÉNOVA)** | Norte Nariño | Suprema, Criolla | La Unión, Popayán |
| `52256` | **EL ROSARIO** | Cordillera | Criolla | Pasto |
| `52678` | **SAMANIEGO** | Occidente Nariño | Criolla, Pastusa Suprema | Pasto, Tumaco |

---

### 4.4 Departamento de ANTIOQUIA (`DP = '05'`)
*Concentra el 14% de la producción nacional (Alta especialización en Diacol Capiro e industria).*

| Código DPMP | Municipio | Subregión Agrícola | Variedades Principales | Destino Primario |
|:---:|:---|:---|:---|:---|
| `05400` | **LA UNIÓN** | Oriente Antioqueño | Diacol Capiro (Industrial y Consumo), Criolla | CMA Itagüí, Minorista Medellín, Industria |
| `05756` | **SONSÓN** | Oriente Antioqueño | Diacol Capiro, Criolla, Nevada | CMA Itagüí, La Unión |
| `05674` | **SAN VICENTE FERRER** | Oriente Antioqueño | Diacol Capiro, Criolla | Marinilla, CMA Itagüí |
| `05440` | **MARINILLA** | Oriente Antioqueño | Diacol Capiro, Criolla | Centro de Acopio del Oriente, CMA |
| `05148` | **EL CARMEN DE VIBORAL**| Oriente Antioqueño | Diacol Capiro, Criolla | CMA Itagüí, Rionegro |
| `05686` | **SANTA ROSA DE OSOS** | Norte Antioqueño | Diacol Capiro | Medellín Minorista, CMA |
| `05664` | **SAN PEDRO DE LOS MILAGROS**| Norte Antioqueño | Diacol Capiro, Pastusa Suprema | CMA Itagüí |
| `05264` | **ENTRERRÍOS** | Norte Antioqueño | Diacol Capiro | CMA Itagüí |
| `05086` | **BELMIRA** | Norte Antioqueño | Diacol Capiro, Suprema | Medellín |
| `05887` | **YARUMAL** | Norte Antioqueño | Diacol Capiro | CMA Itagüí, Costa Norte |
| `05615` | **RIONEGRO** | Oriente Antioqueño | Criolla, Capiro | Abasto Local, Industria |
| `05318` | **GUARNE** | Oriente Antioqueño | Capiro, Criolla | CMA Itagüí |
| `05252` | **EL SANTUARIO** | Oriente Antioqueño | Diacol Capiro | Marinilla, CMA Itagüí |

---

### 4.5 Departamento de SANTANDER (`DP = '68'`) Y NORTE DE SANTANDER (`DP = '54'`)
*Cuenca del Páramo de Santurbán y Berlín (Altiplano Oriental).*

| Código DPMP | Municipio | Departamento | Subregión Agrícola | Variedades | Destino Primario |
|:---:|:---|:---|:---|:---|:---|
| `68820` | **TONA (BERLÍN)** | Santander | Soto Norte / Santurbán | Pastusa Suprema, Diacol Capiro, Parda | Centroabastos Bucaramanga |
| `68162` | **CERRITO** | Santander | García Rovira | Parda Pastusa, Suprema, Criolla | Centroabastos, Málaga |
| `68318` | **GUACA** | Santander | García Rovira | Pastusa Suprema, Criolla | Bucaramanga |
| `68655` | **SAN ANDRÉS** | Santander | García Rovira | Pastusa Suprema, Criolla | Bucaramanga |
| `68207` | **CONCEPCIÓN** | Santander | García Rovira | Suprema, Parda Pastusa | Málaga, Bucaramanga |
| `68432` | **MÁLAGA** | Santander | García Rovira | Suprema, Parda Pastusa | Centro de Acopio Provincial |
| `54480` | **MUTISCUA** | Norte de Santander | Ricaurte / Santurbán | Diacol Capiro, Suprema, Criolla | Cenabastos Cúcuta, Bucaramanga |
| `54518` | **PAMPLONA** | Norte de Santander | Centro Prov. Pamplona | Diacol Capiro, Pastusa Suprema | Cenabastos Cúcuta |
| `54743` | **SILOS** | Norte de Santander | Prov. Pamplona | Suprema, Diacol Capiro | Cúcuta, Bucaramanga |
| `54206` | **CHITAGÁ** | Norte de Santander | Prov. Pamplona | Pastusa Suprema, Capiro | Cúcuta, Duitama |
| `54125` | **CÁCOTA** | Norte de Santander | Prov. Pamplona | Suprema, Criolla | Pamplona, Cúcuta |

---

### 4.6 Departamentos de TOLIMA (`DP = '73'`) Y CAUCA (`DP = '19'`)
*Cuencas de Cordillera Central y Macizo Colombiano.*

| Código DPMP | Municipio | Departamento | Subregión Agrícola | Variedades | Destino Primario |
|:---:|:---|:---|:---|:---|:---|
| `73461` | **MURILLO** | Tolima | Nevado del Ruiz | Pastusa Suprema, Diacol Capiro, Criolla | Plaza La 21 Ibagué, Manizales |
| `73124` | **CAJAMARCA** | Tolima | Cordillera Central / Anaime | Pastusa Suprema, Capiro | Ibagué, Armenia |
| `73622` | **RONCESVALLES**| Tolima | Cordillera Central Sur | Pastusa Suprema, Criolla | Ibagué |
| `73678` | **SANTA ISABEL** | Tolima | Nevados | Suprema, Criolla | Ibagué |
| `73347` | **HERVEO** | Tolima | Cordillera Central | Suprema, Capiro | Manizales, Fresno |
| `19743` | **SILVIA** | Cauca | Tierradentro / Guambía | Parda Pastusa, Criolla, Suprema | Popayán, CAVASA Cali |
| `19824` | **TOTORÓ** | Cauca | Cordillera Central | Parda Pastusa, Criolla | Popayán, CAVASA Cali |
| `19573` | **PURACÉ (COCONUCO)**| Cauca | Macizo Colombiano | Criolla, Parda Pastusa | Popayán |
| `19355` | **INZÁ** | Cauca | Tierradentro | Criolla, Parda Pastusa | Popayán, La Plata (Huila) |

---

## 5. Protocolo de Calidad y Limpieza de Códigos DIVIPOLA en Datos Crudos (SIPSA)

Al integrar datos de precios y volúmenes de SIPSA (archivos SAS, DTA, SAV y CSV), se deben aplicar las siguientes reglas maestras de gobernanza de datos (DAMA-BOK):

### 5.1 Función Canónica de Sanitización de Llaves en Python
```python
import re
import pandas as pd


def sanitizar_codigo_divipola(serie_codigo: pd.Series, longitud: int = 5) -> pd.Series:
    """
    Sanitiza y normaliza códigos DIVIPOLA garantizando formato string
    y rellenado de ceros a la izquierda (zfill).
    longitud = 2 para Departamento, 5 para Municipio.
    """
    def limpiar_valor(val):
        if pd.isna(val) or val is None:
            return None
        # Convertir float 5001.0 a entero 5001 antes de string
        val_str = str(val).strip()
        if val_str.endswith(".0"):
            val_str = val_str[:-2]
        # Extraer solo dígitos numéricos
        digitos = re.sub(r"\D", "", val_str)
        if not digitos:
            return None
        return digitos.zfill(longitud)

    return serie_codigo.apply(limpiar_valor)
```

### 5.2 Diccionario de Resolución de Homónimos y Errores de Transcripción Frecuentes
| Texto Crudo en SIPSA | Departamento Inferido | Código DIVIPOLA Resuelto | Nombre Oficial Canónico DANE |
|:---|:---|:---:|:---|
| `'BOGOTA'` / `'BOGOTA D.C.'` | Bogotá, D.C. | `11001` | BOGOTÁ, D.C. |
| `'MEDELLIN'` / `'CMA'` | Antioquia | `05001` / `05360` | MEDELLÍN / ITAGÜÍ |
| `'CALI'` / `'CAVASA'` | Valle del Cauca | `76001` / `76130` | SANTIAGO DE CALI / CANDELARIA |
| `'BARRANQUILLA'` / `'GRANABASTOS'` | Atlántico | `08001` / `08758`| BARRANQUILLA / SOLEDAD |
| `'TUNJA'` | Boyacá | `15001` | TUNJA |
| `'PASTO'` / `'POTRERILLO'` | Nariño | `52001` | PASTO |
| `'BUCARAMANGA'` / `'CENTROABASTOS'`| Santander | `68001` | BUCARAMANGA |
| `'VILLAPINZON'` | Cundinamarca | `25875` | VILLAPINZÓN |
| `'TUQUERRES'` | Nariño | `52838` | TÚQUERRES |
| `'LA UNION'` (Antioquia) | Antioquia | `05400` | LA UNIÓN |
| `'LA UNION'` (Nariño) | Nariño | `52399` | LA UNIÓN |
| `'LA UNION'` (Valle) | Valle del Cauca | `76400` | LA UNIÓN |

> **Regla de Integridad Referencial**: Para desambiguar municipios homónimos (como *La Unión* en Antioquia, Nariño o Valle), la llave relacional debe componerse siempre de `(divipola_depto, divipola_mpio)` o validarse contra el código departamental del mercado o de la cuenca productora reportada en el encadenamiento de SIPSA.
