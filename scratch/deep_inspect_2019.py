import tempfile
from pathlib import Path
import pandas as pd

temp_file = Path(tempfile.gettempdir()) / "audit_eva_copy.xlsx"
df_pag = pd.read_excel(temp_file, sheet_name="BasePagina", skiprows=8)

papa_only = df_pag[df_pag['Cultivo'].astype(str).str.strip().str.upper() == "PAPA"]

print("\n--- 2019 Details ---")
p2019 = papa_only[papa_only['Año'] == 2019]
print("Shape of 2019:", p2019.shape)

group_keys = ['Código Dane departamento', 'Código Dane municipio', 'Desagregación cultivo', 'Periodo']
print("Unique keys in 2019:", len(p2019.drop_duplicates(subset=group_keys)))
print("Total rows in 2019:", len(p2019))

# Check by Department in 2019:
depto_sum = p2019.groupby('Departamento')[['Área sembrada (ha)', 'Área cosechada (ha)', 'Producción (t)']].sum()
print("\nDepartment totals in 2019:")
print(depto_sum.sort_values(by='Producción (t)', ascending=False).head(10))

print("\nTop 15 Municipalities by Production in 2019:")
mpio_sum = p2019.groupby(['Departamento', 'Municipio'])[['Área sembrada (ha)', 'Área cosechada (ha)', 'Producción (t)']].sum()
print(mpio_sum.sort_values(by='Producción (t)', ascending=False).head(15))

# Check Ciclo del cultivo and Subgrupo
print("\nCiclo del cultivo in 2019:", p2019['Ciclo del cultivo'].value_counts())
print("Subgrupo in 2019:", p2019['Subgrupo'].value_counts())
print("Estado fisico in 2019:", p2019['Estado físico del cultivo'].value_counts())

# What about all years?
print("\n=== Annual summary across all years in BasePagina (exact Cultivo == 'PAPA') ===")
anual_sum = papa_only.groupby('Año')[['Área sembrada (ha)', 'Área cosechada (ha)', 'Producción (t)']].sum()
anual_sum['rto'] = anual_sum['Producción (t)'] / anual_sum['Área cosechada (ha)']
print(anual_sum)
