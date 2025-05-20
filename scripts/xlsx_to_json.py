import pandas as pd
import json
import os
import datetime

# Benutzerdefinierten JSON-Encoder erstellen, der datetime-Objekte behandeln kann
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            # ISO-Format für Datum und Zeit verwenden
            return obj.isoformat()
        return super().default(obj)

def excel_to_json(excel_path, output_folder=None):
    """
    Konvertiert eine Excel-Datei mit mehreren Tabellenblättern in separate JSON-Dateien.
    Das JSON-Format ist an Weaviate angepasst.
    
    Args:
        excel_path: Pfad zur Excel-Datei
        output_folder: Ordner für die Ausgabe der JSON-Dateien (optional)
    
    Returns:
        Eine Liste der erstellten JSON-Dateien
    """
    # Ausgabeordner bestimmen
    if output_folder is None:
        # Im gleichen Ordner wie die Excel-Datei speichern
        output_folder = os.path.dirname(excel_path)
    
    # Excel-Datei einlesen
    print(f"Lese Excel-Datei: {excel_path}")
    excel = pd.ExcelFile(excel_path)
    
    # Liste der Tabellenblätter ausgeben
    sheet_names = excel.sheet_names
    print(f"Gefundene Tabellenblätter: {sheet_names}")
    
    created_files = []
    
    # Jedes Tabellenblatt in eine JSON-Datei umwandeln
    for sheet in sheet_names:
        # Tabellenblatt einlesen
        df = pd.read_excel(excel, sheet_name=sheet)
        
        # Anzahl der Zeilen und Spalten ausgeben
        print(f"Tabellenblatt '{sheet}': {df.shape[0]} Zeilen, {df.shape[1]} Spalten")
        
        # Leere Werte durch None ersetzen (für JSON-kompatibilität)
        df = df.where(pd.notnull(df), None)
        
        # Umwandeln von datetime-Objekten in Strings
        for column in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                df[column] = df[column].dt.strftime('%Y-%m-%dT%H:%M:%S')
        
        # DataFrame in Liste von Dictionaries umwandeln
        records = df.to_dict(orient='records')
        
        # Weaviate-freundliches Format erstellen
        weaviate_format = {
            "class": sheet,  # Tabellenblatt-Name als Klassenname
            "objects": []
        }
        
        for record in records:
            obj = {
                "properties": record
            }
            weaviate_format["objects"].append(obj)
        
        # JSON-Dateipfad erstellen
        base_name = os.path.splitext(os.path.basename(excel_path))[0]
        json_path = os.path.join(output_folder, f"{base_name}_{sheet}.json")
        
        # Als JSON speichern mit dem benutzerdefinierten Encoder
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(weaviate_format, f, ensure_ascii=False, indent=2, cls=DateTimeEncoder)
        
        print(f"JSON-Datei erstellt: {json_path}")
        
        created_files.append(json_path)
    
    return created_files

# Beispielaufruf
if __name__ == "__main__":
    # Passen Sie den Pfad zur Excel-Datei an
    excel_file = "../data/dogbot_content.xlsx"
    
    # Optional: Ausgabeordner angeben
    output_dir = "../data/json"
    
    # Sicherstellen, dass der Ausgabeordner existiert
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Excel in JSON umwandeln
    json_files = excel_to_json(excel_file, output_dir)
    
    print("\nUmwandlung abgeschlossen.")
    print(f"Erstellte JSON-Dateien ({len(json_files)}):")
    for file in json_files:
        print(f"- {file}")