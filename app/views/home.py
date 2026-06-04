import streamlit as st

from app.utils.db_utils import format_kes, load_listings


def render_home():
    df = load_listings()

    st.title("🚗 Japan Car Import Advisory")
    st.markdown(
        "**Compare the true cost of importing used vehicles from Japan against buying locally in Kenya.**"
    )

    st.warning(
        "⚠️ Disclaimer: All cost estimates are indicative only. Consult KRA, a licensed clearing agent, or KEBS before making a purchase decision."
    )

    total = len(df)
    makes = df["make"].nunique() if not df.empty and "make" in df else 0
    models = df["model"].nunique() if not df.empty and "model" in df else 0
    platforms = df["source_platform"].nunique() if not df.empty and "source_platform" in df else 0
    avg_price = df["price_kes"].mean() if not df.empty else 0
    min_price = df["price_kes"].min() if not df.empty else 0
    max_price = df["price_kes"].max() if not df.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Listings", f"{total:,}")
    c2.metric("Makes", f"{makes:,}")
    c3.metric("Models", f"{models:,}")
    c4.metric("Platforms", f"{platforms:,}")

    c5, c6, c7 = st.columns(3)
    c5.metric("Avg Price", format_kes(avg_price))
    c6.metric("Price Range", f"{format_kes(min_price)} - {format_kes(max_price)}")
    c7.metric("Currency", "KES")

    st.divider()

    if df.empty:
        st.info("No cleaned listings found yet. Run the scraper and ETL loader first.")
        return

    st.subheader("Price Distribution by Model")

    chart_df = df.dropna(subset=["model", "price_kes"]).copy()

    # Remove bad numeric model labels such as "100", "30", "40"
    chart_df = chart_df[
        chart_df["model"]
        .astype(str)
        .str.contains(r"[A-Za-z]", regex=True, na=False)
    ]

    chart_df = (
        chart_df.groupby("model", as_index=False)["price_kes"]
        .mean()
        .sort_values("price_kes", ascending=False)
        .head(15)
    )

    st.bar_chart(chart_df.set_index("model"))
