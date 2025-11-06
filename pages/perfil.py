import dash 
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from flask import session
from db import db_cursor
import psycopg2

# dash.register_page(__name__, path="/perfil")

def perfil_layout():
    if "user_id" not in session:
        return dcc.Location(href="/login", id="redirect-login")

    # User in session
    user_id = session["user_id"]

    username = "Desconocido"

    try:
        with db_cursor() as cur:
            cur.execute(
                "SELECT username FROM users WHERE id = %s",
                (user_id,)
            )
            result = cur.fetchone()
            if result: 
                username = result
    except psycopg2.Error as e:
        print("Error al obtener la informacion de usuario", e)

    return html.Div(
        className="principal",
        children=[

            # Profile header
            html.H2("Perfil", className="profile-title"),

            # User info
            html.Div(
                className="profile-info",
                children=[
                    html.Ul(
                        children=[
                            html.H4(f"Bienvenido, {username}", className=""),
                            html.Li([html.B("Nombre de usuario: "), username]),
                            # html.Li([html.B("Correo electrónico: "), "correo@mail.com"]),
                            html.A(
                                html.Button("Cerrar sesión", type="button", className="button volver justify-content-center"),
                                href="/logout"  # you can handle routing with Dash Pages or callbacks
                            )
                        ]
                    )
                ]
            ),

            # Header buttons
            html.Div(
                className="header-buttons",
                children=[
                    html.A(
                        html.Button("Volver a página principal", type="button", className="button-secondary justify-content-center"),
                        href="/inicio"  # you can handle routing with Dash Pages or callbacks
                    )
                ]
            )
        ]
    )