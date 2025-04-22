from connect_weaviate import get_weaviate_client
import json

client = get_weaviate_client()
col = client.collections.get("Symptom")

# Datei laden
with open("symptome_verhaltensmuster.json", "r") as f:
    symptome = json.load(f)

# Upload vorbereiten
erfolgreich = 0
for name, eintrag in symptome.items():
    obj = {
        "symptom_name": name,
        "beschreibung": eintrag.get("schnelldiagnose"),
        "tags": eintrag.get("tags_schnelldiagnose", []),
        "erste_hilfe": eintrag.get("erste_hilfe", [""])[0],
        "hypothese_zuhause": eintrag.get("hypothese_zuhause", ""),
        "instinkt_varianten": {
            "jagd": eintrag["instinkterklaerungen"]["jagdinstinkt"]["beschreibung"],
            "rudel": eintrag["instinkterklaerungen"]["rudelinstinkt"]["beschreibung"],
            "territorial": eintrag["instinkterklaerungen"]["territorialinstinkt"]["beschreibung"],
            "sexual": eintrag["instinkterklaerungen"]["sexualinstinkt"]["beschreibung"]
        }
    }

    try:
        col.data.insert(properties=obj)
        erfolgreich += 1
    except Exception as e:
        print(f"❌ Fehler bei: {name} → {e}")

print(f"✅ Upload abgeschlossen: {erfolgreich} Symptome hochgeladen.")
client.close()
