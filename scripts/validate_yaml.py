"""
Validiert YAML-Dateien im content-Verzeichnis anhand eines einfachen Schemas.
"""

import os
import yaml

def validate_yaml_file(filepath):
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
    required_keys = ["id", "frage", "antwort", "tags"]
    for key in required_keys:
        if key not in data:
            raise ValueError(f"Fehlender Schlüssel: {key} in Datei {filepath}")

if __name__ == "__main__":
    base_path = "content"
    for root, _, files in os.walk(base_path):
        for name in files:
            if name.endswith(".yaml"):
                validate_yaml_file(os.path.join(root, name))
    print("✅ Alle YAML-Dateien validiert.")
