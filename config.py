"""
Configuration management for DogBot Data module.
Handles environment variables and settings securely.
"""
import os
from typing import Optional


class DataConfig:
    """Configuration class for data operations."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.weaviate_url = self._get_weaviate_url()
        self.weaviate_api_key = self._get_required_env("WEAVIATE_API_KEY")
        self.openai_api_key = self._get_required_env("OPENAI_APIKEY")
    
    def _get_weaviate_url(self) -> str:
        """Get Weaviate URL from environment or default."""
        url = os.getenv("WEAVIATE_URL")
        if not url:
            raise ValueError(
                "WEAVIATE_URL environment variable is required. "
                "Set it to your Weaviate cluster URL."
            )
        return url
    
    def _get_required_env(self, key: str) -> str:
        """Get required environment variable or raise error."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value
    
    @property
    def is_configured(self) -> bool:
        """Check if all required configuration is present."""
        try:
            return bool(self.weaviate_url and self.weaviate_api_key and self.openai_api_key)
        except ValueError:
            return False


# Global configuration instance
config = DataConfig()