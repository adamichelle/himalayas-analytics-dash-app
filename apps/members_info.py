import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

load_dotenv()

from app import app

from dataframes import df_members
from dataframes import df_members_wo_dual_citizenship
from dataframes import df_members_dual_citizenship
from dataframes import df_members_death_cause
from geocode_helper import findGeocode


MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')

df_members.sort_values("year", inplace=True)

years_dropdown_options = []
year_names = df_members['year'].value_counts(dropna=False).keys().tolist()
year_names.sort(reverse=True)

for year in year_names:
    if(year == "Unknown"):
        break
    years_dropdown_options.append({"label": year, "value": year})

data = df_members.query("year == 2019")

layout = html.Div(
    children=[
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H1(children='Himalayas Expeditions Members Analytics'), className="mb-2")
            ]),
            dbc.Row([
                dbc.Col(html.P(children='Visualising info on expeditions members by season in the Himalayas from 1920s - 2010s'), className="mb-4")
            ]),
            dbc.Row([
                dcc.Dropdown(
                    id='years-filter',
                    options=years_dropdown_options,
                    value='2019',
                    style={'width': '50%'},
                    clearable=False,
                    className="mb-2"
                ),
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id="members-citizenship-chart", config={"displayModeBar": True},
                    ),
                    className="card mb-3",
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id="pie-members-sexes-chart", config={"displayModeBar": False},
                    ),
                    className="card mb-3",
                ),
                dbc.Col(
                    dcc.Graph(
                        id="members-sexes-by-seasons-chart", config={"displayModeBar": False},
                    ),
                    className="card mb-3",
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id="pie-death-causes-chart", config={"displayModeBar": False},
                    ),
                    className="card mb-3",
                ),
            ]),
        ])
    ]
)

@app.callback(
    [
        Output("members-citizenship-chart", "figure"),
        Output("pie-members-sexes-chart", "figure"),
        Output("members-sexes-by-seasons-chart", "figure"),
        Output("pie-death-causes-chart", "figure")
    ],
    [
        Input("years-filter", "value")
    ],
)
def update_charts(year):
    query = "year == {year}".format(year = year)
    data_map = df_members_wo_dual_citizenship.query(query)
    data = df_members.query(query)
    data_death_causes = df_members_death_cause.query(query)
    
    members_sexes = data["sex"].value_counts().to_frame().reset_index()
    members_sexes.columns = ["sex", "number_of_members"]

    data_copy = data[["season", "sex"]]
    data_copy['is_male'] = np.where(data_copy['sex'] == 'M', True, False)
    data_copy['is_female'] = np.where(data_copy['sex'] == 'F', True, False)
    data_copy.drop(['sex'], axis = 1, inplace = True)
    sexes_by_seasons = data_copy.groupby("season").sum().reset_index()

    death_causes = data_death_causes["death_cause"].value_counts().to_frame().reset_index()
    death_causes.columns = ["cause", "no_of_deaths"]

    member_citizenships_chart_figure = go.Figure(go.Scattermapbox(
        lat=data_map["latitude"].tolist(),
        lon=data_map["longitude"].tolist(),
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=data_map["member_id"].tolist(),
    ))

    member_citizenships_chart_figure.update_layout(
        title='Citizenships of Expendition Members',
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
        ),
    )
    
    pie_members_sexes_chart_figure = px.pie(members_sexes, values=members_sexes["number_of_members"], names=members_sexes["sex"], title='Sex Ratios of Expeditions Members')

    members_sexes_by_seasons_chart_figure = go.Figure()
    members_sexes_by_seasons_chart_figure.add_trace(go.Bar(
        x=sexes_by_seasons["season"].tolist(),
        y=sexes_by_seasons["is_male"].tolist(),
        name='Male Expendition Members',
        marker_color='lightsalmon'
    ))
    members_sexes_by_seasons_chart_figure.add_trace(go.Bar(
        x=sexes_by_seasons["season"].tolist(),
        y=sexes_by_seasons["is_female"].tolist(),
        name='Female Expendition Members',
        marker_color='indianred'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    members_sexes_by_seasons_chart_figure.update_layout(
        barmode='group',
        title={
            'text': "Expendition Members Sex Numbers By Seasons",
            'y':0.1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'bottom'
        },
        legend_title_text='Sex',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    )

    pie_death_causes_chart_figure = px.pie(death_causes, values=death_causes["no_of_deaths"], names=death_causes["cause"], title='Death Cause Ratios of Expeditions Members That Died')


    return member_citizenships_chart_figure, pie_members_sexes_chart_figure, members_sexes_by_seasons_chart_figure, pie_death_causes_chart_figure
