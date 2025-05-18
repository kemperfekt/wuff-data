import json
import os
from pathlib import Path
from connect_weaviate import get_weaviate_client

def import_data():
    client = get_weaviate_client()
    data_dir = Path(__file__).parent.parent / "data"
    for data_file in data_dir.glob("*.json"):
        class_name = data_file.stem.replace("_data", "").capitalize()
        with open(data_file, "r", encoding="utf-8") as f:
            objects = json.load(f)
        print(f"Importing {len(objects)} objects into {class_name}...")
        for obj in objects:
            client.data_object.create(data_object=obj, class_name=class_name)

if __name__ == "__main__":
    import_data()
