import plotly.express as px


def fuel_efficiency_trend(df):

    mpg_trend = (
        df.groupby("model_year")["mpg"]
        .mean()
        .reset_index()
    )

    fig = px.line(
        mpg_trend,
        x="model_year",
        y="mpg",
        markers=True,
        title="Fuel Efficiency Trend"
    )

    return fig


def mpg_by_origin_chart(df):

    mpg_origin = (
        df.groupby("origin")["mpg"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        mpg_origin,
        x="origin",
        y="mpg",
        text="mpg",
        title="Average MPG by Origin"
    )

    return fig


def mpg_vs_weight_chart(df):

    fig = px.scatter(
        df,
        x="weight",
        y="mpg",
        color="origin",
        trendline="ols",
        title="MPG vs Weight"
    )

    return fig


def mpg_vs_hp_chart(df):

    fig = px.scatter(
        df,
        x="horsepower",
        y="mpg",
        color="origin",
        trendline="ols",
        title="MPG vs Horsepower"
    )

    return fig


def mpg_distribution_chart(df):

    fig = px.histogram(
        df,
        x="mpg",
        nbins=20,
        title="MPG Distribution"
    )

    return fig