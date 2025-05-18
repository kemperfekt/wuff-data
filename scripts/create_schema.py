import json
import os
from pathlib import Path
from connect_weaviate import get_weaviate_client

def create_schema():
    client = get_weaviate_client()
    schema_dir = Path(__file__).parent.parent / "schema"
    for schema_file in schema_dir.glob("*.json"):
        with open(schema_file, "r", encoding="utf-8") as f:
            class_def = json.load(f)
            class_name = class_def.get("class")
            if class_name and not client.schema.exists(class_name):
                print(f"Creating class: {class_name}")
                client.schema.create_class(class_def)
            else:
                print(f"Class {class_name} already exists or invalid.")

if __name__ == "__main__":
    create_schema()