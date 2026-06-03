import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from app.views.home import render_home
from app.views.search import render_search
from app.views.calculator import render_calculator
from app.views.comparisons import render_comparisons
from app.views.predictions import render_predictions


st.set_page_config(
    page_title="Japan Car Import Advisory",
    page_icon="🚗",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select page",
    [
        "🏠 Overview",
        "🔍 Browse Listings",
        "🧮 Import Calculator",
        "📊 Import vs Local",
        "🤖 ML Predictions",
    ],
)

st.sidebar.divider()
st.sidebar.markdown("### Japan Car Import Advisory")
st.sidebar.write("Educational data engineering and ML platform for Kenyan car buyers.")
st.sidebar.caption("⚠️ For educational purposes only. Not financial advice.")

if page == "🏠 Overview":
    render_home()
elif page == "🔍 Browse Listings":
    render_search()
elif page == "🧮 Import Calculator":
    render_calculator()
elif page == "📊 Import vs Local":
    render_comparisons()
elif page == "🤖 ML Predictions":
    render_predictions()