import pandas as pd
import os

def excel_to_csv(excel_path, output_folder=None):
    """
    Konvertiert eine Excel-Datei mit mehreren Tabellenblättern in separate CSV-Dateien.
    
    Args:
        excel_path: Pfad zur Excel-Datei
        output_folder: Ordner für die Ausgabe der CSV-Dateien (optional)
    
    Returns:
        Eine Liste der erstellten CSV-Dateien
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
    
    # Jedes Tabellenblatt in eine CSV-Datei umwandeln
    for sheet in sheet_names:
        # Tabellenblatt einlesen
        df = pd.read_excel(excel, sheet_name=sheet)
        
        # Anzahl der Zeilen und Spalten ausgeben
        print(f"Tabellenblatt '{sheet}': {df.shape[0]} Zeilen, {df.shape[1]} Spalten")
        
        # CSV-Dateipfad erstellen
        base_name = os.path.splitext(os.path.basename(excel_path))[0]
        csv_path = os.path.join(output_folder, f"{base_name}_{sheet}.csv")
        
        # Als CSV speichern
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"CSV-Datei erstellt: {csv_path}")
        
        created_files.append(csv_path)
    
    return created_files

# Beispielaufruf
if __name__ == "__main__":
    # Passen Sie den Pfad zur Excel-Datei an
    excel_file = "../data/dogbot_content.xlsx"
    
    # Optional: Ausgabeordner angeben (wenn nicht angegeben, wird der Ordner der Excel-Datei verwendet)
    output_dir = "../data/csv"
    
    # Sicherstellen, dass der Ausgabeordner existiert
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Excel in CSV umwandeln
    csv_files = excel_to_csv(excel_file, output_dir)
    
    print("\nUmwandlung abgeschlossen.")
    print(f"Erstellte CSV-Dateien ({len(csv_files)}):")
    for file in csv_files:
        print(f"- {file}")