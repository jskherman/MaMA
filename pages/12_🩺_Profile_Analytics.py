import datetime as dt
import uuid

import polars as pl
import streamlit as st

from load import init_page, load_brand, load_ph_location_data

init_page(
    pg_title="Profile Analytics",
    pg_icon="🩺",
    title="Profile Analytics",
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
region_list.insert(0, "All Regions")

province_list = (
    phlocation_df.select(pl.col("Province").unique().sort())
    .get_column("Province")
    .to_list()
)
province_list.insert(0, "All Provinces")

municity_list = (
    phlocation_df.select(pl.col("Municipality-City").unique().sort())
    .get_column("Municipality-City")
    .to_list()
)
municity_list.insert(0, "All Municipalities/Cities")

brgy_list = (
    phlocation_df.select(pl.col("Barangay").unique().sort())
    .get_column("Barangay")
    .to_list()
)
brgy_list.insert(0, "All Barangays")

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
    filter_prov.insert(0, "All Provinces")

    st.session_state["province_list"] = filter_prov


def on_change_province():
    filter_municity = (
        phlocation_df.filter(pl.col("Province") == st.session_state["in_province"])
        .select(pl.col("Municipality-City").unique().sort())
        .get_column("Municipality-City")
        .to_list()
    )
    filter_municity.insert(0, "All Municipalities/Cities")

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
    filter_brgy.insert(0, "All Barangays")

    st.session_state["brgy_list"] = filter_brgy


if "pl_data" not in st.session_state or "pl_records" not in st.session_state:
    st.warning("Please load test data first.")
elif st.session_state["pl_data"] is None or st.session_state["pl_records"] is None:
    st.warning("Please load test data first.")
else:
    patient_data = st.session_state["pl_data"]
    patient_records = st.session_state["pl_records"]

if "profile_data" not in st.session_state:
    st.session_state["profile_data"] = False
if "filtered_patient_data" not in st.session_state:
    st.session_state["filtered_patient_data"] = patient_data
if "show_data" not in st.session_state:
    st.session_state["show_data"] = patient_data.to_pandas()
if "patient_names" not in st.session_state:
    st.session_state["patient_names"] = ""

global profile_data
global filtered_patient_data
global show_data_df
global patient_names


def search_profile(patient_data, data_filter):
    filtered_patient_data = patient_data

    if patient_first_name != "":
        filtered_patient_data = filtered_patient_data.filter(
            pl.col("First Name") == data_filter["First Name"]
        )

    if patient_middle_name != "":
        filtered_patient_data = filtered_patient_data.filter(
            pl.col("Middle Name") == data_filter["Middle Name"]
        )

    if patient_last_name != "":
        filtered_patient_data = filtered_patient_data.filter(
            pl.col("Last Name") == data_filter["Last Name"]
        )

    if patient_suffix != "":
        filtered_patient_data = filtered_patient_data.filter(
            pl.col("Suffix") == data_filter["Suffix"]
        )

    if patient_sex != "" or patient_sex != "M/F":
        filtered_patient_data = filtered_patient_data.filter(
            pl.col("Sex") == data_filter["Sex"]
        )

    if patient_region != "" or patient_region != "All Regions":
        filtered_patient_data = filtered_patient_data.filter(
            pl.col("Region") == data_filter["Region"]
        )

    if patient_province != "" or patient_province != "All Provinces":
        filtered_patient_data = filtered_patient_data.filter(
            pl.col("Province") == data_filter["Province"]
        )

    if (
        patient_municity is not None
        or patient_municity != ""
        or patient_municity != "All Municipalities/Cities"
    ):
        filtered_patient_data = filtered_patient_data.filter(
            pl.col("Municipality/City") == data_filter["Municipality/City"]
        )

    if (
        patient_brgy is not None
        or patient_brgy != ""
        or patient_brgy != "All Barangays"
    ):
        filtered_patient_data = filtered_patient_data.filter(
            pl.col("Barangay") == data_filter["Barangay"]
        )

    if filtered_patient_data.height == 0:
        st.session_state["profile_data"] = False
    else:
        st.session_state["profile_data"] = True

        st.session_state["filtered_patient_data"] = filtered_patient_data
        show_data_df = filtered_patient_data.select(
            [
                "First Name",
                "Middle Name",
                "Last Name",
                "Suffix",
                "Sex",
                "Region",
                "Province",
                "Municipality/City",
                "Barangay",
            ]
        )
        st.session_state["show_data"] = show_data_df.to_pandas()

        patient_names_df = filtered_patient_data.select(
            ["First Name", "Middle Name", "Last Name", "Suffix"]
        )
        patient_names_df = patient_names_df.with_columns(
            [
                pl.col("First Name").apply(
                    lambda x: " ".join([w.capitalize() for w in x.split()])
                ),
                pl.col("Middle Name").apply(
                    lambda x: " ".join([w.capitalize() for w in x.split()])
                ),
                pl.col("Last Name").apply(
                    lambda x: " ".join([w.capitalize() for w in x.split()])
                ),
                pl.col("Suffix").str.to_uppercase(),
            ]
        )
        patient_names_df = patient_names_df.select(
            [
                pl.col("First Name")
                + " "
                + pl.col("Middle Name")
                + " "
                + pl.col("Last Name")
                + " "
                + pl.col("Suffix")
            ]
        )
        patient_names = (
            patient_names_df.get_column("First Name").alias("Full Name").to_list()
        )

        st.session_state["patient_names"] = patient_names


# Step 2: Filter data for specific patient

with st.form(key="search"):
    c1r1, c2r1 = st.columns(2)

    with c1r1:
        # Patient First Name
        patient_first_name = st.text_input(
            label="First Name*",
            value="",
            key="first_name",
            help="Enter first name.",
            max_chars=40,
            placeholder="Example: Juan",
        )
        patient_first_name = patient_first_name.strip().lower()

        # Patient Last Name
        patient_last_name = st.text_input(
            label="Last Name*",
            value="",
            key="last_name",
            help="Enter last name.",
            max_chars=40,
            placeholder="Example: Dela Cruz",
        )
        patient_last_name = patient_last_name.strip().lower()

        patient_sex = st.selectbox(
            label="Sex (M/F)*",
            options=["M/F", "M", "F"],
            index=0,
            help="Enter sex: Male (M) / Female (F)",
        )

    with c2r1:
        # Patient Middle Name
        patient_middle_name = st.text_input(
            label="Middle Name",
            value="",
            key="middle_name",
            help="Enter middle name. Leave blank if none.",
            max_chars=40,
            placeholder="Example: De la Peña",
        )
        patient_middle_name = patient_middle_name.strip().lower()

        # Patient Name Suffix
        patient_suffix = st.text_input(
            label="Suffix (Optional)",
            value="",
            key="suffix",
            help="Enter name's suffix. Leave blank if none.",
            max_chars=8,
            placeholder="Example: Jr., III, IX, LXXXVIII, etc.",
        )
        patient_suffix = patient_suffix.strip().lower()

    patient_region = st.selectbox(
        label="Region*",
        options=region_list,
        help="Select your region.",
        key="in_region",
        index=0,
        on_change=on_change_region,
    )

    if patient_province not in st.session_state["province_list"]:
        patient_province = st.session_state["province_list"][0]

        patient_province = st.selectbox(
            label="Province*",
            options=st.session_state["province_list"],
            help="Select your province.",
            key="in_province",
            index=0,
            on_change=on_change_province,
        )
    else:
        patient_province = st.selectbox(
            label="Province*",
            options=st.session_state["province_list"],
            help="Select your province.",
            key="in_province",
            index=0,
            on_change=on_change_province,
        )

    if patient_municity not in st.session_state["municity_list"]:
        patient_municity = st.session_state["municity_list"][0]

        patient_municity = st.selectbox(
            label="Municipality/City*",
            options=st.session_state["municity_list"],
            help="Select your municipality/city.",
            key="in_municity",
            index=0,
            on_change=on_change_municity,
        )
    else:
        patient_municity = st.selectbox(
            label="Municipality/City*",
            options=st.session_state["municity_list"],
            help="Select your municipality/city.",
            key="in_municity",
            index=0,
            on_change=on_change_municity,
        )

    if patient_brgy not in st.session_state["brgy_list"]:
        patient_brgy = st.session_state["brgy_list"][0]
        patient_brgy = st.selectbox(
            label="Barangay*",
            options=st.session_state["brgy_list"],
            help="Select your barangay.",
            key="in_brgy",
            index=0,
        )
    else:
        patient_brgy = st.selectbox(
            label="Barangay*",
            options=st.session_state["brgy_list"],
            help="Select your barangay.",
            key="in_brgy",
            index=0,
        )

    data_filter = {
        "First Name": patient_first_name,
        "Middle Name": patient_middle_name,
        "Last Name": patient_last_name,
        "Suffix": patient_suffix,
        "Sex": patient_sex,
        "Region": patient_region,
        "Province": patient_province,
        "Municipality/City": patient_municity,
        "Barangay": patient_brgy,
    }

    submitted = st.form_submit_button(
        "Search",
        type="primary",
        on_click=search_profile,
        args=(patient_data, data_filter),
    )

    if submitted:
        st.session_state["submitted"] = True


if st.session_state["profile_data"]:
    st.dataframe(st.session_state["show_data"])
