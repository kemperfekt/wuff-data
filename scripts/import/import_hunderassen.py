import pandas as pd
from connect_weaviate import get_weaviate_client
from weaviate.classes.query import Filter

# Schritt 1: Verbindung aufbauen
client = get_weaviate_client()
col_rassen = client.collections.get("Hunderassen")
col_instinkte = client.collections.get("Instinktveranlagung")

# Schritt 2: Excel-Datei laden
df = pd.read_excel("Rasseliste_import.xlsx", sheet_name="Rassen", dtype={"gruppen_code": str})

# Schritt 3–5: Filter anwenden, Daten hochladen
erfolg = 0
fehler = []

for _, row in df.iterrows():
    gruppen_code = row["gruppen_code"]
    rassename = row["rassename"]

    # Schritt 3: passenden Instinktveranlagungseintrag holen
    filter_expr = Filter.by_property("gruppen_code").equal(gruppen_code)
    instinkt_result = col_instinkte.query.fetch_objects(
        filters=filter_expr,
        return_properties=["gruppen_code"]
    )

    if not instinkt_result.objects:
        fehler.append((rassename, gruppen_code))
        continue

    instinkt_uuid = instinkt_result.objects[0].uuid

    # Schritt 4: Objekt mit separaten references einfügen
    col_rassen.data.insert(
        properties={
            "rassename": row["rassename"],
            "alternative_namen": row["alternative_namen"],
            "ursprungsland": row["ursprungsland"],
            "gruppen_code": gruppen_code
        },
        references={
            "verweis_instinktveranlagung": [f"Instinktveranlagung/{instinkt_uuid}"]
        }
    )

    erfolg += 1

# Schritt 6: Verbindung schließen & Ergebnis melden
client.close()

print(f"✅ Upload abgeschlossen: {erfolg} erfolgreich, {len(fehler)} fehlgeschlagen.")
if fehler:
    print("⚠️ Fehlgeschlagene Zuordnungen:")
    for name, code in fehler:
        print(f"  - {name} (gruppen_code: {code})")
