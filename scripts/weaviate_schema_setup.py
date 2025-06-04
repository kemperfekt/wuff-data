# weaviate_schema_setup.py
import weaviate
import weaviate.classes.config as wvcc
from weaviate.collections.classes.config import Property
from weaviate.collections.classes.config import Tokenization
from weaviate.auth import AuthApiKey
import os
import warnings; warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():
    # Bestehende Weaviate-Zugangsdaten verwenden
    weaviate_url = os.environ["WEAVIATE_URL"]
    weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
    openai_api_key = os.environ.get("OPENAI_APIKEY")

    # Connect to Weaviate Cloud - verwende die neue Connect-Methode
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=AuthApiKey(api_key=weaviate_api_key),
        headers={"X-OpenAI-Api-Key": openai_api_key} if openai_api_key else {}
    )

    try:
        existing_collections = client.collections.list_all().keys()
        for name in existing_collections:
            client.collections.delete(name)
        print(f"Alle bestehenden Collections gelöscht: {', '.join(existing_collections)}")
    except Exception as e:
        print(f"Fehler beim Löschen bestehender Collections: {e}")

    print(f"Weaviate bereit: {client.is_ready()}")

    try:
        # Allgemein Collection
        client.collections.create(
            name="Allgemein",
            description="Grundlegende Informationen über Hunde, ihre Bedürfnisse und Verhalten",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                Property(name="thema", data_type=wvcc.DataType.TEXT),
                Property(name="beschreibung", data_type=wvcc.DataType.TEXT),
                Property(name="hundeperspektive", data_type=wvcc.DataType.TEXT)
            ]
        )

        # Instinkte Collection
        client.collections.create(
            name="Instinkte",
            description="Die vier grundlegenden Instinkte von Hunden",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                Property(
                    name="instinkt",
                    data_type=wvcc.DataType.TEXT,
                    description="Instinkt",
                    index_filterable=True,
                    index_searchable=True,
                    tokenization=Tokenization.FIELD
                ),
                Property(name="beschreibung", data_type=wvcc.DataType.TEXT),
                Property(name="hundesperspektive", data_type=wvcc.DataType.TEXT)
            ]
        )

        # Instinktveranlagung Collection
        client.collections.create(
            name="Instinktveranlagung",
            description="Hundegruppen mit spezifischer Instinktverteilung",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                Property(name="gruppen_code", data_type=wvcc.DataType.NUMBER),
                Property(
                    name="uebergruppe",
                    data_type=wvcc.DataType.TEXT,
                    description="Übergruppe",
                    index_filterable=True,
                    index_searchable=True,
                    tokenization=Tokenization.FIELD
                ),
                Property(
                    name="gruppe",
                    data_type=wvcc.DataType.TEXT,
                    description="Instinktgruppe",
                    index_filterable=True,
                    index_searchable=True,
                    tokenization=Tokenization.FIELD
                ),
                Property(name="funktion", data_type=wvcc.DataType.TEXT),
                Property(name="merkmale", data_type=wvcc.DataType.TEXT),
                Property(name="rassevertreter", data_type=wvcc.DataType.TEXT),
                Property(name="rassenbeispiele", data_type=wvcc.DataType.TEXT),
                Property(name="erziehungsanforderung", data_type=wvcc.DataType.TEXT),
                Property(
                    name="jagdinstinkt",
                    data_type=wvcc.DataType.NUMBER,
                    description="Ausprägung des Jagdinstinkts",
                    index_filterable=True,
                    index_searchable=False
                ),
                Property(
                    name="territorialinstinkt",
                    data_type=wvcc.DataType.NUMBER,
                    description="Ausprägung des Territorialinstinkts",
                    index_filterable=True,
                    index_searchable=False
                ),
                Property(name="rudelinstinkt", data_type=wvcc.DataType.NUMBER),
                Property(name="sexualinstinkt", data_type=wvcc.DataType.NUMBER),
                Property(name="hundeperspektive", data_type=wvcc.DataType.TEXT)
            ]
        )

        # Rassen Collection
        client.collections.create(
            name="Rassen",
            description="Hunderassen und ihre Zuordnung zu Instinktgruppen",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                Property(name="rassename", data_type=wvcc.DataType.TEXT),
                Property(name="alternative_namen", data_type=wvcc.DataType.TEXT),
                Property(name="ursprungsland", data_type=wvcc.DataType.TEXT),
                Property(name="gruppen_code", data_type=wvcc.DataType.NUMBER)
            ]
        )

        # Erziehung Collection
        client.collections.create(
            name="Erziehung",
            description="Erziehungsaufgaben und deren Durchführung",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                Property(
                    name="erziehungsaufgabe",
                    data_type=wvcc.DataType.TEXT,
                    description="Erziehungsaufgabe",
                    index_filterable=True,
                    index_searchable=True,
                    tokenization=Tokenization.FIELD
                ),
                Property(name="anleitung", data_type=wvcc.DataType.TEXT),
                Property(name="hintergrund", data_type=wvcc.DataType.TEXT),
                Property(name="hundeperspektive", data_type=wvcc.DataType.TEXT),
                Property(name="relevante_instinkte", data_type=wvcc.DataType.TEXT)
            ]
        )

        # Symptome Collection
        client.collections.create(
            name="Symptome",
            description="Problematische Verhaltensweisen von Hunden und deren Lösungen",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                Property(name="symptom_name", data_type=wvcc.DataType.TEXT),
                Property(name="schnelldiagnose", data_type=wvcc.DataType.TEXT),
                Property(name="tags_schnelldiagnose", data_type=wvcc.DataType.TEXT_ARRAY),
                Property(name="hundeperspektive_jagdinstinkt", data_type=wvcc.DataType.TEXT),
                Property(name="tags_hundeperspektive_jagdinstinkt", data_type=wvcc.DataType.TEXT_ARRAY),
                Property(name="hundeperspektive_rudelinstinkt", data_type=wvcc.DataType.TEXT),
                Property(name="tags_hundeperspektive_rudelinstinkt", data_type=wvcc.DataType.TEXT_ARRAY),
                Property(name="hundeperspektive_territorialinstinkt", data_type=wvcc.DataType.TEXT),
                Property(name="tags_hundeperspektive_territorialinstinkt", data_type=wvcc.DataType.TEXT_ARRAY),
                Property(name="hundeperspektive_sexualinstinkt", data_type=wvcc.DataType.TEXT),
                Property(name="tags_hundeperspektive_sexualinstinkt", data_type=wvcc.DataType.TEXT_ARRAY),
                Property(name="erste_hilfe", data_type=wvcc.DataType.TEXT),
                Property(name="tags_erste_hilfe", data_type=wvcc.DataType.TEXT_ARRAY)
            ]
        )
        
        print("Schema erfolgreich erstellt!")
    except Exception as e:
        print(f"Fehler beim Erstellen des Schemas: {e}")
    finally:
        # Ressourcen freigeben (wichtig in v4)
        client.close()

if __name__ == "__main__":
    main()