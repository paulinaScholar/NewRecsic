import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc

def login(n_clicks, usuario, contraseña):
    if usuario == "admin" and contraseña == "1234":  # Example validation
        return "✅ Inicio de sesión exitoso"
    else:
        return "❌ Usuario o contraseña incorrectos"

login_layout = html.Div(
    className="login-container",
    children=[
        # Logo
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

        # Login content
        html.Div(
            className="login-box",
            children=[
                html.H2("Inicia sesión"),
                html.Div(className="msg", id="msg"),

                html.Div([
                        # Nombre de usuario
                        html.Label("Nombre de usuario", htmlFor="usuario"),
                        dcc.Input(
                            type="text", name="usuario", 
                            placeholder="Nombre de usuario", 
                            id="usuario", required=True,
                        ),

                        # Contraseña
                        html.Label("Contraseña", htmlFor="contraseña"),
                        dcc.Input(
                            type="password", name="contraseña",
                            placeholder="Contraseña",
                            id="contraseña", required=True,
                        ),

                        html.Div(
                            className="form-buttons",
                            children=[
                                html.A(
                                    html.Button("Crear cuenta", className="button", type="button"),
                                    href="/registro"
                                ),

                                html.Button("Iniciar sesión", className="button", id="btn-login", n_clicks=0),
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)