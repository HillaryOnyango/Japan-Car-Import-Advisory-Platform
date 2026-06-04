import os
from decimal import Decimal
from pathlib import Path

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

USD_TO_KES = float(os.getenv("USD_TO_KES", "130"))

DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

SAMPLE_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "processed" / "cars_cleaned_sample.csv"


def load_sample_data():
    df = pd.read_csv(SAMPLE_DATA_PATH)

    if "price_kes" not in df.columns and "price_usd" in df.columns:
        df["price_kes"] = df["price_usd"] * USD_TO_KES

    return df


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


@st.cache_data(ttl=300)
def load_listings(limit=1000):
    query = f"""
        SELECT
            id,
            make,
            model,
            year,
            mileage,
            engine_size_cc,
            fuel_type,
            transmission,
            body_type,
            source_platform,
            price_usd,
            COALESCE(price_kes, price_usd * {USD_TO_KES}) AS price_kes,
            cleaned_at
        FROM cars_cleaned
        ORDER BY id DESC
        LIMIT %s
    """

    try:
        if not DB_HOST or DB_HOST in ["localhost", "127.0.0.1"]:
            return load_sample_data().head(limit)

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (int(limit),))
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]

        df = pd.DataFrame(rows, columns=columns)

        for col in df.columns:
            if df[col].map(lambda x: isinstance(x, Decimal)).any():
                df[col] = pd.to_numeric(df[col], errors="coerce")

        numeric_cols = ["year", "mileage", "engine_size_cc", "price_usd", "price_kes"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        if df.empty:
            return load_sample_data().head(limit)

        return df

    except Exception:
        return load_sample_data().head(limit)


def format_kes(value):
    if pd.isna(value):
        return "KES 0"
    return f"KES {value:,.0f}"


def format_number(value):
    if pd.isna(value):
        return "0"
    return f"{value:,.0f}"
