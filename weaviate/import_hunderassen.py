import pandas as pd
from connect_weaviate import get_weaviate_client

# Excel-Datei einlesen
df = pd.read_excel("rassen.xlsx")

# Verbindung zu Weaviate aufbauen
client = get_weaviate_client()
collection = client.collections.get("Hunderasse")

# Datensätze einfügen
for _, row in df.iterrows():
    daten = {
        "gruppe": row["Übergruppe"],
        "untergruppe": row["Gruppe"],
        "funktion": row["Funktion"],
        "merkmale": row["Merkmale"],
        "erziehungsanforderung": row["Anforderungen"],
        "jagdinstinkt": row["Jagdinstinkt"],
        "rudelinstinkt": row["Sozialer Rudelinstinkt"],
        "territorialinstinkt": row["Territorialinstinkt"],
        "sexualinstinkt": row["Sexualinstinkt"],
        "instinktkommentar": ""  # row.get("Instinktkommentar", "")
    }

    try:
        collection.data.insert(properties=daten)
        print(f"✅ Hochgeladen: {row.get('Rasse', '[unbekannt]')}")
    except Exception as e:
        print(f"❌ Fehler bei Rasse '{row.get('Rasse', '[unbekannt]')}': {e}")

client.close()
