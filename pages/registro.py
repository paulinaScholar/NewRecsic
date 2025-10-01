import dash 
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

registro_layout = html.Div(
    className="registro-container",
    children=[
        html.Div(
            className="logo-container",
            children=[
                html.Img(
                    src="/static/Recsic-09.png",
                    className="logo",
                    alt="Logo",
                ),
            ]
        ),

        html.H2("Crear cuenta", className="form-title"),

        # Nombre de usuario
        html.Div(
            className="form-group",
            children=[
                html.Label("Nombre de usuario", htmlFor="usuario"),
                dcc.Input(
                    type="text", name="usuario",
                    placeholder="Escriba su nombre de usuario",
                    id="usuario", required=True,
                )
            ]
        ),
        
        # Correo electrónico
        html.Div(
            className="form-group",
            children=[
                html.Label("Correo electrónico", htmlFor="email"),
                dcc.Input(
                    type="email", name="email",
                    placeholder="Escriba un correo electrónico",
                    id="email", required=True
                )
            ]
        ),

        # Contraseña
        html.Div(
            className="form-group",
            children=[
                html.Label("Contraseña", htmlFor="contraseña"),
                dcc.Input(
                    type="password", name="contraseña",
                    placeholder="Contraseña",
                    id="contraseña", required=True,
                ),
            ]
        ),

        html.Div(
            className="form-buttons",
            children=[
                html.A(
                    html.Button("Iniciar Sesión", type="button", className="button")
                ),
                html.Button("Registrarse", type="submit", className="button submit", n_clicks=0),
            ]
        )
    ]
)