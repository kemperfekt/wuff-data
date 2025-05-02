import os
import weaviate
from weaviate.classes.init import Auth

# Statische Weaviate-URL
weaviate_url = "https://cpmlrjetsgqskhwx9eqgg.c0.europe-west3.gcp.weaviate.cloud"

# API Keys aus Umgebungsvariable
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
openai_api_key = os.environ["OPENAI_APIKEY"] 

# Verbindung herstellen
def get_weaviate_client():
    return weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
        headers={
        "X-OpenAI-Api-Key": openai_api_key
    }
    )
