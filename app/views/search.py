import pandas as pd
import streamlit as st

from app.utils.db_utils import format_kes, load_listings


def render_search():
    st.title("🔍 Browse Japan Listings")
    st.write("Search and filter vehicles currently listed for export from Japan.")

    df = load_listings()

    if df.empty:
        st.info("No cleaned car data found yet. Run a scraper and ETL loader.")
        return

    with st.sidebar:
        st.markdown("### Filter Listings")

        makes = ["All"] + sorted(df["make"].dropna().unique().tolist())
        selected_make = st.selectbox("Make", makes)

        min_year = int(df["year"].min()) if pd.notna(df["year"].min()) else 2018
        max_year = int(df["year"].max()) if pd.notna(df["year"].max()) else 2026
        year_range = st.slider("Year", min_year, max_year, (min_year, max_year))

        min_price = int(df["price_kes"].min()) if pd.notna(df["price_kes"].min()) else 0
        max_price = int(df["price_kes"].max()) if pd.notna(df["price_kes"].max()) else 1000000
        price_range = st.slider("Price KES", min_price, max_price, (min_price, max_price))

        fuels = ["All"] + sorted(df["fuel_type"].dropna().unique().tolist())
        selected_fuel = st.selectbox("Fuel", fuels)

        transmissions = ["All"] + sorted(df["transmission"].dropna().unique().tolist())
        selected_transmission = st.selectbox("Transmission", transmissions)

    filtered = df.copy()

    if selected_make != "All":
        filtered = filtered[filtered["make"] == selected_make]

    filtered = filtered[
        (filtered["year"] >= year_range[0])
        & (filtered["year"] <= year_range[1])
        & (filtered["price_kes"] >= price_range[0])
        & (filtered["price_kes"] <= price_range[1])
    ]

    if selected_fuel != "All":
        filtered = filtered[filtered["fuel_type"] == selected_fuel]

    if selected_transmission != "All":
        filtered = filtered[filtered["transmission"] == selected_transmission]

    st.markdown(f"**{len(filtered):,} listings match your filters.**")

    display = filtered[
        [
            "make",
            "model",
            "year",
            "mileage",
            "engine_size_cc",
            "fuel_type",
            "transmission",
            "body_type",
            "price_kes",
            "source_platform",
        ]
    ].copy()

    display = display.rename(
        columns={
            "make": "Make",
            "model": "Model",
            "year": "Year",
            "mileage": "Mileage (km)",
            "engine_size_cc": "Engine (cc)",
            "fuel_type": "Fuel",
            "transmission": "Trans.",
            "body_type": "Body",
            "price_kes": "Price (KES)",
            "source_platform": "Platform",
        }
    )

    display["Price (KES)"] = display["Price (KES)"].apply(format_kes)
    display["Mileage (km)"] = display["Mileage (km)"].apply(
        lambda x: f"{x:,.0f}" if pd.notna(x) else ""
    )
    display["Engine (cc)"] = display["Engine (cc)"].apply(
        lambda x: f"{x:,.0f}" if pd.notna(x) else ""
    )

    st.dataframe(display.head(200), use_container_width=True)
