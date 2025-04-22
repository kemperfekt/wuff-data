from connect_weaviate import get_weaviate_client

# Verbindung aufbauen
client = get_weaviate_client()

# Hunderasse-Collection abrufen
hunderassen = client.collections.get("Hunderasse").query.fetch_objects(
    include_vector=False,
    limit=200
)

# Mapping: (gruppe, untergruppe) → UUID
gruppe_untergruppe_to_uuid = {}

for obj in hunderassen.objects:
    props = obj.properties
    gruppe = props.get("gruppe")
    untergruppe = props.get("untergruppe")
    if gruppe and untergruppe:
        gruppe_untergruppe_to_uuid[(gruppe.strip(), untergruppe.strip())] = obj.uuid

# Ausgabe zur Kontrolle
print(f"{len(gruppe_untergruppe_to_uuid)} Einträge im Mapping erstellt.")
for k, v in list(gruppe_untergruppe_to_uuid.items())[:5]:
    print(f"{k} → {v}")

client.close()
