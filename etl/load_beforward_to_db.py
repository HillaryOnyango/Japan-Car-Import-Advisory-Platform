import os
import sys

import psycopg2
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scrapers.beforward_scraper import scrape_beforward
from scrapers.sbt_scraper import scrape_sbt


load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "japan_car_import_db")
DB_USER = os.getenv("DB_USER", "car_admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1900")
USD_TO_KES = float(os.getenv("USD_TO_KES", "130"))


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def insert_raw_cars(cars):
    sql = """
        INSERT INTO cars_raw (
            source_platform, listing_url, make, model, year, mileage,
            engine_size_cc, fuel_type, transmission, body_type, drive_type,
            price_usd, price_jpy, stock_id, image_url, scraped_at
        )
        VALUES (
            %(source_platform)s, %(listing_url)s, %(make)s, %(model)s, %(year)s,
            %(mileage)s, %(engine_size_cc)s, %(fuel_type)s, %(transmission)s,
            %(body_type)s, %(drive_type)s, %(price_usd)s, %(price_jpy)s,
            %(stock_id)s, %(image_url)s, %(scraped_at)s
        )
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            for car in cars:
                cur.execute(sql, car)
        conn.commit()


def clean_raw_to_cleaned():
    sql = f"""
        INSERT INTO cars_cleaned (
            raw_car_id, make, model, year, mileage, engine_size_cc,
            fuel_type, transmission, body_type, source_platform,
            price_usd, price_kes
        )
        SELECT
            id,
            INITCAP(make),
            INITCAP(model),
            year,
            mileage,
            engine_size_cc,
            fuel_type,
            transmission,
            body_type,
            source_platform,
            price_usd,
            price_usd * {USD_TO_KES}
        FROM cars_raw
        WHERE year >= 2018
          AND year <= 2026
          AND price_usd BETWEEN 3000 AND 80000
          AND make IS NOT NULL
          AND model IS NOT NULL
          AND NOT EXISTS (
              SELECT 1
              FROM cars_cleaned c
              WHERE c.raw_car_id = cars_raw.id
          );
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()


def main():
    all_cars = []

    beforward_cars = scrape_beforward(max_pages=3, delay=2)
    print(f"BE FORWARD scraped: {len(beforward_cars)}")
    all_cars.extend(beforward_cars)

    sbt_cars = scrape_sbt(max_pages=3, delay=2)
    print(f"SBT Japan scraped: {len(sbt_cars)}")
    all_cars.extend(sbt_cars)

    print(f"Total scraped cars: {len(all_cars)}")

    if not all_cars:
        print("No cars scraped from either source.")
        return

    insert_raw_cars(all_cars)
    clean_raw_to_cleaned()

    print("Loaded BE FORWARD and SBT Japan data into cars_raw and cars_cleaned")


if __name__ == "__main__":
    main()
