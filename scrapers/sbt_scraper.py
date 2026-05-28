import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper

class SBTScraper(BaseScraper):
    source_platform = "SBT Japan"
    base_url = "https://www.sbtjapan.com"

    def scrape(self, max_pages: int = 1) -> list[dict]:
        listings = []
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}/used-cars/?page={page}"
            response = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            # TODO: Update selectors after inspecting live HTML.
            cards = soup.select(".car-card, .stock-item, .vehicle-card")
            for card in cards:
                listing = {
                    "listing_url": None,
                    "make": None,
                    "model": None,
                    "year": None,
                    "mileage": None,
                    "engine_size": None,
                    "fuel_type": None,
                    "transmission": None,
                    "body_type": None,
                    "price": None,
                    "image_url": None,
                }
                listings.append(self.add_metadata(listing))
        return listings

if __name__ == "__main__":
    scraper = SBTScraper()
    print(scraper.scrape(max_pages=1)[:3])
