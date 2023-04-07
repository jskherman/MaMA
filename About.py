import streamlit as st

from load import init_page, load_brand

init_page(pg_title="About MaMA", pg_icon="🤗", title="About MaMA")

# Load brand logo and name in sidebar
load_brand()


st.markdown(
    """
    **<abbr title='Malnutrition Monitoring and Assessment System'>MaMA</abbr>**
    or **Ma**lnutrition **M**onitoring and **A**ssessment System is an application
    made by Team NutriBUn for the tracking of various case data of malnutrition
    in the Philippines. This application was originally made in 2022 for the
    first Nutri-Hackathon of the National Nutrition Council of the Philippines.
    """,
    unsafe_allow_html=True,
)
