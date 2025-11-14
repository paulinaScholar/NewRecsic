from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages.recommendations import recommendations_layout
# from pages.home import home_layout
# from pages.dashboard import dashboard_layout
from pages.generator import generator_layout
from pages.login import login_layout
from pages.registro import registro_layout
from pages.inicio import inicio_layout
from pages.perfil import perfil_layout
from pages.navbar import navbar
from pages.logout import logout_layout
import pandas as pd
from db import engine
from sqlalchemy import text
from flask import session
from datetime import timedelta
import os


external_stylesheets = [
    dbc.themes.PULSE,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
]

app = Dash(
    __name__, 
    external_stylesheets=external_stylesheets, 
    suppress_callback_exceptions=True,
    title="Recsic"
)

# Sessions flask server
server = app.server

# server.secret_key = os.urandom(24)
server.secret_key = os.getenv("SECRET_KEY")

# Configure session behavior
server.config["SESSION_TYPE"] = "filesystem"
server.config["SESSION_FILE_DIR"] = "/tmp/flask_sessions"
server.config["SESSION_PERMANENT"] = True
server.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)

# print("reached layout")
# app.layout = html.Div("App started successfully")

app.layout = html.Div([
    dcc.Location(id='url', refresh=False), 
    navbar,
    html.Div(id='page-content')
])

# Routing
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)

def display_page(pathname):
    match pathname:
        case '/recommendations':
            return recommendations_layout 
        # case '/dashboard':
        #         return dashboard_layout()
        case '/generator':
              return generator_layout
        case '/login':
              return login_layout 
        case '/registro':
              return registro_layout 
        case '/inicio':
              return inicio_layout
        case '/perfil':
              return perfil_layout()
        case '/logout':
              return logout_layout()
        # case '/home':
        #       return home_layout
        case _:
            return inicio_layout 

# DB CONNECTION
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("Connection successful!")
        print("PostgreSQL version:", result.scalar())
except Exception as e:
    print("Connection failed:", e)


if __name__ == "__main__":
    # SOLO para desarrollo local
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )
    # app.run(debug=True) # use for development
