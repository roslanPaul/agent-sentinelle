"""
Configuration centralisée de l'application.
Toutes les variables d'environnement sont gérées ici.
"""
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path


class Settings(BaseSettings):
    """
    Configuration globale avec validation automatique.
    Les valeurs viennent du fichier .env
    """

    # Application
    APP_NAME: str = "Agent Sentinelle"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # OpenAI
    OPENAI_API_KEY: str = "sk-placeholder"

    # Telegram
    TELEGRAM_BOT_TOKEN: str = "placeholder"

    # Database
    DATABASE_PATH: Path = Path("data/agent_sentinelle.db")

    # Redis (pour task queue)
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Scraping
    SCRAPING_INTERVAL_MINUTES: int = 5
    MAX_REQUESTS_PER_HOUR: int = 120
    REQUEST_TIMEOUT_SECONDS: int = 15

    # Stealth
    USE_PROXIES: bool = False
    PROXY_LIST: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instance globale (singleton)
settings = Settings()