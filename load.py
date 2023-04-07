import streamlit as st


def init_page(pg_title, pg_icon="🍖", title=None, layout="wide"):
    """
    Initialize a streamlit page with a title, icon, and CSS styles.
    """
    st.set_page_config(
        page_title=pg_title,
        page_icon=pg_icon,
        layout=layout,
    )

    # Load CSS styles
    if "css" not in st.session_state:
        st.session_state["css"] = open("assets/css/style.css").read()
    st.markdown(f"<style>{st.session_state['css']}\n</style>", unsafe_allow_html=True)

    if title:
        st.title(title)


def load_brand():
    """
    Load the brand logo and name.
    """

    with st.sidebar:
        st.image("assets/img/logo.png")

        st.markdown(
            """
            <center><strong>Ma</strong>lnutrition&nbsp;<strong>M</strong>onitoring and&nbsp;<strong>A</strong>ssessment&nbsp;System</center>

            <br><br> Project by Team NutriBUn &copy;&nbsp;2022–2023
            """,
            unsafe_allow_html=True,
        )
