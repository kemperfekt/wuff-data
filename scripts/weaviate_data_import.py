# Import für Symptome
def import_symptome(data_file="dogbot_content_Symptome.json"):
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
    import_allgemein("dogbot_content_Allgemein.json")
    import_instinkte("dogbot_content_Instinkte.json")
    import_instinktveranlagung("dogbot_content_Instinktveranlagung.json")
    import_rassen("dogbot_content_Rassen.json")
    import_erziehung("dogbot_content_Erziehung.json")
    import_symptome("dogbot_content_Symptome.json")
    
    print("Datenimport abgeschlossen!")
except Exception as e:
    print(f"Fehler beim Importieren der Daten: {e}")
finally:
    # Ressourcen freigeben (wichtig in v4)
    client.close()