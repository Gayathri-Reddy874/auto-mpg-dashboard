import streamlit as st
from src.data_loader import load_data
from src.kpi_calculator import calculate_kpis
from src.plotly_charts import (
    fuel_efficiency_trend,
    mpg_by_origin_chart,
    mpg_vs_weight_chart,
    mpg_vs_hp_chart,
    mpg_distribution_chart
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Auto MPG Dashboard",
    layout="wide"
)

st.title("🚗 Auto MPG Executive Dashboard")

# =========================
# LOAD DATA
# =========================
df = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("Filters")

# Origin
selected_origin = st.sidebar.multiselect(
    "Origin",
    options=sorted(df["origin"].unique()),
    default=sorted(df["origin"].unique())
)

# Cylinders
selected_cylinders = st.sidebar.multiselect(
    "Cylinders",
    options=sorted(df["cylinders"].unique()),
    default=sorted(df["cylinders"].unique())
)

# Model Year
selected_year = st.sidebar.multiselect(
    "Model Year",
    options=sorted(df["model_year"].unique()),
    default=sorted(df["model_year"].unique())
)

# MPG Range
mpg_min, mpg_max = st.sidebar.slider(
    "MPG Range",
    float(df["mpg"].min()),
    float(df["mpg"].max()),
    (float(df["mpg"].min()), float(df["mpg"].max()))
)

# Horsepower Range
hp_min, hp_max = st.sidebar.slider(
    "Horsepower Range",
    float(df["horsepower"].min()),
    float(df["horsepower"].max()),
    (float(df["horsepower"].min()), float(df["horsepower"].max()))
)

# =========================
# SAFE FILTERING
# =========================
if not selected_origin:
    st.warning("⚠️ Please select at least one origin")
    st.stop()

filtered_df = df[
    (df["origin"].isin(selected_origin)) &
    (df["cylinders"].isin(selected_cylinders)) &
    (df["model_year"].isin(selected_year)) &
    (df["mpg"] >= mpg_min) &
    (df["mpg"] <= mpg_max) &
    (df["horsepower"] >= hp_min) &
    (df["horsepower"] <= hp_max)
]

# =========================
# KPI CALCULATION
# =========================
kpis = calculate_kpis(filtered_df)

avg_mpg = round(kpis["avg_mpg"], 2)
yoy_growth = round(kpis["yoy_growth"], 2)
avg_hp = round(kpis["avg_hp"], 2)
total_vehicles = int(kpis["total_vehicles"])

# =========================
# KPI CARDS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Average MPG", avg_mpg)
col2.metric("YoY Growth %", yoy_growth)
col3.metric("Average Horsepower", avg_hp)
col4.metric("Total Vehicles", total_vehicles)

st.divider()

# =========================
# CHARTS
# =========================
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fuel_efficiency_trend(filtered_df),
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        mpg_by_origin_chart(filtered_df),
        use_container_width=True
    )

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        mpg_vs_weight_chart(filtered_df),
        use_container_width=True
    )

with col4:
    st.plotly_chart(
        mpg_vs_hp_chart(filtered_df),
        use_container_width=True
    )

st.plotly_chart(
    mpg_distribution_chart(filtered_df),
    use_container_width=True
)

# =========================
# TABLE
# =========================
st.subheader("📋 Dataset Preview")
st.dataframe(filtered_df.head(20), use_container_width=True)