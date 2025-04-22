from connect_weaviate import get_weaviate_client

client = get_weaviate_client()
collection = client.collections.get("Symptom")

# Alle Objekte holen
objects = collection.query.fetch_objects(limit=999)

# Alle löschen
for obj in objects.objects:
    collection.data.delete_by_id(obj.uuid)
    print(f"🗑️  Gelöscht: {obj.properties.get('symptom_name', obj.uuid)}")

print(f"✅ Alle {len(objects.objects)} Objekte wurden gelöscht.")
client.close()
