import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import streamlit as st
import psycopg2

from calculator.import_cost_calculator import ImportCostInput, calculate_import_cost


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


def load_cars():
    try:
        with get_connection() as conn:
            return pd.read_sql_query(
                "SELECT * FROM cars_cleaned ORDER BY id DESC LIMIT 500",
                conn,
            )
    except Exception as e:
        st.warning(f"Could not load database data yet: {e}")
        return pd.DataFrame()


st.set_page_config(
    page_title="Japan Car Import Advisory Platform",
    page_icon="🚗",
    layout="wide",
)

st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select page",
    [
        "Home",
        "Japan Listings",
        "Import Cost Calculator",
        "Analytics",
        "ML Price Predictor",
    ],
)

if page == "Home":
    st.title("🚗 Japan Car Import Advisory Platform")
    st.write("Compare Japan import costs with local Kenyan car market prices.")

    st.subheader("Project Overview")
    st.write(
        """
        This platform extracts Japanese car listings, cleans them, stores them,
        estimates Kenya import costs, compares local vs import prices, and predicts
        fair Japan car prices using machine learning.
        """
    )

    cars = load_cars()

    col1, col2, col3 = st.columns(3)
    col1.metric("Cars in database", len(cars))
    col2.metric("Data sources", cars["source_platform"].nunique() if not cars.empty else 0)
    col3.metric("Average price USD", round(cars["price_usd"].mean(), 2) if not cars.empty else 0)

elif page == "Japan Listings":
    st.title("Japan Car Listings")

    cars = load_cars()

    if cars.empty:
        st.info("No cleaned car data found yet. Next step: run a scraper and ETL loader.")
    else:
        st.dataframe(cars, use_container_width=True)

elif page == "Import Cost Calculator":
    st.title("Kenya Import Cost Calculator")

    col1, col2 = st.columns(2)

    with col1:
        purchase_price = st.number_input("Purchase price USD", min_value=0.0, value=8000.0)
        shipping_cost = st.number_input("Shipping cost USD", min_value=0.0, value=1200.0)
        insurance = st.number_input("Insurance USD", min_value=0.0, value=100.0)
        exchange_rate = st.number_input("USD to KES rate", min_value=1.0, value=129.0)

    with col2:
        import_duty_rate = st.number_input("Import duty rate", value=0.25)
        excise_rate = st.number_input("Excise duty rate", value=0.20)
        vat_rate = st.number_input("VAT rate", value=0.16)
        idf_rate = st.number_input("IDF rate", value=0.025)
        rdl_rate = st.number_input("RDL rate", value=0.02)

    port_charges = st.number_input("Port charges KES", min_value=0.0, value=45000.0)
    clearing_fees = st.number_input("Clearing fees KES", min_value=0.0, value=50000.0)
    registration_cost = st.number_input("Registration cost KES", min_value=0.0, value=13800.0)

    if st.button("Calculate Import Cost"):
        data = ImportCostInput(
            purchase_price_usd=purchase_price,
            shipping_cost_usd=shipping_cost,
            insurance_usd=insurance,
            usd_to_kes=exchange_rate,
            import_duty_rate=import_duty_rate,
            excise_duty_rate=excise_rate,
            vat_rate=vat_rate,
            idf_rate=idf_rate,
            rdl_rate=rdl_rate,
            port_charges_kes=port_charges,
            clearing_fees_kes=clearing_fees,
            registration_cost_kes=registration_cost,
        )

        result = calculate_import_cost(data)

        st.success("Import cost calculated")

        st.metric("Total Import Cost KES", f"{result.total_import_cost_kes:,.2f}")
        st.json(result.__dict__)

elif page == "Analytics":
    st.title("Analytics Dashboard")

    cars = load_cars()

    if cars.empty:
        st.info("No data available yet.")
    else:
        st.subheader("Average price by make")
        chart_data = cars.groupby("make", as_index=False)["price_usd"].mean()
        st.bar_chart(chart_data.set_index("make"))

        st.subheader("Listings by year")
        st.bar_chart(cars["year"].value_counts().sort_index())

elif page == "ML Price Predictor":
    st.title("ML Price Predictor")

    st.info("Model training will be added after we collect cleaned car listings.")

    make = st.text_input("Make", "Toyota")
    model = st.text_input("Model", "Harrier")
    year = st.number_input("Year", min_value=2018, max_value=2026, value=2020)
    mileage = st.number_input("Mileage", min_value=0, value=60000)
    engine_size = st.number_input("Engine size CC", min_value=500, value=2000)

    if st.button("Predict Price"):
        st.warning("No trained model found yet. Train the ML model after scraping data.")
