import tempfile
from pathlib import Path
import pandas as pd

temp_file = Path(tempfile.gettempdir()) / "audit_eva_copy.xlsx"

print("Reading BaseSIPRA...")
df_sipra = pd.read_excel(
    temp_file, 
    sheet_name="BaseSIPRA", 
    usecols=['codigoDepartamento', 'departamento', 'codigoMunicipio', 'municipio', 'especie', 'nombre_tipo_ciclo', 'grupo_especie', 'subGrupo_Especie', 'anho', 'Periodo', 'AreaSembrada', 'AreaCosechada', 'produccio', 'rendimiento']
)

print("BaseSIPRA shape:", df_sipra.shape)
papa_sipra = df_sipra[df_sipra["especie"].astype(str).str.upper().str.contains("PAPA")]
print("Potato in BaseSIPRA rows:", len(papa_sipra))
print("Unique especies:", papa_sipra["especie"].unique())
print("Unique Periodo in BaseSIPRA:", papa_sipra["Periodo"].unique())

g_sip = papa_sipra.groupby("anho").agg(
    s=("AreaSembrada", "sum"),
    c=("AreaCosechada", "sum"),
    p=("produccio", "sum")
)
g_sip["rto"] = g_sip["p"] / g_sip["c"]
print("\n=== BaseSIPRA Aggregation for PAPA ===")
print(g_sip)

# Now check BasePagina
df_pag = pd.read_excel(temp_file, sheet_name="BasePagina", skiprows=8)
print("\nBasePagina shape:", df_pag.shape)
col_esp = df_pag.columns[5] # cultivo
col_desag = df_pag.columns[4]
col_anho = df_pag.columns[9]
col_per = df_pag.columns[10]
col_s = df_pag.columns[11]
col_c = df_pag.columns[12]
col_p = df_pag.columns[13]

print(f"BasePagina key cols: cultivo={col_esp}, desagregacion={col_desag}, anho={col_anho}, per={col_per}")
papa_pag = df_pag[df_pag[col_esp].astype(str).str.upper().str.contains("PAPA")]
print("Total potato rows in BasePagina:", len(papa_pag))
print("Desagregaciones in BasePagina:", papa_pag[col_desag].unique())
print("Periodos in BasePagina:", papa_pag[col_per].unique())

# Group by desagregacion and anho in BasePagina
print("\n=== BasePagina by desagregacion and anho ===")
print(papa_pag.groupby([col_anho, col_desag])[[col_s, col_c, col_p]].sum())
