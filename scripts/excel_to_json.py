import pandas as pd
import json
import os
import datetime
import sys

# Add parent directory to path to import from archive
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        
        # DataFrame in eine Liste von Dictionaries umwandeln
        records = df.to_dict('records')
        
        # JSON-Struktur für Weaviate erstellen
        weaviate_json = {
            "class": sheet,  # Klassenname ist der Name des Tabellenblatts
            "objects": []
        }
        
        # Jede Zeile als Objekt formatieren
        for record in records:
            # Überprüfen ob die Zeile komplett leer ist
            if all(value is None for value in record.values()):
                continue
                
            # Objekt erstellen
            obj = {
                "properties": record
            }
            weaviate_json["objects"].append(obj)
        
        # JSON-Datei speichern
        base_name = os.path.splitext(os.path.basename(excel_path))[0]
        json_filename = f"{base_name}_{sheet}.json"
        json_path = os.path.join(output_folder, json_filename)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(weaviate_json, f, indent=2, ensure_ascii=False, cls=DateTimeEncoder)
        
        print(f"  -> Erstellt: {json_filename}")
        created_files.append(json_path)
    
    return created_files

if __name__ == "__main__":
    # Pfad zur Excel-Datei
    excel_path = "../data/dogbot_content.xlsx"
    output_folder = "../data/json"
    
    # JSON-Ordner erstellen falls nicht vorhanden
    os.makedirs(output_folder, exist_ok=True)
    
    # Konvertierung durchführen
    created_files = excel_to_json(excel_path, output_folder)
    
    print(f"\nKonvertierung abgeschlossen! {len(created_files)} JSON-Dateien erstellt.")