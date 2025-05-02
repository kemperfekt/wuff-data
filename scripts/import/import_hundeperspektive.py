# scripts/import/import_hundeperspektive.py

import os
import sys
import json
import weaviate
from pathlib import Path
from weaviate.classes.init import Auth
from weaviate.classes.config import Property, DataType

# Optional: für Debug-Zwecke
from weaviate.classes.query import MetadataQuery

# 🔁 Pfad zu dogbot-agent/src hinzufügen (für get_weaviate_client, falls benötigt)
AGENT_PATH = Path(__file__).resolve().parent.parent.parent.parent / "dogbot-agent" / "src"
sys.path.append(str(AGENT_PATH))

# 📍 Pfade und Collection-Namen
BASE_DIR = Path(__file__).resolve().parent.parent.parent
JSON_PATH = BASE_DIR / "data" / "hundeperspektive" / "hundeperspektive_chunks.json"
COLLECTION_NAME = "Hundeperspektive"

def create_collection(client: weaviate.WeaviateClient):
    """Legt die Collection an, falls sie noch nicht existiert."""
    if COLLECTION_NAME in client.collections.list_all():
        print(f"✅ Collection '{COLLECTION_NAME}' existiert bereits.")
        return

    client.collections.create(
        COLLECTION_NAME,
        properties=[
            Property(name="thema", data_type=DataType.TEXT),
            Property(name="beschreibung", data_type=DataType.TEXT),
            Property(name="emotion", data_type=DataType.TEXT),
            Property(name="instinkte", data_type=DataType.TEXT_ARRAY),
        ]
    )
    print(f"✅ Collection '{COLLECTION_NAME}' wurde erstellt.")

def upload_chunks(client: weaviate.WeaviateClient):
    """Lädt die JSON-Datei in die Collection."""
    collection = client.collections.get(COLLECTION_NAME)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    for chunk in chunks:
        collection.data.insert(chunk)

    print(f"✅ {len(chunks)} Einträge wurden in '{COLLECTION_NAME}' hochgeladen.")

if __name__ == "__main__":
    # 🔐 Verbindung zu Weaviate herstellen
    weaviate_url = os.environ["WEAVIATE_URL"]
    weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
    openai_key = os.getenv("OPENAIAPIKEY", "")  # optional

    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
        headers={"X-OpenAI-Api-Key": openai_key}
    )

    if not client.is_ready():
        raise RuntimeError("❌ Verbindung zu Weaviate fehlgeschlagen.")
    print("🔗 Verbindung zu Weaviate steht.")

    create_collection(client)
    upload_chunks(client)

    client.close()
    print("👋 Verbindung geschlossen.")
