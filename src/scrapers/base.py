"""
Docstring for src.scrapers.base
Chaque site (Leboncoin, SeLoger, ...) héritera de cette classe
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from playwright.async_api import async_playwright, Browser, Page
from src.utils.logger import log

@dataclass
class Listing:
    """Structure d'une annonce immobilière."""
    id: str
    title: str
    price: int
    surface: Optional[float]
    location: str
    url: str
    description: str
    photos: List[str]
    first_seen: datetime
    last_update: datetime
    source: str # 'leboncoin', 'seloger', etc.

class BaseScraper(ABC):
    """
    Docstring for BaseScraper
    Classe abstraite pour tous les scrapers.
    Gère la logique commune (navigation, retry, etc.)
    """

    def __init__(self, name: str):
        self.name = name
        self._playwright = None
        self.context = None # Ajout d'un contexte pour isoler les cookies/cache
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def __aenter__(self):
        """Context manager pour gérer le navigateur."""
        self._playwright = await async_playwright().start()

        self.browser = await self._playwright.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        # Création d'un contexte avec un User-Agent réaliste
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )

        self.page = await self.context.new_page()
        # Timeout par défaut de 30 secondes pour éviter de bloquer l'agent
        self.page.set_default_timeout(30000)
        
        log.info(f"🌐 Scraper [{self.name}] : Navigateur initialisé")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Ferme proprement le navigateur."""
        if self.page: await self.page.close()
        if self.context: await self.context.close()
        if self.browser: await self.browser.close()
        if self._playwright: await self._playwright.stop()
        log.info(f"🌐 Scraper [{self.name}] : Ressources libérées")
    
    @abstractmethod
    async def scrape(self, search_url: str) -> List[Listing]:
        pass

    @abstractmethod
    def extract_listing_from_card(self, card_html: str) -> Optional[Listing]:
        pass