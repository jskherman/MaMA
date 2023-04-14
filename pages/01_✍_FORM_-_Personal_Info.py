import uuid

import streamlit as st

from load import init_page, load_brand

init_page(
    pg_title="Form: Personal Info", pg_icon="✍", title="Form: Personal Information"
)

# Load brand logo and name in sidebar
load_brand()

# Create a form for new Patient
pif = st.form(key="personal_info")

with pif:
    # Generate UUID version 4 for Patient ID
    patient_uuid = uuid.uuid4()

    # Patient First Name
    patient_first_name = pif.text_input(label="First Name", value="")

    # Change to lowercase and remove leading and trailing spaces
    patient_first_name = patient_first_name.lower().strip()

    # Check if first name is empty
    if len(patient_first_name) == 0:
        pif.error("Please enter a valid first name.")
