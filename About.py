import pandas as pd
import polars as pl
import streamlit as st

from load import init_page, load_brand, load_testdata

init_page(pg_title="About MaMA", pg_icon="🤗", title="About MaMA")

# Load brand logo and name in sidebar
load_brand()


st.markdown(
    """
    **<abbr title='Malnutrition Monitoring and Assessment System'>MaMA</abbr>**
    or **Ma**lnutrition **M**onitoring and **A**ssessment System is an application
    made by Team NutriBUn for the tracking of various case data of malnutrition
    in the Philippines. This application was originally made in 2022 for the
    first Nutri-Hackathon of the National Nutrition Council of the Philippines
    but now revised and reinvisioned this time around.
    """,
    unsafe_allow_html=True,
)

# Step 1: Load test data

st.markdown("## Step 1: Load Test Data")
if st.button("Load Test Data"):
    st.markdown(
        """- You can click inside of the table and press
                <kbd>Ctrl</kbd>+<kbd>F</kbd> in Windows or
                <kbd>⌘ Cmd</kbd>+<kbd>F</kbd> in Mac to search the data.\n- You
                can also select cells and copy them to your clipboard with
                <kbd>Ctrl</kbd>+<kbd>C</kbd> in Windows or
                <kbd>⌘ Cmd</kbd>+<kbd>C</kbd> in Mac.""",
        unsafe_allow_html=True,
    )
    st.session_state["pl_data"] = load_testdata(30)
    st.session_state["pd_data"] = st.session_state["pl_data"].to_pandas()
    st.write(st.session_state["pd_data"])
