from connect_weaviate import get_weaviate_client
import weaviate.classes.config as wc

client = get_weaviate_client()

# Vorher löschen, falls vorhanden
if client.collections.exists("Instinktveranlagung"):
    client.collections.delete("Instinktveranlagung")

# Neu anlegen
client.collections.create(
    "Instinktveranlagung",
    properties=[
        wc.Property(name="gruppen_code", data_type=wc.DataType.TEXT),
        wc.Property(name="gruppe", data_type=wc.DataType.TEXT),
        wc.Property(name="untergruppe", data_type=wc.DataType.TEXT),
        wc.Property(name="funktion", data_type=wc.DataType.TEXT),
        wc.Property(name="merkmale", data_type=wc.DataType.TEXT),
        wc.Property(name="anforderungen", data_type=wc.DataType.TEXT),
        wc.Property(name="instinkte", data_type=wc.DataType.OBJECT),
    ],
    vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
    generative_config=wc.Configure.Generative.openai()
)

print("Collection 'Instinktveranlagung' wurde erfolgreich erstellt.")
client.close()
