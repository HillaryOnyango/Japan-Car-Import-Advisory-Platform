import re
import pandas as pd
from config.settings import settings


def parse_number(value):
    if pd.isna(value):
        return None
    match = re.findall(r"[0-9,.]+", str(value))
    if not match:
        return None
    return float(match[0].replace(",", ""))


def clean_car_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["make"] = df["make"].astype(str).str.strip().str.title()
    df["model"] = df["model"].astype(str).str.strip().str.title()
    df["fuel_type"] = df["fuel_type"].astype(str).str.strip().str.title()
    df["transmission"] = df["transmission"].astype(str).str.strip().str.title()
    df["body_type"] = df["body_type"].astype(str).str.strip().str.title()

    df["mileage_km"] = df["mileage"].apply(parse_number)
    df["engine_size_cc"] = df["engine_size"].apply(parse_number)
    df["price_usd"] = df["price"].apply(parse_number)
    df["price_kes"] = df["price_usd"] * settings.exchange_rate_usd_kes

    df = df[df["year"] >= 2018]
    df = df.drop_duplicates(subset=["source_platform", "listing_url"])

    return df


if __name__ == "__main__":
    raw_path = "data/raw/car_listings.csv"
    clean_path = "data/cleaned/car_listings_cleaned.csv"
    df = pd.read_csv(raw_path)
    cleaned = clean_car_data(df)
    cleaned.to_csv(clean_path, index=False)
    print(f"Saved cleaned data to {clean_path}")
