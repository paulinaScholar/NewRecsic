import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import bcrypt

# Try to import db safely (so the app still loads if DB is down)
try:
    from db import db_cursor
    import psycopg2
    DB_AVAILABLE = True
except Exception as e:
    print(f"[REGISTRO] Database import failed: {e}")
    DB_AVAILABLE = False


# ---------- Layout ----------
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
            ],
        ),

        html.H2("Crear cuenta", className="form-title"),

        html.Label(id="registro-msg", className="msg"),
        html.Div(
            className="registro-box",
            children=[
                # Usuario
                html.Div(
                    className="form-group",
                    children=[
                        html.Label("Nombre de usuario", htmlFor="usuario"),
                        dcc.Input(
                            id="usuario",
                            type="text",
                            name="usuario",
                            placeholder="Escriba su usuario",
                            required=True,
                        ),
                    ],
                ),

                # Contraseña
                html.Div(
                    className="form-group",
                    children=[
                        html.Label("Contraseña", htmlFor="contraseña"),
                        dcc.Input(
                            id="contraseña",
                            type="password",
                            name="contraseña",
                            placeholder="Contraseña",
                            required=True,
                        ),
                    ],
                ),

                # Confirmar contraseña
                html.Div(
                    className="form-group",
                    children=[
                        html.Label("Confirmar contraseña", htmlFor="contraseña_confirm"),
                        dcc.Input(
                            id="contraseña_confirm",
                            type="password",
                            name="contraseña_confirm",
                            placeholder="Repetir contraseña",
                            required=True,
                        ),
                    ],
                ),

                # Botón registrar
                html.Div(
                    className="form-buttons",
                    children=[
                        html.Button(
                            "Registrarse",
                            id="btn-registro",
                            type="submit",
                            className="button submit",
                            n_clicks=0,
                        ),
                    ],
                ),
            ],
        ),

        # Botón iniciar sesión
        html.A(
            html.Button("Iniciar Sesión", type="button", className="button-secondary"),
            href="/login",
            className="py-2",
        ),

        dcc.Interval(id="redirect-timer", interval=2000, n_intervals=0, disabled=True),
        dcc.Location(id="registro-redirect", refresh=True),
    ],
)

layout = registro_layout


# ---------- Callback: Registro ----------
@callback(
    Output("registro-msg", "children"),
    Output("registro-msg", "className"),
    Output("redirect-timer", "disabled"),
    Input("btn-registro", "n_clicks"),
    State("usuario", "value"),
    State("contraseña", "value"),
    State("contraseña_confirm", "value"),
    prevent_initial_call=True,
)
def registrar_usuario(n, usuario, contraseña, contraseña_confirm):
    # Validaciones básicas
    if not usuario or not contraseña or not contraseña_confirm:
        return "Complete todos los campos.", "msg error", True

    if contraseña != contraseña_confirm:
        return "Las contraseñas no coinciden.", "msg error", True

    if not DB_AVAILABLE:
        return "Base de datos no disponible. Inténtalo más tarde.", "msg error", True

    hashed_pw = bcrypt.hashpw(contraseña.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    try:
        with db_cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (username, password_hash)
                VALUES (%s, %s)
                """,
                (usuario, hashed_pw),
            )
        return "Cuenta creada exitosamente. Redirigiendo al inicio de sesión...", "msg success", False

    except Exception as e:
        # Handle duplicate usernames and database issues
        error_text = str(e)
        print(f"[REGISTRO ERROR] {error_text}")

        if "unique" in error_text.lower():
            return "El nombre de usuario ya está en uso.", "msg error", True

        return "Ocurrió un error al crear la cuenta. Inténtalo más tarde.", "msg error", True


# ---------- Callback: Redirección ----------
@callback(
    Output("registro-redirect", "href"),
    Input("redirect-timer", "n_intervals"),
    State("redirect-timer", "disabled"),
    prevent_initial_call=True,
)
def redirect_login(n, disabled):
    if not disabled and n > 0:
        return "/login"
    return dash.no_update
