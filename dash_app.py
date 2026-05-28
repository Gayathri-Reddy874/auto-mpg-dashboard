from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

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
# LOAD DATA
# =========================
df = load_data()

# =========================
# APP INIT
# =========================
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY]
)

# =========================
# LAYOUT (INDUSTRY GRID STRUCTURE)
# =========================
app.layout = dbc.Container([

    # =========================
    # TITLE SECTION
    # =========================
    dbc.Row([
        dbc.Col(
            html.H1(
                "🚗 Auto MPG Executive Dashboard",
                style={
                    "textAlign": "center",
                    "marginTop": "20px",
                    "marginBottom": "10px"
                }
            ),
            width=12
        )
    ]),

    html.Hr(),

    # =========================
    # FILTER SECTION
    # =========================
    dbc.Row([

        dbc.Col([
            html.Label("Origin"),
            dcc.Dropdown(
                id="origin-filter",
                options=[{"label": i, "value": i} for i in sorted(df["origin"].unique())],
                value=list(df["origin"].unique()),
                multi=True
            )
        ], width=4),

        dbc.Col([
            html.Label("Cylinders"),
            dcc.Dropdown(
                id="cyl-filter",
                options=[{"label": i, "value": i} for i in sorted(df["cylinders"].unique())],
                value=list(df["cylinders"].unique()),
                multi=True
            )
        ], width=4),

        dbc.Col([
            html.Label("Model Year"),
            dcc.Dropdown(
                id="year-filter",
                options=[{"label": i, "value": i} for i in sorted(df["model_year"].unique())],
                value=list(df["model_year"].unique()),
                multi=True
            )
        ], width=4),

    ], className="mb-3"),

    html.Hr(),

    # =========================
    # KPI ROW
    # =========================
    dbc.Row(id="kpi-row", className="mb-4"),

    html.Hr(),

    # =========================
    # CHART ROW 1
    # =========================
    dbc.Row([

        dbc.Col(dcc.Graph(id="trend-chart"), width=6),
        dbc.Col(dcc.Graph(id="origin-chart"), width=6),

    ], className="mb-4"),

    # =========================
    # CHART ROW 2
    # =========================
    dbc.Row([

        dbc.Col(dcc.Graph(id="weight-chart"), width=6),
        dbc.Col(dcc.Graph(id="hp-chart"), width=6),

    ], className="mb-4"),

    # =========================
    # FULL WIDTH CHART
    # =========================
    dbc.Row([

        dbc.Col(dcc.Graph(id="dist-chart"), width=12),

    ], className="mb-4"),

], fluid=True)


# =========================
# CALLBACK
# =========================
@app.callback(
    [
        Output("kpi-row", "children"),
        Output("trend-chart", "figure"),
        Output("origin-chart", "figure"),
        Output("weight-chart", "figure"),
        Output("hp-chart", "figure"),
        Output("dist-chart", "figure"),
    ],
    [
        Input("origin-filter", "value"),
        Input("cyl-filter", "value"),
        Input("year-filter", "value"),
    ]
)
def update_dashboard(selected_origin, selected_cyl, selected_year):

    # =========================
    # FILTER DATA
    # =========================
    filtered_df = df[
        (df["origin"].isin(selected_origin)) &
        (df["cylinders"].isin(selected_cyl)) &
        (df["model_year"].isin(selected_year))
    ]

    # =========================
    # KPIs
    # =========================
    kpis = calculate_kpis(filtered_df)

    # =========================
    # KPI CARDS
    # =========================
    kpi_cards = [
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Avg MPG"),
                    html.H2(round(kpis["avg_mpg"], 2))
                ])
            ], color="primary", inverse=True),
            width=3
        ),

        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Avg HP"),
                    html.H2(round(kpis["avg_hp"], 2))
                ])
            ], color="info", inverse=True),
            width=3
        ),

        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("YoY Growth %"),
                    html.H2(round(kpis["yoy_growth"], 2))
                ])
            ], color="success", inverse=True),
            width=3
        ),

        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Total Vehicles"),
                    html.H2(int(kpis["total_vehicles"]))
                ])
            ], color="warning", inverse=True),
            width=3
        ),
    ]

    return (
        kpi_cards,
        fuel_efficiency_trend(filtered_df),
        mpg_by_origin_chart(filtered_df),
        mpg_vs_weight_chart(filtered_df),
        mpg_vs_hp_chart(filtered_df),
        mpg_distribution_chart(filtered_df),
    )


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=False)