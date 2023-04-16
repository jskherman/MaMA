import datetime as dt
import random

import polars as pl
import streamlit as st

# Faker Import
from faker import Faker
from faker.providers import BaseProvider


@st.cache_data  # Cache data for faster loading
def load_ph_location_data(type="polars"):
    # Set data types of columns for PH locations
    loc_dtypes = {
        "10-digit PSGC": pl.Utf8,
        "Geocode": pl.Utf8,
        "Brgy Code": pl.Utf8,
        "MuniCity Code": pl.Utf8,
        "Municipality-City": pl.Utf8,
        "Prov Code": pl.Utf8,
        "Province": pl.Utf8,
        "Reg Code": pl.Utf8,
        "Region": pl.Utf8,
    }

    # Load PH locations data from CSV
    if type == "polars":
        # Return Polars DataFrame if type is "polars"
        df = pl.read_csv("data/ph_locations.csv", encoding="utf-8", dtypes=loc_dtypes)
    elif type == "pandas":
        # Return Pandas DataFrame if type is "pandas"
        df = pl.read_csv(
            "data/ph_locations.csv", encoding="utf-8", dtypes=loc_dtypes
        ).to_pandas()
    else:
        # Raise error if type is not "polars" or "pandas"
        raise ValueError("Invalid type. Must be either 'polars' or 'pandas'.")
    return df


# Filipino Data Provider for Faker library
class FilipinoDataProvider(BaseProvider):
    # Name suffixes
    SUFFIXES = ["", "Sr.", "III", "IV", "V", "VI"]

    # Set data types of columns for PH locations
    loc_dtypes = {
        "10-digit PSGC": pl.Utf8,
        "Geocode": pl.Utf8,
        "Brgy Code": pl.Utf8,
        "MuniCity Code": pl.Utf8,
        "Municipality-City": pl.Utf8,
        "Prov Code": pl.Utf8,
        "Province": pl.Utf8,
        "Reg Code": pl.Utf8,
        "Region": pl.Utf8,
    }

    # Load PH locations data from CSV
    PH_LOC_DF = load_ph_location_data()

    # Create lists of regions, provinces, municipalities/cities, and barangays
    REGIONS = (
        PH_LOC_DF.select(pl.col("Region").unique().sort())  # type: ignore
        .get_column("Region")
        .to_list()
    )
    PROVINCES = (
        PH_LOC_DF.select(pl.col("Province").unique().sort())  # type: ignore
        .get_column("Province")
        .to_list()
    )
    MUNICITIES = (
        PH_LOC_DF.select(pl.col("Municipality-City").unique().sort())  # type: ignore
        .get_column("Municipality-City")
        .to_list()
    )
    BRGYS = (
        PH_LOC_DF.select(pl.col("Barangay").unique().sort())  # type: ignore
        .get_column("Barangay")
        .to_list()
    )

    def filipino_suffix(self):
        """
        Returns a random suffix.
        """
        return self.random_element(self.SUFFIXES)

    def ph_region(self):
        """
        Returns a random region.
        """
        return self.random_element(self.REGIONS)

    def ph_province(self, region=None):
        """
        Returns a random province. If a region is specified, returns a random
        province in that region.
        """
        if region:
            prov_list = (
                self.PH_LOC_DF.filter(pl.col("Region") == region)
                .select(pl.col("Province").unique().sort())  # type: ignore
                .get_column("Province")
                .to_list()
            )
            return self.random_element(prov_list)
        else:
            return self.random_element(self.PROVINCES)

    def ph_municity(self, province=None):
        """
        Returns a random municipality/city. If a province is specified, returns
        a random municipality/city in that province.
        """
        if province:
            municity_list = (
                self.PH_LOC_DF.filter(pl.col("Province") == province)
                .select(pl.col("Municipality-City").unique().sort())  # type: ignore
                .get_column("Municipality-City")
                .to_list()
            )
            return self.random_element(municity_list)
        else:
            return self.random_element(self.MUNICITIES)

    def ph_brgy(self, municity=None):
        """
        Returns a random barangay. If a municipality/city is specified, returns
        a random barangay in that municipality/city.
        """
        if municity:
            brgy_list = (
                self.PH_LOC_DF.filter(pl.col("Municipality-City") == municity)
                .select(pl.col("Barangay").unique().sort())  # type: ignore
                .get_column("Barangay")
                .to_list()
            )
            return self.random_element(brgy_list)
        else:
            return self.random_element(self.BRGYS)


def init_page(pg_title, pg_icon="🍖", title=None, layout="wide"):
    """
    Initialize a streamlit page with a title, icon, and CSS styles.
    """
    st.set_page_config(
        page_title=pg_title,
        page_icon=pg_icon,
        layout=layout,  # type: ignore
    )

    # Load CSS styles
    if "css" not in st.session_state:
        st.session_state["css"] = open("assets/css/style.css").read()
    st.markdown(f"<style>{st.session_state['css']}\n</style>", unsafe_allow_html=True)

    if title:
        st.title(title)


def load_brand():
    """
    Load the MaMA brand logo and name.
    """

    with st.sidebar:
        st.image("assets/img/logo.png")

        st.markdown(
            """
            <center><strong>Ma</strong>lnutrition&nbsp;<strong>M</strong>
            onitoring and&nbsp;<strong>A</strong>ssessment&nbsp;System</center>

            <br><br> Project by Team NutriBUn &copy;&nbsp;2022–2023
            """,
            unsafe_allow_html=True,
        )


def count_alnum_chars(text: str):
    """
    Count the number of alphanumeric characters in a string that is not a space
    using only the standard library
    """
    return sum(c.isalnum() for c in text)


def load_testdata(num: int = 30, type: str = "polars"):
    """
    Load test data for the MaMA system.
    """

    # Faker library Config
    fake = Faker("fil_PH")  # Set locale to Filipino
    fake.add_provider(FilipinoDataProvider)  # Add Filipino data provider earlier

    test_data = []
    data = {}

    # Generate test data using Faker up to the specified number of entries `num`
    for _ in range(num):
        data["ID"] = str(fake.uuid4())
        data["First Name"] = fake.first_name().lower()
        data["Middle Name"] = fake.last_name().lower()
        data["Last Name"] = fake.last_name().lower()
        data["Suffix"] = fake.filipino_suffix().lower()
        data["Birthdate"] = fake.date_of_birth(minimum_age=1, maximum_age=4).isoformat()
        data["Sex"] = fake.random_element(elements=("M", "F"))
        data["Region"] = fake.ph_region()
        data["Province"] = fake.ph_province(region=data["Region"])
        data["Municipality/City"] = fake.ph_municity(province=data["Province"])
        data["Barangay"] = fake.ph_brgy(municity=data["Municipality/City"])
        test_data.append(data)
        data = {}

    # Convert test data to a Polars or Pandas DataFrame
    if type == "polars":
        test_data_df = pl.DataFrame(test_data)
    elif type == "pandas":
        test_data_df = pl.DataFrame(test_data).to_pandas()
    else:
        raise ValueError("Invalid type. Must be either 'polars' or 'pandas'.")
    return test_data_df


def load_testrecords(test_data: pl.DataFrame, num: int = 30, type: str = "polars"):
    """
    Load test records for the MaMA system based on the test patient data.
    """
    patient_ids = test_data.select(pl.col("ID")).get_column("ID").to_list()

    # Faker library Config
    fake = Faker("fil_PH")  # Set locale to Filipino

    test_records = []
    record = {}

    for _ in range(num):
        record["ID"] = str(fake.uuid4())
        record["PID"] = fake.random_element(elements=patient_ids)
        record["Sex"] = (
            test_data.filter(pl.col("ID") == record["PID"])
            .select(pl.col("Sex"))
            .get_column("Sex")[0]
        )
        pbirthdate = (
            test_data.filter(pl.col("ID") == record["PID"])
            .select(pl.col("Birthdate"))
            .get_column("Birthdate")[0]
        )
        record["Timestamp"] = fake.date_between(
            start_date=(dt.date.fromisoformat(pbirthdate) + dt.timedelta(days=10)),
            end_date=(
                min(
                    dt.date.fromisoformat(pbirthdate) + dt.timedelta(days=1800),
                    dt.date.today(),
                )
            ),
        ).isoformat()
        record["Month_Age"] = round(
            (
                dt.date.fromisoformat(record["Timestamp"])
                - dt.date.fromisoformat(pbirthdate)
            ).days
            * 12
            / 365.25
        )
        record["Region"] = (
            test_data.filter(pl.col("ID") == record["PID"])
            .select(pl.col("Region"))
            .get_column("Region")[0]
        )
        record["Province"] = (
            test_data.filter(pl.col("ID") == record["PID"])
            .select(pl.col("Province"))
            .get_column("Province")[0]
        )
        record["Municipality/City"] = (
            test_data.filter(pl.col("ID") == record["PID"])
            .select(pl.col("Municipality/City"))
            .get_column("Municipality/City")[0]
        )
        record["Barangay"] = (
            test_data.filter(pl.col("ID") == record["PID"])
            .select(pl.col("Barangay"))
            .get_column("Barangay")[0]
        )
        record["Z-score"] = round(random.uniform(-3.5, 3.5), 2)
        if record["Sex"] == "M":
            record["Weight (kg)"] = round(random.uniform(1.6, 24.8), 2)
            record["Height (cm)"] = round(random.uniform(43.6, 120), 2)
            record["MUAC (cm)"] = round(random.uniform(10.5, 22), 2)
        elif record["Sex"] == "F":
            record["Weight (kg)"] = round(random.uniform(1.5, 25.3), 2)
            record["Height (cm)"] = round(random.uniform(43.0, 120), 2)
            record["MUAC (cm)"] = round(random.uniform(10, 23), 2)
        record["Default"] = fake.random_element(elements=(True, False))
        record["Alive"] = fake.random_element(elements=(True, False))
        record["Edema"] = fake.random_element(elements=(True, False))
        test_records.append(record)
        record = {}

    # Convert test data to a Polars or Pandas DataFrame
    if type == "polars":
        test_records_df = pl.DataFrame(test_records).sort("Timestamp", descending=True)
    elif type == "pandas":
        test_records_df = (
            pl.DataFrame(test_records).sort("Timestamp", descending=True).to_pandas()
        )
    else:
        raise ValueError("Invalid type. Must be either 'polars' or 'pandas'.")
    return test_records_df
