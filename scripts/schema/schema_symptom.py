import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from connect_weaviate import get_weaviate_client
import weaviate.classes.config as wc

# Verbindung zu Weaviate
client = get_weaviate_client()

# Vorher löschen, falls vorhanden
if client.collections.exists("Symptom"):
    client.collections.delete("Symptom")

# Collection "Symptom" erstellen
client.collections.create(
    name="Symptom",
    properties=[
        wc.Property(name="symptom_name", data_type=wc.DataType.TEXT),
        wc.Property(name="beschreibung", data_type=wc.DataType.TEXT),
        wc.Property(name="tags", data_type=wc.DataType.TEXT_ARRAY),
        wc.Property(name="erste_hilfe", data_type=wc.DataType.TEXT),
        wc.Property(name="hypothese_zuhause", data_type=wc.DataType.TEXT),
        wc.Property(
            name="instinkt_varianten",
            data_type=wc.DataType.OBJECT,
            nested_properties=[
                wc.Property(name="jagd", data_type=wc.DataType.TEXT),
                wc.Property(name="rudel", data_type=wc.DataType.TEXT),
                wc.Property(name="territorial", data_type=wc.DataType.TEXT),
                wc.Property(name="sexual", data_type=wc.DataType.TEXT),
            ]
        )
    ],
    vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
    generative_config=wc.Configure.Generative.openai()
)

print("Collection 'Symptom' wurde erfolgreich erstellt.")
client.close()
