import os
import json

# Relativer Pfad zum Verzeichnis mit den einzelnen JSON-Dateien
verzeichnis = os.path.join(os.path.dirname(__file__), "..", "content", "verhaltensmuster")

def lade_verhaltensmuster_aus_ordner(ordnerpfad):
    muster_liste = []

    for dateiname in sorted(os.listdir(ordnerpfad)):
        if dateiname.endswith(".json"):
            pfad = os.path.join(ordnerpfad, dateiname)
            with open(pfad, "r", encoding="utf-8") as f:
                inhalt = json.load(f)
                muster_liste.append(inhalt)

    return muster_liste

if __name__ == "__main__":
    verhaltensmuster = lade_verhaltensmuster_aus_ordner(verzeichnis)

    # Optional: Zusammengeführte Datei speichern (z. B. im gleichen content-Verzeichnis)
    zielpfad = os.path.join(verzeichnis, "verhaltensmuster_gesamt.json")
    with open(zielpfad, "w", encoding="utf-8") as f:
        json.dump(verhaltensmuster, f, ensure_ascii=False, indent=2)

    print(f"{len(verhaltensmuster)} Einträge erfolgreich zusammengeführt und gespeichert unter:")
    print(zielpfad)
