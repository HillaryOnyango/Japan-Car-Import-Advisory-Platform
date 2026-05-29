import streamlit as st

from app.utils.db_utils import format_kes, load_listings


def render_comparisons():
    st.title("📊 Import vs Local Comparison")
    st.write("Compare estimated import prices with local Kenyan market prices.")

    df = load_listings()

    if df.empty:
        st.info("No listings available yet.")
        return

    make = st.selectbox("Select Make", sorted(df["make"].dropna().unique()))
    model_df = df[df["make"] == make]

    model = st.selectbox("Select Model", sorted(model_df["model"].dropna().unique()))
    selected = model_df[model_df["model"] == model]

    avg_import_price = selected["price_kes"].mean()

    local_price = st.number_input("Estimated Local Market Price (KES)", value=float(avg_import_price * 1.25))

    savings = local_price - avg_import_price

    c1, c2, c3 = st.columns(3)
    c1.metric("Avg Japan Listing Price", format_kes(avg_import_price))
    c2.metric("Local Market Price", format_kes(local_price))
    c3.metric("Potential Difference", format_kes(savings))
