import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import json
from connect_weaviate import get_weaviate_client

# Weaviate-Verbindung aufbauen
client = get_weaviate_client()
collection = client.collections.get("Instinktveranlagung")

# JSON-Datei laden
with open("../../data/instinktveranlagung/instinktveranlagung.json", "r", encoding="utf-8") as f:
    daten = json.load(f)

# Objekte hochladen
for gruppen_code, eintrag in daten.items():
    collection.data.insert({
        "gruppen_code": gruppen_code,
        "gruppe": eintrag["gruppe"],
        "untergruppe": eintrag["untergruppe"],
        "funktion": eintrag["funktion"],
        "merkmale": eintrag["merkmale"],
        "anforderungen": eintrag["anforderungen"],
        "instinkte": eintrag["instinkte"]
    })

print(f"{len(daten)} Einträge wurden erfolgreich hochgeladen.")
client.close()
