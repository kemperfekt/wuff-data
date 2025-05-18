import json
from pathlib import Path
from connect_weaviate import get_weaviate_client
from generate_schema_from_excel import special_references

data_dir = Path("data")
schema_dir = Path("schema")

client = get_weaviate_client()

def validate_and_import():
    for schema_file in schema_dir.glob("*.json"):
        class_name = schema_file.stem.capitalize()
        print(f"\n📦 Verarbeite Klasse: {class_name}")

        with open(schema_file, "r", encoding="utf-8") as f:
            schema = json.load(f)

        if not client.schema.exists(class_name):
            print(f"➕ Erstelle Klasse: {class_name}")
            client.schema.create_class(schema)
        else:
            print(f"⏩ Klasse {class_name} existiert bereits")

        data_file = data_dir / f"{schema_file.stem}_data.json"
        if not data_file.exists():
            print(f"⚠️  Keine Daten gefunden für {class_name}")
            continue

        with open(data_file, "r", encoding="utf-8") as f:
            objects = json.load(f)

        for obj in objects:
            for key, val in obj.items():
                if isinstance(val, list) and key in special_references:
                    obj[key] = [{"beacon": f"weaviate://localhost/{special_references[key]}/{v}"} for v in val]
            client.data_object.create(data_object=obj, class_name=class_name)
        print(f"✅ {len(objects)} Objekte in {class_name} importiert")

if __name__ == "__main__":
    validate_and_import()