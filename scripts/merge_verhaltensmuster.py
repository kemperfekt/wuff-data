import os
import json

# Neuer Pfad zu /data/
verzeichnis = os.path.join(os.path.dirname(__file__), "..", "data")

def lade_verhaltensmuster_aus_ordner(ordnerpfad):
    muster_dict = {}

    for dateiname in sorted(os.listdir(ordnerpfad)):
        if dateiname.endswith(".json") and not dateiname.startswith("verhaltensmuster_gesamt"):
            pfad = os.path.join(ordnerpfad, dateiname)
            with open(pfad, "r", encoding="utf-8") as f:
                try:
                    inhalt = json.load(f)

                    if isinstance(inhalt, list):
                        for eintrag in inhalt:
                            frage = eintrag.get("frage")
                            if frage:
                                muster_dict[frage] = eintrag
                    elif isinstance(inhalt, dict):
                        frage = inhalt.get("frage")
                        if frage:
                            muster_dict[frage] = inhalt

                except json.JSONDecodeError as e:
                    print(f"⚠️ Fehler in {dateiname}: {e}")

    return muster_dict

if __name__ == "__main__":
    verhaltensmuster = lade_verhaltensmuster_aus_ordner(verzeichnis)

    zielpfad = os.path.join(verzeichnis, "verhaltensmuster_gesamt.json")
    with open(zielpfad, "w", encoding="utf-8") as f:
        json.dump(verhaltensmuster, f, ensure_ascii=False, indent=2)

    print(f"{len(verhaltensmuster)} Einträge erfolgreich zusammengeführt und gespeichert unter:")
    print(zielpfad)
