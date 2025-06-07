# weaviate_data_import.py
import weaviate
from weaviate.auth import AuthApiKey
import json
import uuid
import os
import sys
from weaviate.util import generate_uuid5

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

# Hilfsfunktion zum Generieren einer deterministischen UUID
def generate_uuid(identifier, namespace="dogbot"):
    return generate_uuid5(f"{namespace}_{identifier}")

def main():
    # Use secure configuration module
    if not config.is_configured:
        print("Error: Configuration incomplete. Please ensure environment variables are set:")
        print("- WEAVIATE_URL")
        print("- WEAVIATE_API_KEY") 
        print("- OPENAI_APIKEY")
        return
    
    # Connect to Weaviate Cloud using secure configuration
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=config.weaviate_url,
        auth_credentials=AuthApiKey(api_key=config.weaviate_api_key),
        headers={"X-OpenAI-Api-Key": config.openai_api_key}
    )

    print(f"Weaviate bereit: {client.is_ready()}")

    # Import für Allgemein
    def import_allgemein(data_file="../data/json/dogbot_content_Allgemein.json"):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Importiere {len(data['objects'])} Allgemein-Einträge...")
        
        # Collection holen
        allgemein_collection = client.collections.get("Allgemein")
        
        # Batch-Import verwenden
        with allgemein_collection.batch.dynamic() as batch:
            for obj in data['objects']:
                properties = obj['properties']
                
                # UUID generieren basierend auf dem Thema
                uuid_str = generate_uuid(properties['thema'], "allgemein")
                
                # Objekt zum Batch hinzufügen
                try:
                    batch.add_object(
                        properties=properties,
                        uuid=uuid_str
                    )
                except Exception as e:
                    print(f"Fehler beim Erstellen des Allgemein-Objekts {properties['thema']}: {e}")
        
        # Fehlerprüfung
        if len(allgemein_collection.batch.failed_objects) > 0:
            print(f"Fehler bei {len(allgemein_collection.batch.failed_objects)} Allgemein-Objekten")
        
        print("Import Allgemein abgeschlossen.")

    # Import für Instinkte
    def import_instinkte(data_file="../data/json/dogbot_content_Instinkte.json"):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Importiere {len(data['objects'])} Instinkte-Einträge...")
        
        # Collection holen
        instinkte_collection = client.collections.get("Instinkte")
        
        # Batch-Import verwenden
        with instinkte_collection.batch.dynamic() as batch:
            for obj in data['objects']:
                properties = obj['properties']
                
                # UUID generieren basierend auf dem Instinkt
                uuid_str = generate_uuid(properties['instinkt'], "instinkte")
                
                # Objekt zum Batch hinzufügen
                try:
                    batch.add_object(
                        properties=properties,
                        uuid=uuid_str
                    )
                except Exception as e:
                    print(f"Fehler beim Erstellen des Instinkte-Objekts {properties['instinkt']}: {e}")
        
        # Fehlerprüfung
        if len(instinkte_collection.batch.failed_objects) > 0:
            print(f"Fehler bei {len(instinkte_collection.batch.failed_objects)} Instinkte-Objekten")
        
        print("Import Instinkte abgeschlossen.")

    # Import für Instinktveranlagung
    def import_instinktveranlagung(data_file="../data/json/dogbot_content_Instinktveranlagung.json"):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Importiere {len(data['objects'])} Instinktveranlagung-Einträge...")
        
        # Collection holen
        instinktveranlagung_collection = client.collections.get("Instinktveranlagung")
        
        # Batch-Import verwenden
        with instinktveranlagung_collection.batch.dynamic() as batch:
            for obj in data['objects']:
                properties = obj['properties']
                
                # numerische Werte sicherstellen
                for field in ['jagdinstinkt', 'territorialinstinkt', 'rudelinstinkt', 'sexualinstinkt']:
                    if field in properties and properties[field] is not None:
                        properties[field] = float(properties[field])
                
                # gruppen_code konvertieren
                if 'gruppen_code' in properties and properties['gruppen_code'] is not None:
                    # Bei ISO Datum-Format konvertieren
                    if isinstance(properties['gruppen_code'], str) and 'T' in properties['gruppen_code']:
                        # Extrahiere nur die numerischen Teile aus dem Datum-String
                        date_parts = properties['gruppen_code'].split('T')[0].split('-')
                        properties['gruppen_code'] = float(f"{date_parts[0][-1]}.{date_parts[1]}")
                    else:
                        properties['gruppen_code'] = float(properties['gruppen_code'])
                
                # UUID generieren basierend auf dem gruppen_code
                uuid_str = generate_uuid(str(properties['gruppen_code']), "instinktveranlagung")
                
                # Objekt zum Batch hinzufügen
                try:
                    batch.add_object(
                        properties=properties,
                        uuid=uuid_str
                    )
                except Exception as e:
                    print(f"Fehler beim Erstellen des Instinktveranlagung-Objekts {properties.get('uebergruppe', '')}: {e}")
        
        # Fehlerprüfung
        if len(instinktveranlagung_collection.batch.failed_objects) > 0:
            print(f"Fehler bei {len(instinktveranlagung_collection.batch.failed_objects)} Instinktveranlagung-Objekten")
        
        print("Import Instinktveranlagung abgeschlossen.")

    # Import für Rassen
    def import_rassen(data_file="../data/json/dogbot_content_Rassen.json"):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Importiere {len(data['objects'])} Rassen-Einträge...")
        
        # Collection holen
        rassen_collection = client.collections.get("Rassen")
        
        # Batch-Import verwenden
        with rassen_collection.batch.dynamic() as batch:
            for obj in data['objects']:
                properties = obj['properties']
                
                # gruppen_code konvertieren wenn nötig
                if 'gruppen_code' in properties and properties['gruppen_code'] is not None:
                    if isinstance(properties['gruppen_code'], str):
                        properties['gruppen_code'] = float(properties['gruppen_code'])
                
                # UUID generieren basierend auf dem Rassename
                uuid_str = generate_uuid(properties['rassename'], "rassen")
                
                # Objekt zum Batch hinzufügen
                try:
                    batch.add_object(
                        properties=properties,
                        uuid=uuid_str
                    )
                except Exception as e:
                    print(f"Fehler beim Erstellen des Rassen-Objekts {properties['rassename']}: {e}")
        
        # Fehlerprüfung
        if len(rassen_collection.batch.failed_objects) > 0:
            print(f"Fehler bei {len(rassen_collection.batch.failed_objects)} Rassen-Objekten")
        
        print("Import Rassen abgeschlossen.")
        
        # Referenzen zu Instinktveranlagung hinzufügen
        print("Füge Referenzen von Rassen zu Instinktveranlagung hinzu...")
        
        # Referenz-Batch verwenden
        with rassen_collection.batch.dynamic() as batch:
            for obj in data['objects']:
                properties = obj['properties']
                
                if 'gruppen_code' in properties and properties['gruppen_code'] is not None:
                    # UUIDs für Referenzen generieren
                    rasse_uuid = generate_uuid(properties['rassename'], "rassen")
                    
                    # Gruppen_code konvertieren wenn nötig
                    gruppen_code = properties['gruppen_code']
                    if isinstance(gruppen_code, str):
                        gruppen_code = float(gruppen_code)
                        
                    instinktveranlagung_uuid = generate_uuid(str(gruppen_code), "instinktveranlagung")
                    
                    # Referenz hinzufügen
                    try:
                        batch.add_reference(
                            from_uuid=rasse_uuid,
                            from_property="hatInstinktveranlagung",
                            to=instinktveranlagung_uuid
                        )
                    except Exception as e:
                        print(f"Fehler beim Hinzufügen der Instinktveranlagung-Referenz für {properties['rassename']}: {e}")
        
        # Fehlerprüfung
        if len(rassen_collection.batch.failed_references) > 0:
            print(f"Fehler bei {len(rassen_collection.batch.failed_references)} Rassen-Referenzen")

    # Import für Erziehung
    def import_erziehung(data_file="../data/json/dogbot_content_Erziehung.json"):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Importiere {len(data['objects'])} Erziehung-Einträge...")
        
        # Collection holen
        erziehung_collection = client.collections.get("Erziehung")
        
        # Batch-Import verwenden
        with erziehung_collection.batch.dynamic() as batch:
            for obj in data['objects']:
                properties = obj['properties']
                
                # UUID generieren basierend auf der Erziehungsaufgabe
                uuid_str = generate_uuid(properties['erziehungsaufgabe'], "erziehung")
                
                # Objekt zum Batch hinzufügen
                try:
                    batch.add_object(
                        properties=properties,
                        uuid=uuid_str
                    )
                except Exception as e:
                    print(f"Fehler beim Erstellen des Erziehung-Objekts {properties['erziehungsaufgabe']}: {e}")
        
        # Fehlerprüfung
        if len(erziehung_collection.batch.failed_objects) > 0:
            print(f"Fehler bei {len(erziehung_collection.batch.failed_objects)} Erziehung-Objekten")
        
        print("Import Erziehung abgeschlossen.")
        
        # Referenzen zu den Instinkten erstellen
        print("Füge Referenzen von Erziehung zu Instinkten hinzu...")
        
        # Referenz-Batch verwenden
        with erziehung_collection.batch.dynamic() as batch:
            for obj in data['objects']:
                properties = obj['properties']
                
                # Erziehungsaufgabe-UUID
                erziehung_uuid = generate_uuid(properties['erziehungsaufgabe'], "erziehung")
                
                # Referenzen zu den Instinkten erstellen, falls vorhanden
                if 'relevante_instinkte' in properties and properties['relevante_instinkte']:
                    instinkte = [i.strip() for i in properties['relevante_instinkte'].split(',')]
                    
                    for instinkt in instinkte:
                        instinkt_uuid = generate_uuid(instinkt, "instinkte")
                        
                        # Referenz hinzufügen
                        try:
                            batch.add_reference(
                                from_uuid=erziehung_uuid,
                                from_property="betrifftInstinkte",
                                to=instinkt_uuid
                            )
                        except Exception as e:
                            print(f"Fehler beim Hinzufügen der Instinkt-Referenz für {instinkt}: {e}")
        
        # Fehlerprüfung
        if len(erziehung_collection.batch.failed_references) > 0:
            print(f"Fehler bei {len(erziehung_collection.batch.failed_references)} Erziehung-Referenzen")

    # Import für Symptome
    def import_symptome(data_file="../data/json/dogbot_content_Symptome.json"):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Importiere {len(data['objects'])} Symptome-Einträge...")
        
        # Collection holen
        symptome_collection = client.collections.get("Symptome")
        
        # Batch-Import verwenden
        with symptome_collection.batch.dynamic() as batch:
            for obj in data['objects']:
                properties = obj['properties']
                
                # tags in Arrays umwandeln
                for field in [f for f in properties.keys() if f.startswith('tags_')]:
                    if properties[field] and isinstance(properties[field], str):
                        properties[field] = [tag.strip() for tag in properties[field].split(',')]
                
                # UUID generieren basierend auf dem Symptom-Namen
                uuid_str = generate_uuid(properties['symptom_name'], "symptome")
                
                # Objekt zum Batch hinzufügen
                try:
                    batch.add_object(
                        properties=properties,
                        uuid=uuid_str
                    )
                except Exception as e:
                    print(f"Fehler beim Erstellen des Symptome-Objekts {properties['symptom_name']}: {e}")
        
        # Fehlerprüfung
        if len(symptome_collection.batch.failed_objects) > 0:
            print(f"Fehler bei {len(symptome_collection.batch.failed_objects)} Symptome-Objekten")
        
        print("Import Symptome abgeschlossen.")
        
        # Referenzen zu den Instinkten hinzufügen
        print("Füge Referenzen von Symptomen zu Instinkten hinzu...")
        
        # Referenz-Batch verwenden
        with symptome_collection.batch.dynamic() as batch:
            for obj in data['objects']:
                properties = obj['properties']
                
                # Symptom-UUID
                symptom_uuid = generate_uuid(properties['symptom_name'], "symptome")
                
                # Überprüfen, welche Instinkt-Perspektiven vorhanden sind
                instinkte = []
                if properties.get('hundeperspektive_jagdinstinkt'):
                    instinkte.append("Jagdinstinkt")
                if properties.get('hundeperspektive_rudelinstinkt'):
                    instinkte.append("Rudelinstinkt")
                if properties.get('hundeperspektive_territorialinstinkt'):
                    instinkte.append("Territorialinstinkt")
                if properties.get('hundeperspektive_sexualinstinkt'):
                    instinkte.append("Sexualinstinkt")
                
                for instinkt in instinkte:
                    instinkt_uuid = generate_uuid(instinkt, "instinkte")
                    
                    # Referenz hinzufügen
                    try:
                        batch.add_reference(
                            from_uuid=symptom_uuid,
                            from_property="beziehtSichAufInstinkte",
                            to=instinkt_uuid
                        )
                    except Exception as e:
                        print(f"Fehler beim Hinzufügen der Instinkt-Referenz für {instinkt}: {e}")
        
        # Fehlerprüfung
        if len(symptome_collection.batch.failed_references) > 0:
            print(f"Fehler bei {len(symptome_collection.batch.failed_references)} Symptome-Referenzen")

    # Daten importieren
    try:
        import_allgemein()
        import_instinkte()
        import_instinktveranlagung()
        import_rassen()
        import_erziehung()
        import_symptome()
        
        print("Datenimport abgeschlossen!")
    except Exception as e:
        print(f"Fehler beim Importieren der Daten: {e}")
    finally:
        # Ressourcen freigeben (wichtig in v4)
        client.close()

if __name__ == "__main__":
    main()