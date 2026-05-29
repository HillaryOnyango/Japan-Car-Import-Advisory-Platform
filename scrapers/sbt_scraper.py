import re
import time
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.sbtjapan.com"
SEARCH_URL = "https://www.sbtjapan.com/used-cars/?year_f=2018"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def clean_int(value):
    if not value:
        return None
    value = re.sub(r"[^0-9]", "", str(value))
    return int(value) if value else None


def parse_card(card):
    text = " ".join(card.get_text(" ", strip=True).split())

    year_match = re.search(r"\b(2018|2019|2020|2021|2022|2023|2024|2025|2026)\b", text)
    price_match = re.search(r"US\$?\s*([0-9,]+)|\$\s*([0-9,]+)", text, re.I)
    mileage_match = re.search(r"([0-9,]+)\s*km", text, re.I)
    engine_match = re.search(r"([0-9,]+)\s*cc", text, re.I)

    if not year_match or not price_match:
        return None

    year = int(year_match.group(1))
    price_text = price_match.group(1) or price_match.group(2)
    price_usd = clean_int(price_text)

    if not price_usd or price_usd < 3000 or price_usd > 80000:
        return None

    link = card.select_one("a[href]")
    listing_url = urljoin(BASE_URL, link["href"]) if link else None

    if not listing_url:
        return None

    title = ""
    for selector in ["h3", "h2", ".title", ".car-name", ".vehicle-title", "a"]:
        tag = card.select_one(selector)
        if tag:
            candidate = tag.get_text(" ", strip=True)
            if candidate and len(candidate.split()) >= 2:
                title = candidate
                break

    title = re.sub(r"^\d{4}\s+", "", title).strip()
    title = re.sub(r"US\$.*", "", title).strip()

    parts = title.replace("-", " ").split()
    make = parts[0].title() if len(parts) >= 1 else None
    model = " ".join(parts[1:4]).title() if len(parts) >= 2 else None

    if not make or not model:
        return None

    image = card.select_one("img")
    image_url = urljoin(BASE_URL, image["src"]) if image and image.get("src") else None

    stock_id = None
    stock_match = re.search(r"Stock\s*(?:No\.?|ID)?\s*[:#]?\s*([A-Z0-9-]+)", text, re.I)
    if stock_match:
        stock_id = stock_match.group(1)

    fuel_type = None
    for fuel in ["Petrol", "Diesel", "Hybrid", "Electric", "Gasoline"]:
        if fuel.lower() in text.lower():
            fuel_type = "Petrol" if fuel == "Gasoline" else fuel
            break

    transmission = None
    if re.search(r"\bAT\b|Automatic", text, re.I):
        transmission = "AT"
    elif re.search(r"\bMT\b|Manual", text, re.I):
        transmission = "MT"

    return {
        "source_platform": "SBT Japan",
        "listing_url": listing_url,
        "make": make,
        "model": model,
        "year": year,
        "mileage": clean_int(mileage_match.group(1)) if mileage_match else None,
        "engine_size_cc": clean_int(engine_match.group(1)) if engine_match else None,
        "fuel_type": fuel_type,
        "transmission": transmission,
        "body_type": None,
        "drive_type": None,
        "price_usd": price_usd,
        "price_jpy": None,
        "stock_id": stock_id,
        "image_url": image_url,
        "scraped_at": datetime.utcnow(),
    }


def scrape_sbt(max_pages=3, delay=2):
    results = []
    seen = set()

    for page in range(1, max_pages + 1):
        url = SEARCH_URL if page == 1 else f"{SEARCH_URL}&page={page}"
        print(f"Scraping SBT Japan: {url}")

        response = requests.get(url, headers=HEADERS, timeout=30)
        print("Status:", response.status_code)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.find_all(["div", "li", "article"])
        page_count = 0

        for card in cards:
            item = parse_card(card)
            if item and item["listing_url"] not in seen:
                seen.add(item["listing_url"])
                results.append(item)
                page_count += 1

        print(f"Found {page_count} usable SBT listings on page {page}")
        time.sleep(delay)

    return results


if __name__ == "__main__":
    cars = scrape_sbt(max_pages=2)
    print(f"Total SBT cars scraped: {len(cars)}")
    for car in cars[:10]:
        print(car)
