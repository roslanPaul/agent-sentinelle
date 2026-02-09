"""
Docstring for src.utils.logger
Système de logs professionnel avec rotation et niveaux.
"""

from loguru import logger
import sys
from pathlib import Path
from src.core.config import settings

def setup_logger():
    """
    Docstring for setup_logger
    Configure le logger avec :
    - Logs console (colorés)
    - Logs fichier (avec rotation)
    - Format structuré
    """

    # Supprime le handler par défaut
    logger.remove()

    # Handler 1 : Console (coloré, niveau INFO)
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> |"
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan> | "
                "<level>{message}</level>",
        level="DEBUG" if settings.DEBUG else "INFO",
        colorize=True  
    )

    # Handler 2 : Fichier détaillé (tout, avec rotation)
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)

    logger.add(
        log_path / "agent_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="00:00",
        retention="30 days",
        compression="zip"
    )

    # Handler 3 : Fichier erreurs uniquement
    logger.add(
        log_path / "errors_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="ERROR",
        rotation="00:00",
        retention="90 days"
    )

    logger.info(f"Logger initialisé - Mode {'DEBUG' if settings.DEBUG else 'PRODUCTION'}")

    return logger

# Instance globale
log = setup_logger()
