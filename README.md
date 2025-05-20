# DogBot Weaviate Integration

Dieses Projekt integriert die DogBot-Daten in eine Weaviate-Datenbank für Retrieval Augmented Generation (RAG).

## Schema

Das Weaviate-Schema besteht aus folgenden Klassen:
- **Allgemein**: Grundlegende Informationen über Hunde
- **Instinkte**: Die vier grundlegenden Hundeinstinkte
- **Instinktveranlagung**: Verteilung der Instinkte nach Hundegruppen
- **Rassen**: Hunderassen mit Verweisen auf Instinktveranlagungen
- **Erziehung**: Erziehungsaufgaben mit Bezug zu Instinkten
- **Symptome**: Problematische Verhaltensweisen mit Instinktbezug und Lösungsvorschlägen

## Beziehungen im Schema

- **Rassen → Instinktveranlagung**: über `gruppen_code` und `hatInstinktveranlagung`
- **Erziehung → Instinkte**: über `relevante_instinkte` und `betrifftInstinkte`
- **Symptome → Instinkte**: über `hundeperspektive_*` und `beziehtSichAufInstinkte`
- **Symptome → Erziehung**: über `empfohleneErziehungsaufgaben`

## Datenimport

Die Daten werden aus JSON-Dateien importiert:
- dogbot_content_Allgemein.json
- dogbot_content_Instinkte.json
- dogbot_content_Instinktveranlagung.json
- dogbot_content_Rassen.json
- dogbot_content_Erziehung.json
- dogbot_content_Symptome.json

## Automatisierung

Der Import-Prozess ist in `weaviate_data_import.py` automatisiert. Führen Sie das Skript aus, nachdem Sie das Schema mit `weaviate_schema_setup.py` erstellt haben.

## Indexierung für Hundeperspektive

Besondere Aufmerksamkeit wurde auf die Indexierung der "Hundeperspektive"-Felder gelegt, die eine zentrale Rolle für den DogBot spielen. Diese Felder werden für semantische Suche vektorisiert.

## Erweiterungen

Geplante Erweiterungen:
- Hundeprofile mit Verweisen auf Rassen
- Automatisierte Schema-Extraktion aus Daten
- Gewichtete Instinktanalyse für Symptome

## Dog Agent Integration

Der Dog Agent nutzt dieses Schema, um:
1. Nutzeranfragen zu verstehen
2. Passende Symptome zu finden
3. Den dominanten Instinkt zu identifizieren
4. Antworten aus der Hundeperspektive zu generieren
5. Passende Erziehungsaufgaben vorzuschlagen


## 🔄 Related Repositories
🤖 GPT-powered backend for diagnosis: https://github.com/kemperfekt/dogbot-agent
🖥️ Visual frontend for human–dog interaction: https://github.com/kemperfekt/dogbot-ui
🐶 Project meta-repo with vision and coordination: https://github.com/kemperfekt/dogbot
