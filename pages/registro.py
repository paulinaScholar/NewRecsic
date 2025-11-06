import dash 
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from db import db_cursor
import bcrypt
import psycopg2

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

        html.Label(id="registro-msg", className="msg"),
        html.Div(
            className="registro-box",
            children=[
                # Nombre de usuario
                html.Div(
                    className="form-group",
                    children=[
                        html.Label("Nombre de usuario", htmlFor="usuario"),
                        dcc.Input(
                            id="usuario", 
                            type="text", 
                            name="usuario",
                            placeholder="Escriba su usuario",
                            required=True
                        )
                    ]
                ),
                
                # # Correo electrónico
                # html.Div(
                #     className="form-group",
                #     children=[
                #         html.Label("Correo electrónico", htmlFor="email"),
                #         dcc.Input(
                #             id="email", 
                #             type="email", 
                #             name="email",
                #             placeholder="Escriba un correo electrónico",
                #             required=True
                #         )
                #     ]
                # ),

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
                    ]
                ),

                # Confirmar Contraseña
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
                    ]
                ),

                # Botones
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
                    ]
                ),
            ]
        ),
        html.A(
            html.Button("Iniciar Sesión", type="button", className="button-secondary"),
            href="/login",
            className="py-2"
        ),

        dcc.Interval(id="redirect-timer", interval=2000, n_intervals=0, disabled=True),
        dcc.Location(id="registro-redirect", refresh=True)
    ]
)

layout = registro_layout

@dash.callback(
    Output("registro-msg", "children"),
    Output("registro-msg", "className"),
    Output("redirect-timer", "disabled"),
    Input("btn-registro", "n_clicks"),
    State("usuario", "value"),
    # State("email", "value"),
    State("contraseña", "value"),
    State("contraseña_confirm", "value"),
    prevent_initial_call=True,
)
def registrar_usuario(n, usuario, contraseña, contraseña_confirm):
    if not usuario or not contraseña:
        return "Complete todos los campos.", "msg error", True
    
    if contraseña != contraseña_confirm:
        return "Las contraseñas no coinciden.", "msg error", True

    hashed_pw = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")

    try:
        with db_cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (username,  password_hash)
                VALUES (%s, %s)
                """,
                (usuario, hashed_pw),
            )
        return "Cuenta creada exitosamente. Redirigiendo al inicio de sesión...", "msg success", False

    except psycopg2.errors.UniqueViolation:
        # Handle duplicate usernames or emails
        return "El nombre de usuario ya está en uso.", "msg error", True

    except Exception as e:
        print("Error:", e)
        return "Ocurrió un error al crear la cuenta.", "msg error", True
    
@dash.callback(
    Output("registro-redirect", "href"),
    Input("redirect-timer", "n_intervals"),
    Input("redirect-timer", "disabled"),
    prevent_initial_call = True
)
def redirect_login(n, disabled):
    if not disabled and n > 0:
        return "/login"
    return dash.no_update