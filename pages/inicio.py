import dash 
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

inicio_layout = html.Div(
    className="inicio-container",
    children=[
        # Logo
        html.Div(
            className="logo-container",
            children=[
                html.Img(
                    src='/static/Recsic-11.png',
                    className="logo",
                    alt="Logo"
                )
            ]
        ),

        # Botones Cierre sesión y Perfil
        html.Div(
            className="header-buttons",
            children=[
                html.A(
                    html.Button("Perfil", type="button", className="button"),
                    href="/perfil",
                ),
                html.A(
                    html.Button("Cerrar sesión", type="button", className="button"),
                    href="/logout",
                ),
            ]
        ),

        html.Div(
            className="welcome-message",
            children=[
                html.H2("Bienvenido,"),
                html.P("Estás en tu página principal.")
            ]
        )
    ]
)