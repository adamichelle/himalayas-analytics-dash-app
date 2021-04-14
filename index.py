import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import server
from app import app
# import all pages in the app
from apps import expeditions_info, home, members_info

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/pangong-tso.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("Himalayas Dashboard", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/home",
            )
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/expeditions_info':
        return expeditions_info.layout
    elif pathname == '/members_info':
        return members_info.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)