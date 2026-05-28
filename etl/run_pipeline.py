import pandas as pd
from scrapers.sbt_scraper import SBTScraper
from scrapers.beforward_scraper import BeForwardScraper
from etl.clean_listings import clean_car_data


def run_pipeline(max_pages: int = 1):
    scrapers = [SBTScraper(), BeForwardScraper()]
    all_listings = []

    for scraper in scrapers:
        print(f"Scraping {scraper.source_platform}...")
        all_listings.extend(scraper.scrape(max_pages=max_pages))

    raw_df = pd.DataFrame(all_listings)
    raw_df.to_csv("data/raw/car_listings.csv", index=False)

    if not raw_df.empty:
        clean_df = clean_car_data(raw_df)
        clean_df.to_csv("data/cleaned/car_listings_cleaned.csv", index=False)
        print("Pipeline completed successfully.")
    else:
        print("No listings scraped. Check selectors.")




def main():
    run_pipeline(max_pages=1)


if __name__ == "__main__":
    main()
