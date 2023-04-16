import streamlit as st

from load import init_page, load_brand

init_page(pg_title="Form: Measures", pg_icon="📝", title="Form: Measurements")

# Load brand logo and name in sidebar
load_brand()

st.dataframe(st.session_state["pl_data"])
