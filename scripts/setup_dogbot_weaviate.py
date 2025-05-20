# setup_dogbot_weaviate.py
import os
import argparse
import subprocess
import sys

def check_env_vars():
    """Überprüft, ob die notwendigen Umgebungsvariablen gesetzt sind"""
    required_vars = ["WEAVIATE_URL", "WEAVIATE_API_KEY"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"Fehler: Die folgenden Umgebungsvariablen sind nicht gesetzt: {', '.join(missing_vars)}")
        print("Bitte setzen Sie diese Variablen vor dem Ausführen des Skripts.")
        return False
    
    if not os.environ.get("OPENAI_APIKEY"):
        print("Warnung: OPENAI_APIKEY ist nicht gesetzt. Die Vektorisierung könnte fehlschlagen.")
    
    return True

def run_script(script_name):
    """Führt ein Python-Skript aus und gibt den Erfolg oder Misserfolg zurück"""
    print(f"Führe {script_name} aus...")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print(f"Fehler bei der Ausführung von {script_name}:")
        print(result.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="DogBot Weaviate Setup")
    parser.add_argument('--schema', action='store_true', help='Nur Schema erstellen')
    parser.add_argument('--import', action='store_true', dest='import_data', help='Nur Daten importieren')
    parser.add_argument('--test', action='store_true', help='Nur Tests ausführen')
    parser.add_argument('--all', action='store_true', help='Alles ausführen (Schema, Import, Test)')
    
    args = parser.parse_args()
    
    # Wenn keine Argumente angegeben wurden, --all verwenden
    if not (args.schema or args.import_data or args.test or args.all):
        args.all = True
    
    # Überprüfen, ob die Umgebungsvariablen gesetzt sind
    if not check_env_vars():
        return 1
    
    success = True
    
    if args.schema or args.all:
        success = run_script("weaviate_schema_setup.py") and success
    
    if (args.import_data or args.all) and success:
        success = run_script("weaviate_data_import.py") and success
    
    if (args.test or args.all) and success:
        success = run_script("test_weaviate_import.py") and success
    
    if success:
        print("Setup erfolgreich abgeschlossen!")
        return 0
    else:
        print("Setup mit Fehlern abgeschlossen. Siehe oben für Details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())