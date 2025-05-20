# weaviate_schema_setup.py
import weaviate
import weaviate.classes.config as wvcc
from weaviate.auth import AuthApiKey
import os

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

    print(f"Weaviate bereit: {client.is_ready()}")

    try:
        # Allgemein Collection
        client.collections.create(
            name="Allgemein",
            description="Grundlegende Informationen über Hunde, ihre Bedürfnisse und Verhalten",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                wvcc.Property(name="thema", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="beschreibung", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="hundeperspektive", data_type=wvcc.DataType.TEXT)
            ]
        )

        # Instinkte Collection
        client.collections.create(
            name="Instinkte",
            description="Die vier grundlegenden Instinkte von Hunden",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                wvcc.Property(name="instinkt", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="beschreibung", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="hundesperspektive", data_type=wvcc.DataType.TEXT)
            ]
        )

        # Instinktveranlagung Collection
        client.collections.create(
            name="Instinktveranlagung",
            description="Hundegruppen mit spezifischer Instinktverteilung",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                wvcc.Property(name="gruppen_code", data_type=wvcc.DataType.NUMBER),
                wvcc.Property(name="uebergruppe", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="gruppe", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="funktion", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="merkmale", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="rassevertreter", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="rassenbeispiele", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="erziehungsanforderung", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="jagdinstinkt", data_type=wvcc.DataType.NUMBER),
                wvcc.Property(name="territorialinstinkt", data_type=wvcc.DataType.NUMBER),
                wvcc.Property(name="rudelinstinkt", data_type=wvcc.DataType.NUMBER),
                wvcc.Property(name="sexualinstinkt", data_type=wvcc.DataType.NUMBER),
                wvcc.Property(name="hundeperspektive", data_type=wvcc.DataType.TEXT)
            ]
        )

        # Rassen Collection
        client.collections.create(
            name="Rassen",
            description="Hunderassen und ihre Zuordnung zu Instinktgruppen",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                wvcc.Property(name="rassename", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="alternative_namen", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="ursprungsland", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="gruppen_code", data_type=wvcc.DataType.NUMBER),
                wvcc.Property(
                    name="hatInstinktveranlagung", 
                    data_type=wvcc.DataType.OBJECT_ARRAY,
                    reference_to="Instinktveranlagung"
                )
            ]
        )

        # Erziehung Collection
        client.collections.create(
            name="Erziehung",
            description="Erziehungsaufgaben und deren Durchführung",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                wvcc.Property(name="erziehungsaufgabe", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="anleitung", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="hintergrund", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="hundeperspektive", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="relevante_instinkte", data_type=wvcc.DataType.TEXT),
                wvcc.Property(
                    name="betrifftInstinkte", 
                    data_type=wvcc.DataType.OBJECT_ARRAY,
                    reference_to="Instinkte"
                )
            ]
        )

        # Symptome Collection
        client.collections.create(
            name="Symptome",
            description="Problematische Verhaltensweisen von Hunden und deren Lösungen",
            vectorizer_config=wvcc.Configure.Vectorizer.text2vec_openai(),
            properties=[
                wvcc.Property(name="symptom_name", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="schnelldiagnose", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="tags_schnelldiagnose", data_type=wvcc.DataType.TEXT_ARRAY),
                wvcc.Property(name="hundeperspektive_jagdinstinkt", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="tags_hundeperspektive_jagdinstinkt", data_type=wvcc.DataType.TEXT_ARRAY),
                wvcc.Property(name="hundeperspektive_rudelinstinkt", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="tags_hundeperspektive_rudelinstinkt", data_type=wvcc.DataType.TEXT_ARRAY),
                wvcc.Property(name="hundeperspektive_territorialinstinkt", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="tags_hundeperspektive_territorialinstinkt", data_type=wvcc.DataType.TEXT_ARRAY),
                wvcc.Property(name="hundeperspektive_sexualinstinkt", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="tags_hundeperspektive_sexualinstinkt", data_type=wvcc.DataType.TEXT_ARRAY),
                wvcc.Property(name="erste_hilfe", data_type=wvcc.DataType.TEXT),
                wvcc.Property(name="tags_erste_hilfe", data_type=wvcc.DataType.TEXT_ARRAY),
                wvcc.Property(
                    name="beziehtSichAufInstinkte", 
                    data_type=wvcc.DataType.OBJECT_ARRAY,
                    reference_to="Instinkte"
                ),
                wvcc.Property(
                    name="empfohleneErziehungsaufgaben", 
                    data_type=wvcc.DataType.OBJECT_ARRAY,
                    reference_to="Erziehung"
                )
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