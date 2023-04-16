import datetime as dt
import uuid

import polars as pl
import streamlit as st

from load import count_alnum_chars, init_page, load_brand, load_ph_location_data

init_page(
    pg_title="Form: Personal Info",
    pg_icon="✍",
    title="Form: Personal Information",
    # layout="centered",
)

# Load brand logo and name in sidebar
load_brand()

# Create lists of regions, provinces, municipalities, and barangays
if "phlocation_df" not in st.session_state:
    st.session_state["phlocation_df"] = load_ph_location_data()

phlocation_df = st.session_state["phlocation_df"]

region_list = (
    phlocation_df.select(pl.col("Region").unique().sort())
    .get_column("Region")
    .to_list()
)

province_list = (
    phlocation_df.select(pl.col("Province").unique().sort())
    .get_column("Province")
    .to_list()
)

municity_list = (
    phlocation_df.select(pl.col("Municipality-City").unique().sort())
    .get_column("Municipality-City")
    .to_list()
)

brgy_list = (
    phlocation_df.select(pl.col("Barangay").unique().sort())
    .get_column("Barangay")
    .to_list()
)

patient_province = ""
patient_municity = ""
patient_brgy = ""

if "in_region" not in st.session_state:
    st.session_state["in_region"] = region_list[0]
if "in_province" not in st.session_state:
    st.session_state["in_province"] = province_list[0]
if "in_municity" not in st.session_state:
    st.session_state["in_municity"] = municity_list[0]
if "in_brgy" not in st.session_state:
    st.session_state["in_brgy"] = brgy_list[0]
if "province_list" not in st.session_state:
    st.session_state["province_list"] = province_list
if "municity_list" not in st.session_state:
    st.session_state["municity_list"] = municity_list
if "brgy_list" not in st.session_state:
    st.session_state["brgy_list"] = brgy_list


def on_change_region():
    filter_prov = (
        phlocation_df.filter(pl.col("Region") == st.session_state["in_region"])
        .select(pl.col("Province").unique().sort())
        .get_column("Province")
        .to_list()
    )

    st.session_state["province_list"] = filter_prov


def on_change_province():
    filter_municity = (
        phlocation_df.filter(pl.col("Province") == st.session_state["in_province"])
        .select(pl.col("Municipality-City").unique().sort())
        .get_column("Municipality-City")
        .to_list()
    )

    st.session_state["municity_list"] = filter_municity


def on_change_municity():
    filter_brgy = (
        phlocation_df.filter(
            pl.col("Municipality-City") == st.session_state["in_municity"]
        )
        .select(pl.col("Barangay").unique().sort())
        .get_column("Barangay")
        .to_list()
    )

    st.session_state["brgy_list"] = filter_brgy


# Create a form for new Patient
pif = st.form(key="personal_info")

# with pif:
# Generate UUID version 4 for Patient ID
patient_uuid = str(uuid.uuid4())

# Create note that * indicates required field
st.markdown(
    """
    **<kbd>*</kbd> Indicates a required field.</span>**
    """,
    unsafe_allow_html=True,
)

c1r1, c2r1 = st.columns(2)

with c1r1:
    # Patient First Name
    patient_first_name = st.text_input(
        label="First Name*",
        value="",
        key="first_name",
        help="Enter your first name.",
        max_chars=40,
        placeholder="Example: Juan",
    )

    # Patient Last Name
    patient_last_name = st.text_input(
        label="Last Name*",
        value="",
        key="last_name",
        help="Enter your last name.",
        max_chars=40,
        placeholder="Example: Dela Cruz",
    )

    patient_birthdate = st.date_input(
        label="Birthdate*",
        value=dt.datetime.today(),
        key="birthdate",
        help="Enter your birthdate.",
        min_value=dt.datetime(2010, 1, 1),
    )

with c2r1:
    # Patient Middle Name
    patient_middle_name = st.text_input(
        label="Middle Name",
        value="",
        key="middle_name",
        help="Enter your middle name. Leave blank if none.",
        max_chars=40,
        placeholder="Example: De la Peña",
    )

    # Patient Name Suffix
    patient_suffix = st.text_input(
        label="Suffix (Optional)",
        value="",
        key="suffix",
        help="Enter your name's suffix. Leave blank if none.",
        max_chars=8,
        placeholder="Example: Jr., III, IX, LXXXVIII, etc.",
    )

    patient_sex = st.selectbox(
        label="Sex (M/F)*",
        options=["M", "F"],
        index=0,
        help="Enter your sex: Male (M) / Female (F)",
    )

# Patient Address
patient_region = st.selectbox(
    label="Region*",
    options=region_list,
    help="Select your region.",
    key="in_region",
    on_change=on_change_region,
)

if patient_province not in st.session_state["province_list"]:
    patient_province = st.session_state["province_list"][0]

    patient_province = st.selectbox(
        label="Province*",
        options=st.session_state["province_list"],
        help="Select your province.",
        key="in_province",
        on_change=on_change_province,
    )
else:
    patient_province = st.selectbox(
        label="Province*",
        options=st.session_state["province_list"],
        help="Select your province.",
        key="in_province",
        on_change=on_change_province,
    )

if patient_municity not in st.session_state["municity_list"]:
    patient_municity = st.session_state["municity_list"][0]

    patient_municity = st.selectbox(
        label="Municipality/City*",
        options=st.session_state["municity_list"],
        help="Select your municipality/city.",
        key="in_municity",
        on_change=on_change_municity,
    )
else:
    patient_municity = st.selectbox(
        label="Municipality/City*",
        options=st.session_state["municity_list"],
        help="Select your municipality/city.",
        key="in_municity",
        on_change=on_change_municity,
    )

if patient_brgy not in st.session_state["brgy_list"]:
    patient_brgy = st.session_state["brgy_list"][0]
    patient_brgy = st.selectbox(
        label="Barangay*",
        options=st.session_state["brgy_list"],
        help="Select your barangay.",
        key="in_brgy",
    )
else:
    patient_brgy = st.selectbox(
        label="Barangay*",
        options=st.session_state["brgy_list"],
        help="Select your barangay.",
        key="in_brgy",
    )

# Form submit button
if st.button(label="Submit", type="primary"):
    # Check if all required fields are filled
    if not patient_first_name or not patient_last_name:
        st.error("Please fill out all required fields.")
    elif count_alnum_chars(patient_first_name) <= 0:
        st.error("Please enter a valid first name.")
    elif count_alnum_chars(patient_last_name) <= 0:
        st.error("Please enter a valid last name.")
    else:
        patient_data = {
            "ID": patient_uuid,
            "First Name": patient_first_name.lower().strip(),
            "Middle Name": patient_middle_name.lower().strip(),
            "Last Name": patient_last_name.lower().strip(),
            "Suffix": patient_suffix.lower().strip(),
            "Birthdate": patient_birthdate,
            "Sex": patient_sex,
            "Region": patient_region,
            "Province": patient_province,
            "Municipality/City": patient_municity,
            "Barangay": patient_brgy,
        }

        patient_data_df = pl.DataFrame(patient_data)
        test_data_df = st.session_state["pl_data"]

        st.session_state["pl_data"] = pl.concat([test_data_df, patient_data_df])

        # Show success message
        st.success("🎉 Profile submitted successfully.")
        st.balloons()

        # Clear form
        patient_first_name = ""
        patient_middle_name = ""
        patient_last_name = ""
        patient_suffix = ""
        patient_birthdate = dt.datetime.today()
        patient_sex = "M"
