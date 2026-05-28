import pandas as pd
import streamlit as st


@st.cache_data
def load_data():

    df = pd.read_csv(
    "data/auto-mpg.data",
    sep=r"\s+",
    header=None,
    na_values="?"
)

    df.columns = [
        "mpg",
        "cylinders",
        "displacement",
        "horsepower",
        "weight",
        "acceleration",
        "model_year",
        "origin",
        "car_name"
    ]

    df.dropna(inplace=True)

    origin_map = {
        1: "USA",
        2: "Europe",
        3: "Japan"
    }

    df["origin"] = df["origin"].map(origin_map)

    return df