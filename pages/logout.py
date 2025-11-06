import dash 
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from flask import session

# dash.register_page(__name__, path="/logout")

def logout_layout():
    session.clear()
    return html.Div([
        html.H3("Cerrando sesión..."),
        html.Div(
            className="logo-container",
            children=[
                html.Img(
                    src="/static/Recsic-09.png",  
                    className="logo",
                    alt="Logo",                    
                )
            ]
        ),
        dcc.Location(href="/login", id="redirect-home")
    ])