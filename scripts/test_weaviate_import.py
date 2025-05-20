# test_weaviate_import.py
import weaviate
from weaviate.auth import AuthApiKey
import json
import os
import weaviate.classes.query as wvcq

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

    def test_counts():
        """Überprüft, ob alle Daten korrekt importiert wurden"""
        classes = ["Allgemein", "Instinkte", "Instinktveranlagung", "Rassen", "Erziehung", "Symptome"]
        
        for class_name in classes:
            try:
                collection = client.collections.get(class_name)
                # Verwendung der new Aggregation Methode
                count = collection.aggregate.over_all().with_meta_count().objects
                # In v4 wird das Zählergebnis anders zurückgegeben
                count_value = count[0].meta_count
                print(f"Anzahl der {class_name}-Objekte: {count_value}")
            except Exception as e:
                print(f"Fehler beim Zählen der {class_name}-Objekte: {e}")

    def test_references():
        """Überprüft, ob die Referenzen korrekt erstellt wurden"""
        # Test Rassen -> Instinktveranlagung
        try:
            rassen_collection = client.collections.get("Rassen")
            # Verwendung der neuen Query API
            rasse_results = rassen_collection.query.fetch_objects(
                limit=1,
                include_vector=False,
                return_properties=["rassename", "gruppen_code", "hatInstinktveranlagung { gruppe jagdinstinkt territorialinstinkt }"]
            )
            
            print("\nTest Rassen -> Instinktveranlagung:")
            if rasse_results.objects:
                print(json.dumps(rasse_results.objects[0].properties, indent=2))
            else:
                print("Keine Rassen gefunden")
        except Exception as e:
            print(f"Fehler beim Testen der Rassen-Referenzen: {e}")
        
        # Test Erziehung -> Instinkte
        try:
            erziehung_collection = client.collections.get("Erziehung")
            erziehung_results = erziehung_collection.query.fetch_objects(
                limit=1,
                include_vector=False,
                return_properties=["erziehungsaufgabe", "relevante_instinkte", "betrifftInstinkte { instinkt }"]
            )
            
            print("\nTest Erziehung -> Instinkte:")
            if erziehung_results.objects:
                print(json.dumps(erziehung_results.objects[0].properties, indent=2))
            else:
                print("Keine Erziehungsaufgaben gefunden")
        except Exception as e:
            print(f"Fehler beim Testen der Erziehung-Referenzen: {e}")
        
        # Test Symptome -> Instinkte
        try:
            symptome_collection = client.collections.get("Symptome")
            symptome_results = symptome_collection.query.fetch_objects(
                limit=1,
                include_vector=False,
                return_properties=["symptom_name", "beziehtSichAufInstinkte { instinkt }"]
            )
            
            print("\nTest Symptome -> Instinkte:")
            if symptome_results.objects:
                print(json.dumps(symptome_results.objects[0].properties, indent=2))
            else:
                print("Keine Symptome gefunden")
        except Exception as e:
            print(f"Fehler beim Testen der Symptome-Referenzen: {e}")

    def test_semantic_search():
        """Testet die semantische Suche für die Hundeperspektive"""
        try:
            symptome_collection = client.collections.get("Symptome")
            # Verwendung der neuen NearText-Methode
            results = symptome_collection.query.near_text(
                query="Hund bellt fremde Menschen an",
                limit=2,
                return_properties=["symptom_name", "hundeperspektive_jagdinstinkt", "hundeperspektive_rudelinstinkt"],
                return_metadata=wvcq.MetadataQuery(distance=True)
            )
            
            print("\nSemantische Suche 'Hund bellt fremde Menschen an':")
            if results.objects:
                for obj in results.objects:
                    print(f"Symptom: {obj.properties.get('symptom_name')}")
                    print(f"Distanz: {obj.metadata.distance}")
                    print(json.dumps(obj.properties, indent=2))
            else:
                print("Keine Ergebnisse gefunden")
        except Exception as e:
            print(f"Fehler bei der semantischen Suche: {e}")

    # Tests ausführen
    try:
        test_counts()
        test_references()
        test_semantic_search()
    except Exception as e:
        print(f"Fehler beim Ausführen der Tests: {e}")
    finally:
        # Ressourcen freigeben (wichtig in v4)
        client.close()

if __name__ == "__main__":
    main()