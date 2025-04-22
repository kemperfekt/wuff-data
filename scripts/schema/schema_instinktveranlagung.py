import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from connect_weaviate import get_weaviate_client
import weaviate.classes.config as wc

# Verbindung zu Weaviate
client = get_weaviate_client()

# Vorher löschen, falls vorhanden
if client.collections.exists("Instinktveranlagung"):
    client.collections.delete("Instinktveranlagung")

# Neue Collection erstellen mit geschachteltem Instinkte-Objekt
client.collections.create(
    "Instinktveranlagung",
    properties=[
        wc.Property(name="gruppen_code", data_type=wc.DataType.TEXT),
        wc.Property(name="gruppe", data_type=wc.DataType.TEXT),
        wc.Property(name="untergruppe", data_type=wc.DataType.TEXT),
        wc.Property(name="funktion", data_type=wc.DataType.TEXT),
        wc.Property(name="merkmale", data_type=wc.DataType.TEXT),
        wc.Property(name="anforderungen", data_type=wc.DataType.TEXT),
        wc.Property(
            name="instinkte",
            data_type=wc.DataType.OBJECT,
            nested_properties=[
                wc.Property(name="jagd", data_type=wc.DataType.NUMBER),
                wc.Property(name="rudel", data_type=wc.DataType.NUMBER),
                wc.Property(name="territorial", data_type=wc.DataType.NUMBER),
                wc.Property(name="sexual", data_type=wc.DataType.NUMBER),
            ]
        )
    ],
    vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
    generative_config=wc.Configure.Generative.openai()
)

print("Collection 'Instinktveranlagung' wurde erfolgreich erstellt.")
client.close()
