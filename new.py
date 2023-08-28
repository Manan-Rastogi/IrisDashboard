import pandas as pd
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
import json

df = pd.read_csv(
    "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"
)
df["date"] = pd.to_datetime(df["date"])

df = df.sort_values(["date", "iso_code"])

px.bar(
    df.groupby("iso_code", as_index=False).last().sample(20),
    x="iso_code",
    y="total_vaccinations",
)

from jupyter_dash import JupyterDash

# Build App
app = JupyterDash(__name__)
app.layout = dash.html.Div(
    [
        dash.dcc.Graph(
            id="bar_chart",
            figure=px.bar(
                df.groupby("iso_code", as_index=False).last().sample(20),
                x="iso_code",
                y="total_vaccinations",
            ),
        ),
        dash.html.Div(
            id="table_container",
        ),
    ]
)


@app.callback(
    Output("table_container", "children"),
    Input("bar_chart", "clickData"),
)
def fig_click(clickData):
    if not clickData:
        raise dash.exceptions.PreventUpdate

    tab = dash.dash_table.DataTable(
        data=df.loc[df["iso_code"].eq(clickData["points"][0]["x"])]
        .tail(5)
        .to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
    )

    return tab


app.run_server(mode="inline")