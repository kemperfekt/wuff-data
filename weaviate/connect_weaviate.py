import os
import weaviate
from dotenv import load_dotenv

# Optional, wenn du .env-Dateien verwendest:
load_dotenv()

# Hole API-Key aus Umgebungsvariable (z. B. in ~/.zshrc gesetzt)
api_key = os.getenv("WEAVIATE_API_KEY")

if not api_key:
    raise EnvironmentError("WEAVIATE_API_KEY nicht gesetzt. Bitte in ~/.zshrc oder .env angeben.")

# Endpoint deiner Weaviate-Instanz
weaviate_url = "https://cpmlrjetsgqskhwx9eqgg.c0.europe-west3.gcp.weaviate.cloud"

# Initialisiere Weaviate-Client
client = weaviate.Client(
    url=weaviate_url,
    auth_client_secret=weaviate.AuthApiKey(api_key),
    additional_headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY", "")  # Falls RAG-Generierung genutzt wird
    }
)

# Verbindung testen
if client.is_ready():
    print("✅ Erfolgreich mit Weaviate verbunden!")
    print("Vorhandene Klassen:")
    print(client.schema.get())
else:
    print("❌ Verbindung zu Weaviate fehlgeschlagen")
