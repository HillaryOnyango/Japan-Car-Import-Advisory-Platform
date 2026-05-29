import os
import warnings

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=UserWarning, module="pandas.io.sql")

load_dotenv()

USD_TO_KES = float(os.getenv("USD_TO_KES", "130"))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "japan_car_import_db")
DB_USER = os.getenv("DB_USER", "car_admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1900")


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
        LIMIT {int(limit)}
    """

    try:
        with get_connection() as conn:
            df = pd.read_sql_query(query, conn)

        numeric_cols = ["year", "mileage", "engine_size_cc", "price_usd", "price_kes"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df
    except Exception as e:
        st.warning(f"Could not load database data yet: {e}")
        return pd.DataFrame()


def format_kes(value):
    if pd.isna(value):
        return "KES 0"
    return f"KES {value:,.0f}"


def format_number(value):
    if pd.isna(value):
        return "0"
    return f"{value:,.0f}"
