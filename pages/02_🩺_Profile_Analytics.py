import datetime as dt
import uuid

import pandas as pd
import plotly.express as px
import polars as pl
import streamlit as st

from load import classify_malnutrition, init_page, load_brand, load_ph_location_data

init_page(
    pg_title="MaMA - Profile Analytics",
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
if "select_pdf" not in st.session_state:
    st.session_state["select_pdf"] = pl.DataFrame([{}])
if "profile_found" not in st.session_state:
    st.session_state["profile_found"] = False
# global profile_data
# global filtered_patient_data
# global show_data_df
# global patient_names

# profile_found = False
filtered_patient_data = patient_data
# show_data_df = patient_data.to_pandas()
# patient_names = []
# filtered_patient_data = patient_data

# def search_profile(patient_data, data_filter):

# Step 2: Filter data for specific patient
with st.expander("Search Profile", expanded=True):
    st.info("Press enter for the text input to take effect.", icon="ℹ")

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

    submitted = st.button(
        "Search",
        type="primary",
        # on_click=search_profile,
        # args=(patient_data, data_filter),
    )

    if submitted:
        filtered_patient_data = patient_data

        if patient_first_name != "":
            filtered_patient_data = filtered_patient_data.filter(
                pl.col("First Name") == patient_first_name
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

        if patient_sex != "" and patient_sex != "M/F":
            filtered_patient_data = filtered_patient_data.filter(
                pl.col("Sex") == data_filter["Sex"]
            )

        if patient_region != "All Regions":
            filtered_patient_data = filtered_patient_data.filter(
                pl.col("Region") == data_filter["Region"]
            )

        if patient_province != "All Provinces":
            filtered_patient_data = filtered_patient_data.filter(
                pl.col("Province") == data_filter["Province"]
            )

        if patient_municity != "All Municipalities/Cities":
            filtered_patient_data = filtered_patient_data.filter(
                pl.col("Municipality/City") == data_filter["Municipality/City"]
            )

        if patient_brgy != "All Barangays":
            filtered_patient_data = filtered_patient_data.filter(
                pl.col("Barangay") == data_filter["Barangay"]
            )

        st.session_state["filtered_patient_data"] = filtered_patient_data

    "---"

    if st.session_state["filtered_patient_data"].height == 0:
        st.error("Error: No data found.")
        profile_found = False
    elif st.session_state["filtered_patient_data"].height == patient_data.height:
        st.info("No filter applied. Please apply one.")
        profile_found = False
        st.session_state["profile_found"] = profile_found
    else:
        filter_df = st.session_state["filtered_patient_data"]
        if filter_df.height == 1:
            st.success("Profile found!")
            profile_found = True
            st.session_state["profile_found"] = profile_found
            pid = filter_df["ID"][0]
            st.session_state["pid"] = pid
        else:
            st.error("Error: Please narrow down your search to only one result.")
            profile_found = False
            st.session_state["profile_found"] = profile_found

        st.dataframe(filter_df.to_pandas().drop(columns=["ID"]))


if st.session_state["profile_found"]:
    pid = st.session_state["pid"]
    pdata = patient_data.filter(pl.col("ID") == pid)
    fname = pdata["First Name"][0]
    mname = pdata["Middle Name"][0]
    lname = pdata["Last Name"][0]
    psuffix = pdata["Suffix"][0]

    psex = pdata["Sex"][0]
    pbirthdate = dt.date.fromisoformat(pdata["Birthdate"][0])

    pregion = pdata["Region"][0]
    pprovince = pdata["Province"][0]
    pmunicity = pdata["Municipality/City"][0]
    pbrgy = pdata["Barangay"][0]

    precords = patient_records.filter(pl.col("PID") == pid).sort(
        "Timestamp", descending=True
    )
    precords = precords.with_columns(
        pl.struct(["Alive", "Default", "Edema", "MUAC (cm)", "Z-score"])
        .map_elements(
            lambda cols: classify_malnutrition(
                cols["Alive"],
                cols["Default"],
                cols["Edema"],
                cols["MUAC (cm)"],
                cols["Z-score"],
            )
        )
        .alias("Malnutrition Status")
    )
    recent_record = precords[0]
    if len(precords) > 1:
        last_record = precords[1]
    else:
        last_record = precords[0]
    recent_record_date = dt.date.fromisoformat(recent_record["Timestamp"][0])
    current_age = round((recent_record_date - pbirthdate).days * 12 / 365.25)
    current_weight = recent_record["Weight (kg)"][0]
    current_height = recent_record["Height (cm)"][0]
    current_muac = recent_record["MUAC (cm)"][0]
    status_alive = recent_record["Alive"][0]
    status_default = recent_record["Default"][0]
    status_edema = recent_record["Edema"][0]
    status_nutrition = recent_record["Malnutrition Status"][0]

    st.header(f"{fname.capitalize()}'s Profile")

    # r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    # r1c1.metric(label="First Name", value=fname.capitalize())
    # r1c2.metric(label="Middle Name", value=mname.capitalize())
    # r1c3.metric(label="Last Name", value=lname.capitalize())
    # r1c4.metric(label="Suffix", value=psuffix.upper())

    r1c1, r1c2, r1c3 = st.columns([1, 2, 1])

    with r1c1:
        st.write("### Name")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "First Name": fname.capitalize(),
                        "Middle Name": mname.capitalize(),
                        "Last Name": lname.capitalize(),
                        "Suffix": psuffix.upper(),
                    }
                ]
            )
            .transpose()
            .rename(columns={0: "Data"})
        )

    with r1c2:
        st.write("### Location")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Region": pregion,
                        "Province": pprovince,
                        "Municipality/City": pmunicity,
                        "Barangay": pbrgy,
                    }
                ]
            )
            .transpose()
            .rename(columns={0: "Data"})
        )

    with r1c3:
        st.markdown("### Sex and Age")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Sex": "Male" if psex == "M" else "Female",
                        "Birthdate": pbirthdate.strftime("%B %d, %Y"),
                        "Age (months)": current_age,
                        "Age (years)": round(current_age / 12, 2),
                    }
                ]
            )
            .transpose()
            .rename(columns={0: "Data"})
        )

    st.markdown(
        f"## Recent Record: <span style='color:crimson;white-space:nowrap;'><u>{recent_record_date.strftime('%B %d, %Y')}</u></span>",
        unsafe_allow_html=True,
    )

    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    r2c1.metric(label="Alive", value=("YES" if status_alive else "NO"))
    r2c2.metric(label="Default", value=("YES" if status_default else "NO"))
    r2c3.metric(label="Edema", value=("YES" if status_edema else "NO"))
    r2c4.metric(
        label="Malnutrition Status",
        value=(
            status_nutrition
            if status_nutrition != "DEAD" and status_nutrition != "DEFAULT"
            else "—"
        ),
    )

    if status_alive and not status_default:
        r3c1, r3c2, r3c3, r3c4 = st.columns(4)
        r3c1.metric(
            label="Weight (kg)",
            value=current_weight,
            delta=round(current_weight - last_record["Weight (kg)"][0], 2),
        )
        r3c2.metric(
            label="Height (cm)",
            value=current_height,
            delta=round(current_height - last_record["Height (cm)"][0], 2),
        )
        r3c3.metric(
            label="MUAC (cm)",
            value=current_muac,
            delta=round(current_muac - last_record["MUAC (cm)"][0], 2),
        )
        r3c4.metric(
            label="Z-score",
            value=round(recent_record["Z-score"][0], 2),
            delta=round(recent_record["Z-score"][0] - last_record["Z-score"][0], 2),
        )

    show_records = precords.drop(
        [
            "ID",
            "PID",
            "Sex",
            "Region",
            "Province",
            "Municipality/City",
            "Barangay",
        ]
    ).to_pandas()

    st.header(f"{fname.capitalize()}'s Graph")
    graph_choice = st.selectbox(
        label="Select a graph to view",
        options=[
            "Weight (kg)",
            "Height (cm)",
            "MUAC (cm)",
            "Edema",
            "Malnutrition Status",
        ],
        index=0,
    )

    if graph_choice == "Edema":
        graph_df = show_records[["Timestamp", graph_choice]]
        graph_df[graph_choice] = graph_df[graph_choice].apply(
            lambda x: "YES" if x else "NO"
        )

    else:
        graph_df = show_records[["Timestamp", graph_choice]]

    fig1 = px.bar(
        graph_df,
        x="Timestamp",
        y=graph_choice,
        color=graph_choice,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title=f"{fname.capitalize()}'s {graph_choice} over time",
        color_continuous_scale="rdylgn",
    )
    if graph_choice == "Edema":
        fig1.update_yaxes(autorange="reversed")

    st.plotly_chart(fig1, use_container_width=True)

    with st.expander("Show All Records"):
        csv_records = show_records.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"Download {fname.capitalize()}'s Records (CSV/Excel)",
            data=csv_records,
            file_name=f"{lname.upper().replace(' ', '_')}_{dt.date.today().strftime('%Y-%m-%d')}.csv",
            mime="text/csv",
        )

        st.dataframe(show_records)
