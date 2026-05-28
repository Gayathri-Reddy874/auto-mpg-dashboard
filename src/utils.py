"""
Utility Functions Module
------------------------
Contains reusable helper functions used across the project.
"""

import pandas as pd


def format_number(value):
    """
    Format large numbers into readable format.

    Example:
    1500 -> 1.5K
    2500000 -> 2.5M
    """

    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"

    elif value >= 1_000:
        return f"{value / 1_000:.1f}K"

    return str(round(value, 2))


def calculate_market_share(df, column_name):
    """
    Calculate percentage distribution
    for a categorical column.
    """

    market_share = (
        df[column_name]
        .value_counts(normalize=True) * 100
    )

    return market_share.round(2)


def safe_division(numerator, denominator):
    """
    Prevent division by zero errors.
    """

    if denominator == 0:
        return 0

    return numerator / denominator


def get_top_n(df, column_name, n=5):
    """
    Return top N frequent values.
    """

    return df[column_name].value_counts().head(n)


def generate_summary_statistics(df):
    """
    Generate summary statistics
    for numerical columns.
    """

    return df.describe().round(2)


def convert_origin_codes(df):
    """
    Convert numeric origin codes
    into country names.
    """

    origin_map = {
        1: "USA",
        2: "Europe",
        3: "Japan"
    }

    df["origin"] = df["origin"].map(origin_map)

    return df


def create_power_to_weight_ratio(df):
    """
    Create power-to-weight ratio feature.
    """

    df["power_to_weight"] = (
        df["horsepower"] / df["weight"]
    )

    return df


def check_missing_values(df):
    """
    Return missing value count.
    """

    return df.isnull().sum()


def remove_duplicates(df):
    """
    Remove duplicate records.
    """

    return df.drop_duplicates()


def filter_dataframe(df, column_name, value):
    """
    Generic dataframe filter function.
    """

    return df[df[column_name] == value]