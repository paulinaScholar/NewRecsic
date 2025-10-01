import dash 
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

perfil_layout = html.Div(
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
                        html.Li([html.B("Nombre de usuario: "), "Nombre"]),
                        html.Li([html.B("Correo electrónico: "), "correo@mail.com"]),
                    ]
                )
            ]
        ),

        # Header buttons
        html.Div(
            className="header-buttons",
            children=[
                html.A(
                    html.Button("Volver a página principal", type="button", className="button volver justify-content-center"),
                    href="/inicio"  # you can handle routing with Dash Pages or callbacks
                )
            ]
        )
    ]
)