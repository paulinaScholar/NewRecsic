import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from flask import session
import bcrypt

# Import DB utilities safely
try:
    from db import db_cursor
    DB_AVAILABLE = True
except Exception as e:
    print(f"[LOGIN] Database import failed: {e}")
    DB_AVAILABLE = False


# ---------- Layout ----------
login_layout = html.Div(
    className="login-container",
    children=[
        html.Div(
            className="logo-container",
            children=[
                html.Img(src="/static/Recsic-09.png", className="logo", alt="Logo"),
            ],
        ),

        html.Div(
            className="login-box",
            children=[
                html.H2("Inicia sesión"),
                html.Div(className="msg", id="msg"),

                html.Label("Nombre de usuario", htmlFor="usuario"),
                dcc.Input(
                    id="usuario",
                    type="text",
                    placeholder="Nombre de usuario",
                    className="input",
                ),

                html.Label("Contraseña", htmlFor="contraseña"),
                dcc.Input(
                    id="contraseña",
                    type="password",
                    placeholder="Contraseña",
                    className="input",
                ),

                html.Div(
                    className="form-buttons",
                    children=[
                        html.Button("Iniciar sesión", className="button", id="btn-login", n_clicks=0),
                        html.A(
                            html.Button("Crear cuenta", className="button-secondary", type="button"),
                            href="/registro",
                        ),
                    ],
                ),
                dcc.Location(id="login-redirect", refresh=True),
            ],
        ),
    ],
)

layout = login_layout


# ---------- Callback ----------
@callback(
    Output("msg", "children"),
    Output("login-redirect", "href"),
    Input("btn-login", "n_clicks"),
    State("usuario", "value"),
    State("contraseña", "value"),
    prevent_initial_call=True,
)
def validar_login(n_clicks, usuario, contraseña):
    # Basic field check
    if not usuario or not contraseña:
        return "Completa ambos campos.", dash.no_update

    # Database not loaded
    if not DB_AVAILABLE:
        return "Base de datos no disponible. Inténtalo más tarde.", dash.no_update

    try:
        with db_cursor() as cur:
            cur.execute(
                "SELECT id, username, password_hash FROM users WHERE username = %s",
                (usuario,),
            )
            user = cur.fetchone()

        if not user:
            return "Usuario o contraseña incorrecta.", dash.no_update

        user_id, username, password_hash = user

        if bcrypt.checkpw(contraseña.encode(), password_hash.encode()):
            session["user_id"] = user_id
            session["username"] = username
            return "", "/inicio"
        else:
            return "Usuario o contraseña incorrecta.", dash.no_update

    except Exception as e:
        print(f"[LOGIN ERROR] {e}")
        return "Error de conexión con la base de datos.", dash.no_update
