#!/usr/bin/env python3
"""
Import new symptom to Weaviate
"""
import weaviate
from weaviate.auth import AuthApiKey
import json
import os
from weaviate.util import generate_uuid5

def generate_uuid(identifier, namespace="dogbot"):
    return generate_uuid5(f"{namespace}_{identifier}")

def main():
    # Umgebungsvariablen laden
    from dotenv import load_dotenv
    load_dotenv()
    
    # Weaviate-Zugangsdaten
    weaviate_url = os.environ["WEAVIATE_URL"]
    weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
    openai_api_key = os.environ.get("OPENAI_APIKEY")

    # Connect to Weaviate Cloud
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=AuthApiKey(api_key=weaviate_api_key),
        headers={"X-OpenAI-Api-Key": openai_api_key} if openai_api_key else {}
    )

    print(f"Weaviate bereit: {client.is_ready()}")

    # Load the new symptoms data
    with open("data/json/dogbot_content_Symptome.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Find the new symptom (row 21 - "Der Hund winselt mich die ganze Zeit an")
    new_symptom = None
    for obj in data['objects']:
        if obj['properties']['symptom_name'] == "Der Hund winselt mich die ganze Zeit an":
            new_symptom = obj
            break
    
    if not new_symptom:
        print("Neues Symptom nicht gefunden!")
        return
    
    print(f"Gefundenes neues Symptom: {new_symptom['properties']['symptom_name']}")
    
    # Get the Symptome collection
    symptome_collection = client.collections.get("Symptome")
    
    # Generate UUID for the new symptom
    uuid_str = generate_uuid(new_symptom['properties']['symptom_name'], "symptome")
    
    # Process properties to convert tag strings to arrays
    properties = new_symptom['properties'].copy()
    tag_fields = [
        'tags_schnelldiagnose',
        'tags_hundeperspektive_jagdinstinkt',
        'tags_hundeperspektive_rudelinstinkt',
        'tags_hundeperspektive_territorialinstinkt',
        'tags_hundeperspektive_sexualinstinkt',
        'tags_erste_hilfe'
    ]
    
    for field in tag_fields:
        if field in properties:
            if isinstance(properties[field], str):
                # Convert comma-separated string to array
                properties[field] = [tag.strip() for tag in properties[field].split(',') if tag.strip()]
            elif properties[field] is None:
                # Convert None to empty array
                properties[field] = []
    
    # Add the new symptom
    try:
        symptome_collection.data.insert(
            properties=properties,
            uuid=uuid_str
        )
        print(f"✓ Erfolgreich hinzugefügt: {new_symptom['properties']['symptom_name']}")
        
        # Verify it was added
        result = symptome_collection.query.fetch_object_by_id(uuid_str)
        if result:
            print(f"✓ Verifiziert: Symptom wurde erfolgreich zu Weaviate hinzugefügt")
            print(f"  - UUID: {uuid_str}")
            print(f"  - Schnelldiagnose: {result.properties['schnelldiagnose'][:100]}...")
        
    except Exception as e:
        print(f"Fehler beim Hinzufügen des Symptoms: {e}")
    
    finally:
        client.close()

if __name__ == "__main__":
    main()