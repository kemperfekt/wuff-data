import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from connect_weaviate import get_weaviate_client
import weaviate.classes.config as wc

# Verbindung zu Weaviate aufbauen
client = get_weaviate_client()

# Prüfen, ob die Collection 'Rasse' bereits existiert
if not client.collections.exists("Rasse"):
    # Collection 'Rasse' erstellen
    client.collections.create(
        name="Rasse",
        properties=[
            wc.Property(name="rassename", data_type=wc.DataType.TEXT),
            wc.Property(name="alternative_namen", data_type=wc.DataType.TEXT),
            wc.Property(name="ursprungsland", data_type=wc.DataType.TEXT),
            wc.Property(name="gruppen_code", data_type=wc.DataType.TEXT)
        ],
        references=[
            wc.ReferenceProperty(name="verweis_hunderasse", target_collection="Hunderasse")
        ],
        vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),  # Optional: Vektorisierer
        generative_config=wc.Configure.Generative.openai()            # Optional: Generative Konfiguration
    )
    print("Collection 'Rasse' erfolgreich erstellt.")
else:
    print("Collection 'Rasse' existiert bereits.")
client.close()
