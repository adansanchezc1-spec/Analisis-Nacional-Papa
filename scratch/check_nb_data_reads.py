import json

with open("docs/report.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = "".join(cell['source'])
        for keyword in ["read_parquet", "read_csv", "read_excel", "dataset_", "Fact_", "Dim_"]:
            if keyword in src:
                lines = [l.strip() for l in src.split("\n") if keyword in l]
                print(f"Celda {i} referencias a datos:")
                for l in lines:
                    print(f"  {l}")
