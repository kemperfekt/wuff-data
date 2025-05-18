

import pandas as pd
import json
from pathlib import Path

excel_path = "Inhalte (3).xlsx"
output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

list_fields = {
    "relevante_instinkte",
    "tags_erste_hilfe",
    "tags_schnelldiagnose",
    "tags_hundeperspektive_jagdinstinkt",
    "tags_hundeperspektive_rudelinstinkt",
    "tags_hundeperspektive_territorialinstinkt",
    "tags_hundeperspektive_sexualinstinkt"
}

def convert_cell(value, column):
    if pd.isna(value):
        return None
    if column in list_fields:
        return [v.strip() for v in str(value).split(",")]
    return value

df_all = pd.read_excel(excel_path, sheet_name=None)

for sheet_name, df in df_all.items():
    records = []
    for _, row in df.iterrows():
        obj = {
            col: convert_cell(row[col], col)
            for col in df.columns
            if not pd.isna(row[col])
        }
        records.append(obj)
    output_file = output_dir / f"{sheet_name.lower()}_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"✅ Daten geschrieben: {output_file}")