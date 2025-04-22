import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import pandas as pd
from pprint import pprint
from pathlib import Path

# Excel einlesen
path = Path("../../data/rassen/Rasseliste_import.xlsx")
df_rassen = pd.read_excel(path, sheet_name="Rassen", dtype={"gruppen_code": str})
df_mapping = pd.read_excel(path, sheet_name="Mapping", dtype={"gruppen_code": str})
df_joined = pd.merge(df_rassen, df_mapping, on="gruppen_code", how="left")

# Mapping importieren
from get_hunderasse_mapping import gruppe_untergruppe_to_uuid

def normalize_key(gruppe, untergruppe):
    return (
        gruppe.lower().replace("-", "").replace(" ", ""),
        untergruppe.lower().replace("-", "").replace(" ", "")
    )

upload_batch = []
for _, row in df_joined.head(5).iterrows():
    gruppe_norm, untergruppe_norm = normalize_key(row["gruppe"], row["untergruppe"])
    uuid_ref = gruppe_untergruppe_to_uuid.get((gruppe_norm, untergruppe_norm))

    upload_batch.append({
        "rassename": row["rassename"],
        "alternative_namen": row["alternative_namen"],
        "ursprungsland": row["ursprungsland"],
        "gruppen_code": row["gruppen_code"],
        "verweis_hunderasse_uuid": uuid_ref,
    })

pprint(upload_batch)
