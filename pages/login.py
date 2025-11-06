import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from db import db_cursor
import bcrypt
from flask import session
 
# from flask import session

# Login
# conn = get_db_conn(),
# cur = conn.cursor(),
# cur.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
# user = cur.fetchone()
# cur.close()
# conn.close()

# if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
#     session['logged_in'] = True
#     session['username'] = username
#     return "", "/main"
# else
#     return "Invalid username or password", '/'

# def login(n_clicks, usuario, contraseña):
#     if usuario == "admin" and contraseña == "1234":  # Example validation
#         return "✅ Inicio de sesión exitoso"
#     else:
#         return "❌ Usuario o contraseña incorrectos"

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

                # Nombre de usuario
                html.Label("Nombre de usuario", htmlFor="usuario"),
                dcc.Input(
                    id="usuario",
                    type="text", 
                    placeholder="Nombre de usuario",
                    className="input",
                ),

                # Contraseña
                html.Label("Contraseña", htmlFor="contraseña"),
                dcc.Input(
                    id="contraseña",
                    type="password", 
                    placeholder="Contraseña",
                    className="input",
                ),

                # Botones
                html.Div(
                    className="form-buttons",
                    children=[
                        html.Button("Iniciar sesión", className="button", id="btn-login", n_clicks=0),

                        html.A(
                            html.Button("Crear cuenta", className="button-secondary", type="button"),
                            href="/registro"
                        ),
                    ]
                ),

                dcc.Location(id="login-redirect", refresh=True)
            ]
        )
    ]
)

layout = login_layout

# Login
@dash.callback(
    Output("msg", "children"),
    Output("login-redirect", "href"),
    Input("btn-login", "n_clicks"),
    State("usuario", "value"),
    State("contraseña", "value"),
    prevent_initial_call=True
)

def validar_login(n_clicks, usuario, contraseña):
    if not usuario or not contraseña:
        return "Completa ambos campos", dash.no_update
    
    with db_cursor() as cur:
        cur.execute("SELECT id, username, password_hash FROM users WHERE username = %s", (usuario,))
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