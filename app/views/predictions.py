from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from app.utils.db_utils import format_kes, load_listings

MODEL_PATH = Path("data/models/car_price_model.pkl")


def load_model():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def render_predictions():
    st.title("🤖 ML Price Predictions")
    st.write("Predict estimated Japan vehicle prices using the trained ML model.")

    df = load_listings()
    artifact = load_model()

    if artifact is None:
        st.warning("No trained ML model found yet.")
        st.code("PYTHONPATH=. uv run python models/train_price_model.py")
        return

    metrics = artifact["metrics"]
    pipeline = artifact["pipeline"]

    st.subheader("Model Performance")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Training Rows", f"{metrics['rows']:,}")
    c2.metric("MAE", format_kes(metrics["mae_kes"]))
    c3.metric("RMSE", format_kes(metrics["rmse_kes"]))
    c4.metric("R²", f"{metrics['r2']:.3f}")

    st.divider()

    if df.empty:
        st.error("No listings available in database.")
        return

    # ----------------------------------------------------------------
    # Dynamic dropdowns from real database data
    # ----------------------------------------------------------------

    makes = sorted(df["make"].dropna().unique().tolist())

    make = st.selectbox("Make", makes)

    filtered_models = (
        df[df["make"] == make]["model"]
        .dropna()
        .sort_values()
        .unique()
        .tolist()
    )

    model = st.selectbox("Model", filtered_models)

    filtered_rows = df[
        (df["make"] == make)
        & (df["model"] == model)
    ]

    default_year = int(filtered_rows["year"].median()) if not filtered_rows.empty else 2021
    default_mileage = int(filtered_rows["mileage"].median()) if not filtered_rows.empty else 50000
    default_engine = int(filtered_rows["engine_size_cc"].median()) if not filtered_rows.empty else 1800

    col1, col2 = st.columns(2)

    with col1:
        year = st.number_input(
            "Year",
            min_value=2015,
            max_value=2026,
            value=default_year,
        )

        mileage = st.number_input(
            "Mileage",
            min_value=0,
            value=default_mileage,
        )

    with col2:
        engine_size = st.number_input(
            "Engine Size CC",
            min_value=500,
            value=default_engine,
        )

        fuels = sorted(df["fuel_type"].dropna().unique().tolist())
        transmissions = sorted(df["transmission"].dropna().unique().tolist())
        body_types = sorted(df["body_type"].dropna().unique().tolist())
        platforms = sorted(df["source_platform"].dropna().unique().tolist())

        fuel = st.selectbox("Fuel", fuels)
        transmission = st.selectbox("Transmission", transmissions)
        body_type = st.selectbox("Body Type", body_types)
        platform = st.selectbox("Platform", platforms)

    if st.button("Predict Price"):

        input_df = pd.DataFrame(
            [
                {
                    "make": make,
                    "model": model,
                    "year": year,
                    "mileage": mileage,
                    "engine_size_cc": engine_size,
                    "fuel_type": fuel,
                    "transmission": transmission,
                    "body_type": body_type,
                    "source_platform": platform,
                }
            ]
        )

        prediction = float(pipeline.predict(input_df)[0])

        lower = prediction * 0.85
        upper = prediction * 1.15

        st.success("Prediction completed successfully.")

        st.metric(
            "Predicted Japan Price",
            format_kes(prediction),
        )

        st.write(
            f"Estimated confidence range: "
            f"**{format_kes(lower)} — {format_kes(upper)}**"
        )

        st.subheader("Prediction Input Summary")

        st.json(input_df.to_dict(orient="records")[0])
