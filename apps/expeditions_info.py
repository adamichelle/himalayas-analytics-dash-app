import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app import app

from dataframes import df_expeditions

df_expeditions.sort_values("year", inplace=True)

seasons_dropdown_options = []
season_names = df_expeditions['season'].value_counts(dropna=False).keys().tolist()

for name in season_names:
    if(name == "Unknown"):
        break
    seasons_dropdown_options.append({"label": name, "value": name})

data = df_expeditions.query("season == 'Autumn'")

expeditions_details_per_year = data.groupby("year").sum().reset_index()
expeditions_details_per_year["number_of_expeditions"] = expeditions_details_per_year['year'].map(data['year'].value_counts())

layout = html.Div(
    children=[
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H1(children='Himalayas Expeditions Analytics'), className="mb-2")
            ]),
            dbc.Row([
                dbc.Col(html.P(children='Visualising expedition info by season in the Himalayas from the 1920s - 2010s'), className="mb-4")
            ]),
            dbc.Row([
                dcc.Dropdown(
                    id='seasons-filter',
                    options=seasons_dropdown_options,
                    value='Autumn',
                    style={'width': '50%'},
                    clearable=False,
                    className="mb-2"
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id="expeditions-no-chart", config={"displayModeBar": False},
                    ),
                    className="card mb-3",
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id="expeditions-members-chart", config={"displayModeBar": False},
                    ),
                    className="card mb-3",
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id="expeditions-deaths-chart", config={"displayModeBar": False},
                    ),
                    className="card mb-3",
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id="pie-termination-reasons-chart", config={"displayModeBar": False},
                    ),
                    className="card mb-3",
                )
            ]),
        ]),
    ]
)

@app.callback(
    [
        Output("expeditions-no-chart", "figure"), 
        Output("expeditions-members-chart", "figure"), 
        Output("expeditions-deaths-chart", "figure"),
        Output("pie-termination-reasons-chart", "figure")
    ],
    [
        Input("seasons-filter", "value")
    ],
)
def update_charts(season):
    query = "season == '{season}'".format(season = season)
    data = df_expeditions.query(query)
    expeditions_details_per_year = data.groupby("year").sum().reset_index()
    expeditions_details_per_year["number_of_expeditions"] = expeditions_details_per_year['year'].map(data['year'].value_counts())

    termination_reasons_df = data["termination_reason"].value_counts().to_frame().reset_index()
    termination_reasons_df.columns = ["termination_reason", "number_of_expeditions"]

    expedition_ids_df = data["expedition_id"].value_counts().to_frame().reset_index()
    peak_names_df = data["peak_name"].value_counts().to_frame().reset_index()
    peak_names_df.columns = ["peak_name", "number_of_expeditions"]

    expeditions_no_chart_figure = {
        "data": [
            {
                "x": expeditions_details_per_year["year"],
                "y": expeditions_details_per_year["number_of_expeditions"],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {
                "text": "Total number of expeditions by year",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {
                "title": "Year"
            },
            "yaxis": {
                "title": "Number of Expeditions"
            },
            "colorway": ["#2F8799"],
        },
    }

    expeditions_members_chart_figure = {
        "data": [
            {
                "x": expeditions_details_per_year["year"],
                "y": expeditions_details_per_year["members"],
                "type": "bar",
            },
        ],
        "layout": {
            "title": {
                "text": "Total number of expedition members by year",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {
                "title": "Year"
            },
            "yaxis": {
                "title": "Number of Members"
            },
            "colorway": ["#A64C4C"],
        },
    }

    expeditions_deaths_chart_figure = {
        "data": [
            {
                "x": expeditions_details_per_year["year"],
                "y": expeditions_details_per_year["member_deaths"],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {
                "text": "Total number of expedition member deaths by year",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {
                "title": "Year"
            },
            "yaxis": {
                "title": "Number of Expedition Member Deaths"
            },
            "colorway": ["#17B897"],
        },
    }

    pie_termination_reasons_chart_figure = px.pie(termination_reasons_df, values=termination_reasons_df["number_of_expeditions"], names=termination_reasons_df["termination_reason"], title='Termination reasons for Expeditions')
    return expeditions_no_chart_figure, expeditions_members_chart_figure, expeditions_deaths_chart_figure, pie_termination_reasons_chart_figure
