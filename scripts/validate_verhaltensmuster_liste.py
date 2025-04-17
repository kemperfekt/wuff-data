import os
import json
import math
from jsonschema import validate, ValidationError

# Basis: Speicherort dieses Skripts
basis_pfad = os.path.dirname(__file__)

# Pfade: Schema liegt in scripts/, Daten im ../content/verhaltensmuster/
schema_pfad = os.path.join(basis_pfad, "verhaltensmuster_liste.schema.json")
daten_pfad = os.path.join(basis_pfad, "..", "content", "verhaltensmuster", "verhaltensmuster_gesamt.json")

# JSON-Sicherheitsfunktion: ersetze NaN durch ""
def sanitize_json(obj):
    if isinstance(obj, dict):
        return {k: sanitize_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_json(item) for item in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return ""
    else:
        return obj

# Lade Schema
with open(schema_pfad, "r", encoding="utf-8") as f:
    schema = json.load(f)

# Lade & säubere Daten
with open(daten_pfad, "r", encoding="utf-8") as f:
    daten = sanitize_json(json.load(f))

# Validierung
try:
    validate(instance=daten, schema=schema)
    print("✅ JSON-Datei ist gültig nach dem Schema.")
except ValidationError as e:
    print("❌ Fehler im JSON:")
    print(e.message)
