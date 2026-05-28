import seaborn as sns
import matplotlib.pyplot as plt


def correlation_heatmap(df):

    corr = df[
        [
            "mpg",
            "weight",
            "horsepower",
            "displacement",
            "cylinders"
        ]
    ].corr()

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.heatmap(
        corr,
        annot=True,
        cmap="Blues",
        ax=ax
    )

    ax.set_title("Correlation Heatmap")

    return fig