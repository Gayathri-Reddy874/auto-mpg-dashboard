import matplotlib.pyplot as plt


def mpg_line_chart(df):

    mpg_year = (
        df.groupby("model_year")["mpg"]
        .mean()
    )

    fig, ax = plt.subplots()

    mpg_year.plot(
        kind="line",
        ax=ax
    )

    ax.set_title("Fuel Efficiency Trend")

    return fig