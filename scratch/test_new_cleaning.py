import re
import unicodedata
import pandas as pd

MAPEO_VARIEDADES_CANONICAS = {
    "PAPA PASTUSA": "PAPA PASTUSA",
    "PAPA PARDA PASTUSA": "PAPA PARDA PASTUSA",
    "PAPA PARDA": "PAPA PARDA PASTUSA",
    "PAPA R-12 NEGRA": "PAPA PARDA PASTUSA",
    "PAPA SUPREMA": "PAPA PASTUSA SUPREMA",
    "PAPA PASTUSA SUPREMA": "PAPA PASTUSA SUPREMA",
    "PAPA DIACOL CAPIRO": "PAPA CAPIRO",
    "PAPA CAPIRO": "PAPA CAPIRO",
    "PAPA CAPIRA": "PAPA CAPIRO",
    "PAPA R-12 ROJA": "PAPA CAPIRO",
    "PAPA R-12": "PAPA R-12",
    "PAPA CRIOLLA": "PAPA CRIOLLA COLOMBIA",
    "PAPA CRIOLLA COLOMBIA": "PAPA CRIOLLA COLOMBIA",
    "PAPA CRIOLLA LIMPIA": "PAPA CRIOLLA COLOMBIA",
    "PAPA CRIOLLA SUCIA": "PAPA CRIOLLA COLOMBIA",
    "PAPA SUPERIOR": "PAPA SUPERIOR",
    "PAPA UNICA": "PAPA UNICA",
    "PAPA BETINA": "PAPA BETINA",
    "PAPA RUBI": "PAPA RUBI",
    "PAPA NEVADA": "PAPA NEVADA",
    "PAPA SABANERA": "PAPA SABANERA",
    "PAPA MORASURCO": "PAPA MORASURCO",
    "PAPA TUQUERREÑA": "PAPA TUQUERREÑA",
    "PAPA PURACE": "PAPA PURACE",
    "PAPA SAN FELIX": "PAPA SAN FELIX",
    "PAPA ICA-HUILA": "PAPA ICA HUILA",
}

def remover_acentos(texto: str) -> str:
    if not isinstance(texto, str):
        return ""
    # Reemplazos especificos de caracteres corruptos antes de normalizar
    t = texto.replace("", "")
    nfkd = unicodedata.normalize("NFKD", t)
    sin_tildes = "".join([c for c in nfkd if not unicodedata.combining(c)])
    limpio = re.sub(r"[^A-Z0-9\s,\-\.]", "", sin_tildes.upper())
    return " ".join(limpio.split())

def estandarizar_variedades(serie_variedad: pd.Series) -> pd.Series:
    def clasificar(val):
        texto = remover_acentos(str(val))
        # 1. Búsqueda directa en diccionario canónico
        for k, canonica in MAPEO_VARIEDADES_CANONICAS.items():
            k_clean = remover_acentos(k)
            if k_clean in texto or texto == k_clean:
                return canonica
        # 2. Reglas por palabras clave prioritarias
        if "CRIOLLA" in texto:
            return "PAPA CRIOLLA COLOMBIA"
        if "SUPERIOR" in texto:
            return "PAPA SUPERIOR"
        if "UNICA" in texto:
            return "PAPA UNICA"
        if "CAPIR" in texto:
            return "PAPA CAPIRO"
        if "PASTUSA" in texto:
            return "PAPA PASTUSA"
        if "BETINA" in texto:
            return "PAPA BETINA"
        if "SABANERA" in texto:
            return "PAPA SABANERA"
        if "MORASURCO" in texto:
            return "PAPA MORASURCO"
        if "RUB" in texto:
            return "PAPA RUBI"
        if "R-12" in texto or "R12" in texto:
            return "PAPA R-12"
        return "PAPA OTRAS VARIEDADES"

    return serie_variedad.apply(clasificar)

df = pd.read_parquet("data/CLEANED/dataset_sipsa_mensual_nacional.parquet")
res = estandarizar_variedades(df["variedad_papa"])
print("Distribución de variedades con el nuevo clasificador:")
print(res.value_counts())
print("\nTotal filas:", len(res))
print("Otras variedades:", (res == "PAPA OTRAS VARIEDADES").sum())
