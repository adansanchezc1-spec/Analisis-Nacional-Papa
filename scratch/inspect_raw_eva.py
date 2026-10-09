import os
import shutil
import tempfile
from pathlib import Path
import subprocess
import pandas as pd

raw_dir = Path("data/RAW/eva")
eva_files = list(raw_dir.glob("*.xlsx"))
print("Files in data/RAW/eva:", eva_files)
eva_file = eva_files[0]

temp_file = Path(tempfile.gettempdir()) / "audit_eva_copy.xlsx"
cmd = f'powershell -NoProfile -Command "Copy-Item -Path \'{eva_file}\' -Destination \'{temp_file}\' -Force"'
subprocess.run(cmd, shell=True)

xl = pd.ExcelFile(temp_file)
print("Sheet names:", xl.sheet_names)

# Inspect the first few rows of each sheet
for sname in xl.sheet_names:
    df_head = pd.read_excel(temp_file, sheet_name=sname, nrows=15)
    print(f"\n--- Sheet: {sname} (shape preview: {df_head.shape}) ---")
    print(df_head.iloc[:5, :8])
