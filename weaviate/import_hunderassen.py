import pandas as pd
from connect_weaviate import get_weaviate_client

# Verbindung zu Weaviate
client = get_weaviate_client()
col_rassen = client.collections.get("Hunderassen")
col_instinkte = client.collections.get("Instinktveranlagung")

# Excel-Datei laden
df = pd.read_excel("Rasseliste_import.xlsx", sheet_name="Rassen", dtype={"gruppen_code": str})

erfolg = 0
fehler = []

for _, row in df.iterrows():
    gruppen_code = row["gruppen_code"]

    # passenden Instinktveranlagungseintrag holen
    instinkt = col_instinkte.query.fetch_objects(
        filters={"path": ["gruppen_code"], "operator": "Equal", "valueText": gruppen_code},
        return_properties=["gruppen_code"]
    )
    if not instinkt.objects:
        fehler.append((row["rassename"], gruppen_code))
        continue

    instinkt_uuid = instinkt.objects[0].uuid

    # Objekt einfügen
    col_rassen.data.insert({
        "rassename": row["rassename"],
        "alternative_namen": row["alternative_namen"],
        "ursprungsland": row["ursprungsland"],
        "gruppen_code": gruppen_code,
        "verweis_instinktveranlagung": {
            "beacon": f"weaviate://localhost/Instinktveranlagung/{instinkt_uuid}"
        }
    })
    erfolg += 1

client.close()

print(f"✅ Upload abgeschlossen: {erfolg} erfolgreich, {len(fehler)} fehlgeschlagen.")
if fehler:
    print("Fehlgeschlagene Zuordnungen:")
    for name, code in fehler:
        print(f"  - {name} (gruppen_code: {code})")
