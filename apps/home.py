import dash_html_components as html
import dash_bootstrap_components as dbc

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to the Himalayas expeditions dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='This is a visualization project form COMP 8157 using Plotly, Dash and Bootstrap! '
                                     )
                    , className="mb-4")
            ]),

        html.A("Special thanks to Eucalyp on Flaticon for the icon in Himalayas Dashboard's logo.",
               href="https://www.flaticon.com/authors/eucalyp", className="text-center")
    ])

])

#<div>Icons made by <a href="https://www.flaticon.com/authors/eucalyp" title="Eucalyp">Eucalyp</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>