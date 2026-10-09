import tempfile
from pathlib import Path
import pandas as pd

temp_file = Path(tempfile.gettempdir()) / "audit_eva_copy.xlsx"
df_pag = pd.read_excel(temp_file, sheet_name="BasePagina", skiprows=8)

col_esp = df_pag.columns[5] # Cultivo
col_desag = df_pag.columns[4]
col_anho = df_pag.columns[9]
col_per = df_pag.columns[10]
col_s = df_pag.columns[11]
col_c = df_pag.columns[12]
col_p = df_pag.columns[13]

# Filter potato
# Notice in previous output:
# Especies matched: 'Papa todas las variedades', 'Papa criolla', 'Papaya...', 'Malanga...'
# Because str.contains('PAPA') also matches PAPAYA and PAPA CHINA!
# But what is df_pag[col_esp] exactly?
print("Unique Cultivo values matching PAPA:")
print(df_pag[df_pag[col_esp].astype(str).str.upper().str.contains("PAPA")][col_esp].value_counts())

papa_only = df_pag[df_pag[col_esp].astype(str).str.strip().str.upper() == "PAPA"]
print(f"\nExact Cultivo == 'PAPA' rows: {len(papa_only)}")
print("Desagregaciones of exact PAPA:")
print(papa_only[col_desag].value_counts())

print("\nPeriodos of exact PAPA:")
print(papa_only[col_per].value_counts())

# Group by año and Periodo
print("\nSum of area sembrada by Año and Periodo:")
print(papa_only.groupby([col_anho, col_per])[[col_s, col_c, col_p]].sum())

# Check if there are duplicate municipalities in 2019A, 2019B vs 2019!
print("\nMunicipality breakdown in 2019:")
p2019 = papa_only[papa_only[col_anho] == 2019]
print("Periods in 2019:", p2019[col_per].value_counts())
print("Number of municipalities in 2019A:", p2019[p2019[col_per] == '2019A']['Cod. Mun.'].nunique())
print("Number of municipalities in 2019B:", p2019[p2019[col_per] == '2019B']['Cod. Mun.'].nunique())
if (p2019[col_per] == '2019').any():
    print("Number of municipalities in 2019 (annual):", p2019[p2019[col_per] == '2019']['Cod. Mun.'].nunique())

# Check how departments distribute in 2019
print("\nDepartment totals in 2019:")
print(p2019.groupby(['Departamento', col_desag])[[col_s, col_c, col_p]].sum())
