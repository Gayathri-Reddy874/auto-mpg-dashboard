def calculate_kpis(df):

    mpg_year = df.groupby("model_year")["mpg"].mean()

    yoy_growth = round(
        mpg_year.pct_change().mean() * 100,
        2
    )

    return {
        "avg_mpg": round(df["mpg"].mean(), 2),
        "avg_hp": round(df["horsepower"].mean(), 2),
        "total_vehicles": len(df),
        "yoy_growth": yoy_growth
    }