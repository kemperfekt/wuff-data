from connect_weaviate import get_weaviate_client

# Verbindung zu Weaviate aufbauen
client = get_weaviate_client()

# Semantische Suche mit near_text
response = client.collections.get("Hunderasse").query.near_text(
    query="Rassen mit starkem Jagdtrieb",
    limit=5
)

# Ergebnisse ausgeben
print("\n🐕 Semantische Weaviate-Ergebnisse für: Rassen mit starkem Jagdtrieb")
for obj in response.objects:
    props = obj.properties
    print(f"\n➡️ Gruppe: {props.get('gruppe', '[unbekannt]')} / {props.get('untergruppe', '[unbekannt]')}")
    #print(f"🔍 Merkmale: {props.get('merkmale', '[keine Angabe]')}")
    print(f"📊 Jagdinstinkt: {props.get('jagdinstinkt', '[keine Angabe]')}")

client.close()
