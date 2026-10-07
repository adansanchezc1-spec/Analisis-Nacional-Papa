// ==============================================================================
// CÓDIGO POWER QUERY (M) LISTO PARA COPIAR Y PEGAR EN POWER BI
// Ruta de datos: C:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando\data\POWERBI
// ==============================================================================
// INSTRUCCIONES RÁPIDAS EN POWER BI:
// 1. En la cinta Inicio de Power BI, haz clic en "Transformar datos" (se abre Power Query).
// 2. Haz clic en "Nueva consulta" -> "Consulta en blanco".
// 3. Haz clic en "Editor avanzado" en la cinta superior.
// 4. Borra todo lo que haya en la ventana y pega el bloque correspondiente a cada tabla.
// 5. Haz clic en "Listo" y renombra la consulta (ej. Dim_Tiempo).
// ==============================================================================

// ------------------------------------------------------------------------------
// CONSULTA 1: Dim_Tiempo
// Nombre de la consulta: Dim_Tiempo
// ------------------------------------------------------------------------------
let
    Origen = Csv.Document(File.Contents("C:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando\data\POWERBI\Dim_Tiempo.csv"),[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados,{
        {"fecha", type date},
        {"id_tiempo", Int64.Type},
        {"año", Int64.Type},
        {"mes", Int64.Type},
        {"nombre_mes", type text},
        {"mes_corto", type text},
        {"año_mes", type text},
        {"trimestre", type text},
        {"año_trimestre", type text},
        {"semestre", type text},
        {"año_semestre", type text},
        {"periodo_agricola", type text},
        {"orden_año_mes", Int64.Type}
    })
in
    Tipos

// ------------------------------------------------------------------------------
// CONSULTA 2: Dim_Geografia
// Nombre de la consulta: Dim_Geografia
// ------------------------------------------------------------------------------
let
    Origen = Csv.Document(File.Contents("C:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando\data\POWERBI\Dim_Geografia.csv"),[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados,{
        {"cod_depto", type text},
        {"departamento", type text},
        {"cod_mpio", type text},
        {"municipio", type text},
        {"region_natural", type text},
        {"es_productor_destacado", type logical}
    })
in
    Tipos

// ------------------------------------------------------------------------------
// CONSULTA 3: Dim_Variedad
// Nombre de la consulta: Dim_Variedad
// ------------------------------------------------------------------------------
let
    Origen = Csv.Document(File.Contents("C:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando\data\POWERBI\Dim_Variedad.csv"),[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados,{
        {"cod_variedad", type text},
        {"nombre_variedad", type text},
        {"variedad_canonica", type text},
        {"nombre_cientifico", type text},
        {"ciclo_fenologico_dias", Int64.Type},
        {"segmento_mercado", type text},
        {"descripcion", type text}
    })
in
    Tipos

// ------------------------------------------------------------------------------
// CONSULTA 4: Dim_Mercado
// Nombre de la consulta: Dim_Mercado
// ------------------------------------------------------------------------------
let
    Origen = Csv.Document(File.Contents("C:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando\data\POWERBI\Dim_Mercado.csv"),[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados,{
        {"id_mercado", Int64.Type},
        {"mercado_mayorista", type text},
        {"cod_mpio", type text},
        {"nombre_mpio", type text},
        {"cod_depto", type text},
        {"nombre_depto", type text},
        {"tipo_hub_logistico", type text}
    })
in
    Tipos

// ------------------------------------------------------------------------------
// CONSULTA 5: Fact_Produccion_EVA
// Nombre de la consulta: Fact_Produccion_EVA
// ------------------------------------------------------------------------------
let
    Origen = Csv.Document(File.Contents("C:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando\data\POWERBI\Fact_Produccion_EVA.csv"),[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados,{
        {"id_tiempo", Int64.Type},
        {"cod_mpio", type text},
        {"cod_variedad", type text},
        {"area_sembrada_ha", type number},
        {"area_cosechada_ha", type number},
        {"produccion_ton", type number},
        {"rendimiento_ton_ha", type number},
        {"tasa_perdida_cosecha_pct", type number},
        {"produccion_per_capita_nacional_kg", type number}
    })
in
    Tipos

// ------------------------------------------------------------------------------
// CONSULTA 6: Fact_Abastecimiento_SIPSA
// Nombre de la consulta: Fact_Abastecimiento_SIPSA
// ------------------------------------------------------------------------------
let
    Origen = Csv.Document(File.Contents("C:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando\data\POWERBI\Fact_Abastecimiento_SIPSA.csv"),[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados,{
        {"id_tiempo", Int64.Type},
        {"id_mercado", Int64.Type},
        {"cod_variedad", type text},
        {"volumen_ingreso_ton", type number},
        {"indice_estacional_oferta_ieo", type number},
        {"consumo_mayorista_per_capita_kg", type number}
    })
in
    Tipos

// ------------------------------------------------------------------------------
// CONSULTA 7: Fact_Precios_SIPSA
// Nombre de la consulta: Fact_Precios_SIPSA
// ------------------------------------------------------------------------------
let
    Origen = Csv.Document(File.Contents("C:\Users\ADAN\OneDrive\Documentos\analisispapamercadoorlando\data\POWERBI\Fact_Precios_SIPSA.csv"),[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Encabezados = Table.PromoteHeaders(Origen, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados,{
        {"id_tiempo", Int64.Type},
        {"id_mercado", Int64.Type},
        {"cod_variedad", type text},
        {"precio_prom_kg", type number},
        {"precio_min_kg", type number},
        {"precio_max_kg", type number},
        {"spread_precios_kg", type number},
        {"num_transacciones", Int64.Type},
        {"indice_estacional_precio_iep", type number}
    })
in
    Tipos
