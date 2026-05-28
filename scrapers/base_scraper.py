from abc import ABC, abstractmethod
from datetime import datetime

class BaseScraper(ABC):
    source_platform: str

    @abstractmethod
    def scrape(self, max_pages: int = 1) -> list[dict]:
        """Return a list of raw car listing dictionaries."""
        raise NotImplementedError

    def add_metadata(self, listing: dict) -> dict:
        listing["source_platform"] = self.source_platform
        listing["scraped_at"] = datetime.utcnow().isoformat()
        return listing
