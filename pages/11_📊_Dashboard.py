import datetime as dt
import uuid

import pandas as pd
import plotly.express as px
import polars as pl
import streamlit as st

from load import classify_malnutrition, init_page, load_brand, load_ph_location_data

init_page(
    pg_title="Dashboard",
    pg_icon="📊",
    title="Dashboard",
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
    filter_records = patient_records.with_columns(
        pl.struct(["Alive", "Default", "Edema", "MUAC (cm)", "Z-score"])
        .apply(
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

# Filter patient data by region, province, municipality, and barangay
with st.expander("Filter by Location"):
    patient_region = st.selectbox(
        label="Region",
        options=region_list,
        help="Select your region.",
        key="in_region",
        index=0,
        on_change=on_change_region,
    )

    if patient_province not in st.session_state["province_list"]:
        patient_province = st.session_state["province_list"][0]

        patient_province = st.selectbox(
            label="Province",
            options=st.session_state["province_list"],
            help="Select your province.",
            key="in_province",
            index=0,
            on_change=on_change_province,
        )
    else:
        patient_province = st.selectbox(
            label="Province",
            options=st.session_state["province_list"],
            help="Select your province.",
            key="in_province",
            index=0,
            on_change=on_change_province,
        )

    if patient_municity not in st.session_state["municity_list"]:
        patient_municity = st.session_state["municity_list"][0]

        patient_municity = st.selectbox(
            label="Municipality/City",
            options=st.session_state["municity_list"],
            help="Select your municipality/city.",
            key="in_municity",
            index=0,
            on_change=on_change_municity,
        )
    else:
        patient_municity = st.selectbox(
            label="Municipality/City",
            options=st.session_state["municity_list"],
            help="Select your municipality/city.",
            key="in_municity",
            index=0,
            on_change=on_change_municity,
        )

    if patient_brgy not in st.session_state["brgy_list"]:
        patient_brgy = st.session_state["brgy_list"][0]
        patient_brgy = st.selectbox(
            label="Barangay",
            options=st.session_state["brgy_list"],
            help="Select your barangay.",
            key="in_brgy",
            index=0,
        )
    else:
        patient_brgy = st.selectbox(
            label="Barangay",
            options=st.session_state["brgy_list"],
            help="Select your barangay.",
            key="in_brgy",
            index=0,
        )

    submitted_filter = st.button("Submit", type="primary")

    if submitted_filter:
        if patient_region != "All Regions":
            filter_records = filter_records.filter(pl.col("Region") == patient_region)

        if patient_province != "All Provinces":
            filter_records = filter_records.filter(
                pl.col("Province") == patient_province
            )

        if patient_municity != "All Municipalities/Cities":
            filter_records = filter_records.filter(
                pl.col("Municipality-City") == patient_municity
            )

        if patient_brgy != "All Barangays":
            filter_records = filter_records.filter(pl.col("Barangay") == patient_brgy)

        filter_records = filter_records
        st.session_state["filter_rdf"] = filter_records
        if filter_records.height == patient_records.height:
            st.warning("No records were filtered.")
        else:
            st.success(f"Successfully filtered {filter_records.height} records.")

# Choose data to display in graph
with st.expander("Choose Data"):
    dcol1, dcol2 = st.columns(2)
    with dcol1:
        graph_choice = st.radio(
            label="Choose status to display in graph",
            options=["Deaths", "Defaults", "SAM", "MAM", "Normal"],
            help="Choose status to display in graph.",
            key="in_graph_choice",
            index=0,
        )
        if graph_choice == "Deaths":
            filter_stat = "DEAD"
        elif graph_choice == "Defaults":
            filter_stat = "DEFAULT"
        elif graph_choice == "SAM":
            filter_stat = "SEVERE"
        elif graph_choice == "MAM":
            filter_stat = "MODERATE"
        elif graph_choice == "Normal":
            filter_stat = "NORMAL"

    with dcol2:
        period_interval = st.radio(
            label="Choose period interval",
            options=["Daily", "Weekly", "Monthly"],
            help="Choose period interval.",
            key="in_period_interval",
            index=2,
        )

        if period_interval == "Daily":
            interval = "1d"
        elif period_interval == "Weekly":
            interval = "1w"
        elif period_interval == "Monthly":
            interval = "1M"

# Display metrics for active and total cases
active_frecords = filter_records.unique("PID").sort("Timestamp")
active_sam = active_frecords.filter(pl.col("Malnutrition Status") == "SEVERE").height
active_mam = active_frecords.filter(pl.col("Malnutrition Status") == "MODERATE").height
active_normal = active_frecords.filter(pl.col("Malnutrition Status") == "NORMAL").height
active_dead = active_frecords.filter(pl.col("Malnutrition Status") == "DEAD").height
active_default = active_frecords.filter(
    pl.col("Malnutrition Status") == "DEFAULT"
).height

total_frecords = filter_records.sort("Timestamp")
total_sam = total_frecords.filter(pl.col("Malnutrition Status") == "SEVERE").height
total_mam = total_frecords.filter(pl.col("Malnutrition Status") == "MODERATE").height
total_normal = total_frecords.filter(pl.col("Malnutrition Status") == "NORMAL").height
total_dead = total_frecords.filter(pl.col("Malnutrition Status") == "DEAD").height
total_default = total_frecords.filter(pl.col("Malnutrition Status") == "DEFAULT").height

# Display active and total number of patients
st.header("Active and Total Number of Cases")
r1c1, r1c2, r1c3, r1c4, r1c5 = st.columns(5)
r1c1.metric(label="Active SAM", value=active_sam)
r1c2.metric(label="Active MAM", value=active_mam)
r1c3.metric(label="Active Normal", value=active_normal)
r1c4.metric(label="Active Dead", value=active_dead)
r1c5.metric(label="Active Default", value=active_default)

r2c1, r2c2, r2c3, r2c4, r2c5 = st.columns(5)
r2c1.metric(label="Total SAM", value=total_sam)
r2c2.metric(label="Total MAM", value=total_mam)
r2c3.metric(label="Total Normal", value=total_normal)
r2c4.metric(label="Total Dead", value=total_dead)
r2c5.metric(label="Total Default", value=total_default)


filter_df = (
    filter_records.select(["Timestamp", "Malnutrition Status"])
    .with_columns(
        [
            ((pl.col("Malnutrition Status") == filter_stat) * 1).alias("Count"),
            (pl.col("Timestamp").str.strptime(pl.Date, "%Y-%m-%d").alias("Timestamp")),
        ]
    )
    .filter(pl.col("Count") == 1)
).sort("Timestamp", descending=True)
filter_dfu = filter_df.to_pandas()
filter_dfu["Timestamp"] = pd.to_datetime(filter_dfu["Timestamp"])
if not filter_dfu.empty:
    filter_dfu = filter_dfu.resample(interval, on="Timestamp").sum().fillna(0)
    # Remove zero values
    filter_dfu = filter_dfu[filter_dfu["Count"] != 0]

    # Calculate 4-week moving average
    filter_dfu["MA"] = filter_dfu["Count"].rolling(window=4).mean()

    # Display graph
    fig1 = px.bar(
        filter_dfu,
        x=filter_dfu.index,
        y="Count",
        title=f"Number of {graph_choice} {period_interval}",
        labels={
            "Count": f"Number of {graph_choice}",
            "Timestamp": f"{period_interval}",
        },
    )
    # Add moving average line
    fig1.add_scatter(x=filter_dfu.index, y=filter_dfu["MA"], mode="lines", name="MA")
    fig1.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
            type="date",
        )
    )

    # Increase height of graph
    fig1.update_layout(height=600)

    # Display graph
    st.divider()
    st.header(f"Data Time Series")
    st.plotly_chart(fig1, use_container_width=True)

else:
    st.warning("No records.")

# Calculate top number of active graph choice cases by region, province, and municipality/city
