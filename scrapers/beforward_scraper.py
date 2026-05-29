import re
import time
from datetime import datetime
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.beforward.jp"
SEARCH_URL = "https://www.beforward.jp/stocklist/mfg_year_from%3D2018/mfg_year_to%3D2026/"


def clean_int(value):
    if not value:
        return None
    value = re.sub(r"[^0-9]", "", str(value))
    return int(value) if value else None


def parse_card(card):
    text = " ".join(card.get_text(" ", strip=True).split())

    if "Ref No." not in text:
        return None

    ref_match = re.search(r"Ref No\.\s*([A-Z0-9]+)", text)
    year_match = re.search(r"\b(2018|2019|2020|2021|2022|2023|2024|2025|2026)\b", text)
    price_match = re.search(r"\$\s*([0-9,]+)", text)
    mileage_match = re.search(r"([0-9,]+)\s*km", text, re.I)
    engine_match = re.search(r"([0-9,]+)\s*cc", text, re.I)

    if not ref_match or not year_match or not price_match:
        return None

    stock_id = ref_match.group(1)
    year = int(year_match.group(1))
    price_usd = clean_int(price_match.group(1))
    mileage = clean_int(mileage_match.group(1)) if mileage_match else None
    engine_size_cc = clean_int(engine_match.group(1)) if engine_match else None

    if price_usd is None or price_usd < 3000 or price_usd > 80000:
        return None

    link_tag = card.select_one("a[href]")
    listing_url = urljoin(BASE_URL, link_tag["href"]) if link_tag else f"{BASE_URL}/stocklist/{stock_id}/"

    img_tag = card.select_one("img")
    image_url = urljoin(BASE_URL, img_tag["src"]) if img_tag and img_tag.get("src") else None

    title = None
    for selector in ["h3", "h2", ".stock-title", ".vehicle-title", ".item-title", "a"]:
        tag = card.select_one(selector)
        if tag:
            candidate = tag.get_text(" ", strip=True)
            if candidate and len(candidate.split()) >= 2:
                title = candidate
                break

    if not title:
        title_match = re.search(rf"{year}\s+([A-Z][A-Z0-9\s/-]+)", text)
        title = title_match.group(1).strip() if title_match else ""

    title = re.sub(r"^\d{4}\s+", "", title).strip()
    title = re.sub(r"Ref No\..*", "", title).strip()

    parts = title.replace("-", " ").split()

    make = parts[0].title() if len(parts) >= 1 else None
    model = " ".join(parts[1:4]).title() if len(parts) >= 2 else None

    if not make or not model:
        return None

    fuel_type = None
    for fuel in ["Petrol", "Diesel", "Hybrid", "Electric"]:
        if fuel.lower() in text.lower():
            fuel_type = fuel
            break

    transmission = None
    if re.search(r"\bAT\b|Automatic", text, re.I):
        transmission = "AT"
    elif re.search(r"\bMT\b|Manual", text, re.I):
        transmission = "MT"

    drive_type = None
    drive_match = re.search(r"\b(2WD|4WD|AWD)\b", text, re.I)
    if drive_match:
        drive_type = drive_match.group(1).upper()

    return {
        "source_platform": "BE FORWARD",
        "listing_url": listing_url,
        "make": make,
        "model": model,
        "year": year,
        "mileage": mileage,
        "engine_size_cc": engine_size_cc,
        "fuel_type": fuel_type,
        "transmission": transmission,
        "body_type": None,
        "drive_type": drive_type,
        "price_usd": price_usd,
        "price_jpy": None,
        "stock_id": stock_id,
        "image_url": image_url,
        "scraped_at": datetime.utcnow(),
    }


def scrape_beforward(max_pages=3, delay=2):
    results = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page_obj = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            )
        )

        for page_num in range(1, max_pages + 1):
            url = SEARCH_URL if page_num == 1 else f"{SEARCH_URL}page%3D{page_num}/"
            print(f"Scraping: {url}")

            page_obj.goto(url, wait_until="domcontentloaded", timeout=120000)
            time.sleep(3)

            html = page_obj.content()
            soup = BeautifulSoup(html, "html.parser")

            cards = soup.select("li, article, div")
            page_count = 0

            for card in cards:
                item = parse_card(card)
                if item and item["stock_id"] not in seen:
                    seen.add(item["stock_id"])
                    results.append(item)
                    page_count += 1

            print(f"Found {page_count} usable listings on page {page_num}")
            time.sleep(delay)

        browser.close()

    return results


if __name__ == "__main__":
    cars = scrape_beforward(max_pages=2)
    print(f"Total scraped cars: {len(cars)}")
    for car in cars[:10]:
        print(car)
