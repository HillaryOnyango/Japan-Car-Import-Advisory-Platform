import streamlit as st

from app.utils.db_utils import format_kes


def render_predictions():
    st.title("🤖 ML Price Predictions")
    st.write("Predict fair Japan vehicle price based on listing features.")

    make = st.text_input("Make", "Toyota")
    model = st.text_input("Model", "Corolla")
    year = st.number_input("Year", min_value=2015, max_value=2026, value=2021)
    mileage = st.number_input("Mileage", min_value=0, value=50000)
    engine_size = st.number_input("Engine Size CC", min_value=500, value=1800)
    fuel = st.selectbox("Fuel", ["Petrol", "Diesel", "Hybrid", "Electric"])
    transmission = st.selectbox("Transmission", ["Automatic", "Manual", "AT", "MT"])
    platform = st.selectbox("Platform", ["BE FORWARD", "SBT Japan"])

    if st.button("Predict Price"):
        st.warning("Model training will be connected after the ML pipeline is implemented.")

        estimated_kes = 1_800_000
        st.metric("Estimated Fair Price", format_kes(estimated_kes))
