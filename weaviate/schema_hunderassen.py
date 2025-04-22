from connect_weaviate import get_weaviate_client
import weaviate.classes.config as wc

# Verbindung zu Weaviate aufbauen
client = get_weaviate_client()

# Vorher löschen, falls vorhanden
if client.collections.exists("Hunderassen"):
    client.collections.delete("Hunderassen")

# Neue Collection erstellen
client.collections.create(
    name="Hunderassen",
    properties=[
        wc.Property(name="rassename", data_type=wc.DataType.TEXT),
        wc.Property(name="alternative_namen", data_type=wc.DataType.TEXT),
        wc.Property(name="ursprungsland", data_type=wc.DataType.TEXT),
        wc.Property(name="gruppen_code", data_type=wc.DataType.TEXT),
    ],
    references=[
        wc.ReferenceProperty(name="verweis_instinktveranlagung", target_collection="Instinktveranlagung")
    ],
    vectorizer_config=wc.Configure.Vectorizer.text2vec_openai(),
    generative_config=wc.Configure.Generative.openai()
)

print("Collection 'Hunderassen' wurde erfolgreich erstellt.")
client.close()
