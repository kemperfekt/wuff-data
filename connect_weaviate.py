"""
Secure Weaviate connection module for DogBot Data.
Uses environment-based configuration for security.
"""
import weaviate
from weaviate.classes.init import Auth
from config import config


def get_weaviate_client():
    """
    Create and return a Weaviate client with secure configuration.
    
    Returns:
        weaviate.WeaviateClient: Configured Weaviate client
        
    Raises:
        ValueError: If required environment variables are not set
    """
    if not config.is_configured:
        raise ValueError(
            "Weaviate configuration is incomplete. Please ensure the following "
            "environment variables are set: WEAVIATE_URL, WEAVIATE_API_KEY, OPENAI_APIKEY"
        )
    
    return weaviate.connect_to_weaviate_cloud(
        cluster_url=config.weaviate_url,
        auth_credentials=Auth.api_key(config.weaviate_api_key),
        headers={
            "X-OpenAI-Api-Key": config.openai_api_key
        }
    )
