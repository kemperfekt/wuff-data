import pandas as pd
import json
from pathlib import Path

excel_path = "../data/dogbot_content.xlsx"
schema_dir = Path("schema")
schema_dir.mkdir(exist_ok=True)

special_references = {
    "relevante_instinkte": "Instinkt"
}
special_as_number = {
    "gruppen_code",
    "jagdinstinkt",
    "territorialinstinkt",
    "rudelinstinkt",
    "sexualinstinkt"
}

def infer_type(column, values):
    if column in special_as_number:
        return "number"
    if column in special_references:
        return [special_references[column]]
    if all(isinstance(v, (int, float)) or pd.isna(v) for v in values):
        return "number"
    if values.str.contains(",").any():
        return ["text"]
    return "text"

df_all = pd.read_excel(excel_path, sheet_name=None)

for sheet_name, df in df_all.items():
    props = []
    for col in df.columns:
        sample_values = df[col].dropna().astype(str).head(10)
        dtype = infer_type(col, sample_values)
        props.append({
            "name": col,
            "dataType": dtype if isinstance(dtype, list) else [dtype]
        })

    class_def = {
        "class": sheet_name,
        "description": f"Automatisch erzeugt aus Sheet {sheet_name}",
        "vectorizer": "text2vec-openai",
        "moduleConfig": {
            "text2vec-openai": {
                "model": "text-embedding-3-small",
                "type": "text"
            }
        },
        "properties": props
    }

    with open(schema_dir / f"{sheet_name.lower()}.json", "w", encoding="utf-8") as f:
        json.dump(class_def, f, indent=2, ensure_ascii=False)
    print(f"✅ Schema geschrieben: {sheet_name.lower()}.json")