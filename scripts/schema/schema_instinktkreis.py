from connect_weaviate import get_weaviate_client
from weaviate.classes.config import Configure, Property, DataType

# Verbindung zu Weaviate herstellen
client = get_weaviate_client()

# Prüfen, ob die Collection "Rasse" bereits existiert
if "Rasse" not in client.collections.list_all():
    client.collections.create(
        "Hunderasse",
        vectorizer_config=Configure.Vectorizer.text2vec_openai(),
        properties=[
            Property(name="gruppe", data_type=DataType.TEXT),
            Property(name="untergruppe", data_type=DataType.TEXT),
            Property(name="funktion", data_type=DataType.TEXT),
            Property(name="merkmale", data_type=DataType.TEXT),
            Property(name="erziehungsanforderung", data_type=DataType.TEXT),
            Property(name="jagdinstinkt", data_type=DataType.NUMBER),
            Property(name="rudelinstinkt", data_type=DataType.NUMBER),
            Property(name="territorialinstinkt", data_type=DataType.NUMBER),
            Property(name="sexualinstinkt", data_type=DataType.NUMBER),
            Property(name="instinktkommentar", data_type=DataType.TEXT),
        ]
    )
    print("✅ Collection 'Hunderasse' wurde erfolgreich erstellt.")
else:
    print("ℹ️ Collection 'Hunderasse' ist bereits vorhanden.")

client.close()
