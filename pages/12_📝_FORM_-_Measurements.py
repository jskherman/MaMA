import datetime as dt
import random
import uuid

import polars as pl
import streamlit as st

from load import count_alnum_chars, init_page, load_brand, load_ph_location_data

init_page(pg_title="MaMA - Form: Measurements", pg_icon="📝", title="Form: Measurements")

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
u_province = ""
u_municity = ""
u_brgy = ""

if "in_region" not in st.session_state:
    st.session_state["in_region"] = region_list[0]
if "in_province" not in st.session_state:
    st.session_state["in_province"] = province_list[0]
if "in_municity" not in st.session_state:
    st.session_state["in_municity"] = municity_list[0]
if "in_brgy" not in st.session_state:
    st.session_state["in_brgy"] = brgy_list[0]
if "u_region" not in st.session_state:
    st.session_state["u_region"] = region_list[0]
if "u_province" not in st.session_state:
    st.session_state["u_province"] = province_list[0]
if "u_municity" not in st.session_state:
    st.session_state["u_municity"] = municity_list[0]
if "u_brgy" not in st.session_state:
    st.session_state["in_brgy"] = brgy_list[0]
if "province_list" not in st.session_state:
    st.session_state["province_list"] = province_list
if "municity_list" not in st.session_state:
    st.session_state["municity_list"] = municity_list
if "brgy_list" not in st.session_state:
    st.session_state["brgy_list"] = brgy_list
if "uprovince_list" not in st.session_state:
    st.session_state["uprovince_list"] = province_list
if "umunicity_list" not in st.session_state:
    st.session_state["umunicity_list"] = municity_list
if "ubrgy_list" not in st.session_state:
    st.session_state["ubrgy_list"] = brgy_list


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


def update_region():
    filter_prov = (
        phlocation_df.filter(pl.col("Region") == st.session_state["u_region"])
        .select(pl.col("Province").unique().sort())
        .get_column("Province")
        .to_list()
    )
    filter_prov.insert(0, "All Provinces")

    st.session_state["uprovince_list"] = filter_prov


def update_province():
    filter_municity = (
        phlocation_df.filter(pl.col("Province") == st.session_state["u_province"])
        .select(pl.col("Municipality-City").unique().sort())
        .get_column("Municipality-City")
        .to_list()
    )
    filter_municity.insert(0, "All Municipalities/Cities")

    st.session_state["umunicity_list"] = filter_municity


def update_municity():
    filter_brgy = (
        phlocation_df.filter(
            pl.col("Municipality-City") == st.session_state["u_municity"]
        )
        .select(pl.col("Barangay").unique().sort())
        .get_column("Barangay")
        .to_list()
    )
    filter_brgy.insert(0, "All Barangays")

    st.session_state["ubrgy_list"] = filter_brgy


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

filtered_patient_data = patient_data

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
    precords = patient_records.filter(pl.col("PID") == pid).sort(
        "Timestamp", descending=True
    )

    st.write(
        f"## Selected&nbsp;Profile: `{pdata['First Name'][0].upper()} {pdata['Middle Name'][0].upper()} {pdata['Last Name'][0].upper()} {pdata['Suffix'][0].upper()}`"
    )

    st.write("Profile's Personal Information:")
    st.dataframe(pdata.to_pandas().drop(columns=["ID"]))

    # st.write("Profile's Records:")
    # st.dataframe(
    #     precords.to_pandas().drop(
    #         columns=[
    #             "ID",
    #             "PID",
    #             "Sex",
    #             "Region",
    #             "Province",
    #             "Municipality/City",
    #             "Barangay",
    #         ]
    #     )
    # )

    "---"

    measure_form = st.form(key="measure_form")

    with measure_form:
        st.write("## Consultation Form")

        insert_uuid = str(uuid.uuid4())
        insert_zscore = round(random.uniform(-3.5, 3.5), 2)

        f1c1, f1c2 = st.columns(2)

        with f1c1:
            insert_date = st.date_input(
                "Date of Consultation*",
                value=dt.date.today(),
                min_value=dt.date(2000, 1, 1),
                max_value=dt.date.today(),
                help="Select the date of consultation.",
            )

            insert_alive = st.checkbox(
                f"Is {pdata['First Name'][0].title()} **alive**?",
                value=True,
                help="Check if the person is alive.",
            )

            insert_default = st.checkbox(
                f"Did {pdata['First Name'][0].title()} **default** on consultations?",
                value=False,
                help="Check if the person defaulted on consultations.",
            )

            insert_edema = st.checkbox(
                f"Does {pdata['First Name'][0].title()} have **edema**?",
                value=False,
                help="Check if the person has edema.",
            )

        with f1c2:
            insert_weight = st.number_input(
                "Weight (kg)*",
                value=0.0,
                min_value=0.0,
                max_value=500.0,
                step=0.1,
                help="Enter the person's weight in kilograms.",
            )

            insert_height = st.number_input(
                "Height (cm)*",
                value=0.0,
                min_value=0.0,
                max_value=300.0,
                step=0.1,
                help="Enter the person's height in centimeters.",
            )

            insert_muac = st.number_input(
                "MUAC (cm)*",
                value=0.0,
                min_value=0.0,
                max_value=50.0,
                step=0.1,
                help="Enter the person's mid-upper arm circumference (MUAC) in centimeters.",
            )

        pbirthdate = dt.date.fromisoformat(pdata["Birthdate"][0])
        insert_age = round((insert_date - pbirthdate).days * 12 / 365.25)

        measure_submit = st.form_submit_button("Submit", type="primary")

        if measure_submit:
            # Check if all required fields are filled
            if insert_date and insert_weight and insert_height and insert_muac:
                insert_data = {
                    "ID": insert_uuid,
                    "PID": pid,
                    "Sex": pdata["Sex"][0],
                    "Timestamp": insert_date.isoformat(),
                    "Month_Age": insert_age,
                    "Region": pdata["Region"][0],
                    "Province": pdata["Province"][0],
                    "Municipality/City": pdata["Municipality/City"][0],
                    "Barangay": pdata["Barangay"][0],
                    "Z-score": insert_zscore,
                    "Weight (kg)": insert_weight,
                    "Height (cm)": insert_height,
                    "MUAC (cm)": insert_muac,
                    "Default": insert_default,
                    "Alive": insert_alive,
                    "Edema": insert_edema,
                }

                insert_data_df = pl.DataFrame(insert_data)
                patient_records = st.session_state["pl_records"]
                patient_records = pl.concat([patient_records, insert_data_df])
                st.session_state["pl_records"] = patient_records

                st.session_state["patient_records"] = patient_records

                st.success("Record successfully added!")

    "---"

    st.write("## Update Profile Form")

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
        u_first_name = st.text_input(
            label="First Name*",
            value=pdata["First Name"][0].title(),
            key="ufirst_name",
            help="Enter your first name.",
            max_chars=40,
            placeholder="Example: Juan",
        )

        # Patient Last Name
        u_last_name = st.text_input(
            label="Last Name*",
            value=pdata["Last Name"][0].title(),
            key="ulast_name",
            help="Enter your last name.",
            max_chars=40,
            placeholder="Example: Dela Cruz",
        )

        u_birthdate = st.date_input(
            label="Birthdate*",
            value=dt.date.fromisoformat(pdata["Birthdate"][0]),
            key="ubirthdate",
            help="Enter your birthdate.",
            min_value=dt.datetime(2010, 1, 1),
        )

    with c2r1:
        # Patient Middle Name
        u_middle_name = st.text_input(
            label="Middle Name",
            value=pdata["Middle Name"][0].title(),
            key="umiddle_name",
            help="Enter your middle name. Leave blank if none.",
            max_chars=40,
            placeholder="Example: De la Peña",
        )

        # Patient Name Suffix
        u_suffix = st.text_input(
            label="Suffix (Optional)",
            value=pdata["Suffix"][0].upper(),
            key="usuffix",
            help="Enter your name's suffix. Leave blank if none.",
            max_chars=8,
            placeholder="Example: Jr., III, IX, LXXXVIII, etc.",
        )

        u_sex = st.selectbox(
            label="Sex (M/F)*",
            options=["M", "F"],
            index=(["M", "F"].index(pdata["Sex"][0])),
            help="Enter your sex: Male (M) / Female (F)",
        )

    # Patient Address
    u_region = st.selectbox(
        label="Region*",
        options=region_list,
        help="Select your region.",
        key="u_region",
        index=(region_list.index(pdata["Region"][0])),
        on_change=update_region,
    )

    if u_province not in st.session_state["uprovince_list"]:
        u_province = st.session_state["uprovince_list"][0]

        u_province = st.selectbox(
            label="Province*",
            options=st.session_state["uprovince_list"],
            help="Select your province.",
            key="u_province",
            index=(st.session_state["uprovince_list"].index(pdata["Province"][0])),
            on_change=update_province,
        )

    else:
        u_province = st.selectbox(
            label="Province*",
            options=st.session_state["uprovince_list"],
            help="Select your province.",
            key="u_province",
            on_change=update_province,
        )

    if u_municity not in st.session_state["umunicity_list"]:
        u_municity = st.session_state["umunicity_list"][0]

        u_municity = st.selectbox(
            label="Municipality/City*",
            options=st.session_state["umunicity_list"],
            help="Select your municipality/city.",
            key="u_municity",
            index=(
                st.session_state["umunicity_list"].index(pdata["Municipality/City"][0])
            ),
            on_change=update_municity,
        )
    else:
        u_municity = st.selectbox(
            label="Municipality/City*",
            options=st.session_state["umunicity_list"],
            help="Select your municipality/city.",
            key="u_municity",
            index=(
                st.session_state["umunicity_list"].index(pdata["Municipality/City"][0])
            ),
            on_change=update_municity,
        )

    if u_brgy not in st.session_state["ubrgy_list"]:
        u_brgy = st.session_state["ubrgy_list"][0]
        u_brgy = st.selectbox(
            label="Barangay*",
            options=st.session_state["ubrgy_list"],
            help="Select your barangay.",
            index=(st.session_state["ubrgy_list"].index(pdata["Barangay"][0])),
            key="u_brgy",
        )
    else:
        u_brgy = st.selectbox(
            label="Barangay*",
            options=st.session_state["ubrgy_list"],
            help="Select your barangay.",
            key="u_brgy",
            index=(st.session_state["ubrgy_list"].index(pdata["Barangay"][0])),
        )

    # Form submit button
    if st.button(label="Submit", type="primary"):
        # Check if all required fields are filled
        if not u_first_name or not u_last_name:
            st.error("Please fill out all required fields.")
        elif count_alnum_chars(u_first_name) <= 0:
            st.error("Please enter a valid first name.")
        elif count_alnum_chars(u_last_name) <= 0:
            st.error("Please enter a valid last name.")
        else:
            u_data = {
                "ID": pid,
                "First Name": u_first_name.lower().strip(),
                "Middle Name": u_middle_name.lower().strip(),
                "Last Name": u_last_name.lower().strip(),
                "Suffix": u_suffix.lower().strip(),
                "Birthdate": u_birthdate.isoformat(),
                "Sex": u_sex,
                "Region": u_region,
                "Province": u_province,
                "Municipality/City": u_municity,
                "Barangay": u_brgy,
            }

            # Create df from dict of patient data
            u_data_df = pl.DataFrame(u_data)

            test_data_df = st.session_state["pl_data"]

            # Remove old patient personal info
            test_data_df = test_data_df.filter(pl.col("ID") != pid)

            # Add new patient personal info
            st.session_state["pl_data"] = pl.concat([test_data_df, u_data_df])

            # Modify patient records with new personal info

            test_records = st.session_state["pl_records"]
            specific_test_records = test_records.filter(pl.col("PID") == pid)

            # Drop old patient personal info
            test_records_new = test_records.filter(pl.col("PID") != pid)

            specific_test_records = specific_test_records.with_columns(
                [
                    pl.col("Sex").apply(lambda x: u_sex),
                    (
                        (
                            (
                                pl.col("Timestamp").str.strptime(pl.Date, "%Y-%m-%d")
                                - u_birthdate
                            )
                            * (12 / 365.25)
                            * (1 / 86400000)
                        ).cast(pl.Int64)
                    ).alias("Month_Age"),
                    pl.col("Region").apply(lambda x: u_region),
                    pl.col("Province").apply(lambda x: u_province),
                    pl.col("Municipality/City").apply(lambda x: u_municity),
                    pl.col("Barangay").apply(lambda x: u_brgy),
                ]
            )

            # Add new patient personal info
            st.session_state["pl_records"] = pl.concat(
                [test_records_new, specific_test_records]
            )

            # Show success message
            st.success("🎉 Profile updated successfully.")
            st.balloons()

            # Clear form
            u_first_name = ""
            u_middle_name = ""
            u_last_name = ""
            u_suffix = ""
            u_birthdate = u_birthdate
            u_sex = "M"
