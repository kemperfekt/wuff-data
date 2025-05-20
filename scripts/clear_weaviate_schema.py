# clear_weaviate_schema.py
import weaviate
from weaviate.auth import AuthApiKey
import os

def main():
    # Bestehende Weaviate-Zugangsdaten verwenden
    weaviate_url = os.environ["WEAVIATE_URL"]
    weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
    openai_api_key = os.environ.get("OPENAI_APIKEY")

    # Connect to Weaviate Cloud - verwende die neue Connect-Methode
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=AuthApiKey(api_key=weaviate_api_key),
        headers={"X-OpenAI-Api-Key": openai_api_key} if openai_api_key else {}
    )

    print(f"Weaviate bereit: {client.is_ready()}")

    try:
        # Alle Sammlungen auflisten
        collections = client.collections.list_all()
        print(f"Vorhandene Collections: {[collection.name for collection in collections]}")
        
        # Löschen in umgekehrter Reihenfolge wegen Abhängigkeiten
        collections_to_delete = ["Symptome", "Erziehung", "Rassen", "Instinktveranlagung", "Instinkte", "Allgemein"]
        
        for collection_name in collections_to_delete:
            try:
                print(f"Lösche Collection {collection_name}...")
                client.collections.delete(collection_name)
                print(f"Collection {collection_name} gelöscht")
            except Exception as e:
                print(f"Fehler beim Löschen der Collection {collection_name}: {e}")
        
        print("Alle Collections gelöscht!")
    except Exception as e:
        print(f"Fehler beim Löschen des Schemas: {e}")
    finally:
        # Ressourcen freigeben
        client.close()

if __name__ == "__main__":
    main()