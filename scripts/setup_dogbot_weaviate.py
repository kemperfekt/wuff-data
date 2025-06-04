import os
import argparse
import subprocess
import sys

def check_env_vars():
    required_vars = ["WEAVIATE_URL", "WEAVIATE_API_KEY"]
    missing = [v for v in required_vars if not os.environ.get(v)]

    if missing:
        print(f"Fehler: Fehlende Umgebungsvariablen: {', '.join(missing)}")
        return False

    if not os.environ.get("OPENAI_APIKEY"):
        print("⚠️ Warnung: OPENAI_APIKEY ist nicht gesetzt – Vektorisierung könnte fehlschlagen.")

    return True

def run_script(script_name):
    print(f"\n▶️ Starte: {script_name}")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Erfolgreich: {script_name}")
        return True
    else:
        print(f"❌ Fehler in {script_name}:\n{result.stdout}\n{result.stderr}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Dogbot Weaviate Setup")
    parser.add_argument("--schema", action="store_true", help="Nur Schema (inkl. Löschen)")
    parser.add_argument("--import", dest="import_data", action="store_true", help="Nur Daten + Referenzen importieren")
    parser.add_argument("--test", action="store_true", help="Nur Test")
    parser.add_argument("--all", action="store_true", help="Alles: Schema + Import + Test")

    args = parser.parse_args()
    if not check_env_vars():
        return 1

    success = True
    if args.all or args.schema:
        success = run_script("weaviate_schema_setup.py") and success
    if args.all or args.import_data:
        success = run_script("weaviate_data_import.py") and success
    if args.all or args.test:
        success = run_script("test_weaviate_import.py") and success

    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())