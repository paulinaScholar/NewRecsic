import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from flask import session
from db import db_cursor
import psycopg2

def perfil_layout():
    # If session not set → redirect safely
    if "user_id" not in session:
        return dcc.Location(href="/login", id="redirect-login")

    username = "Desconocido"
    user_id = session.get("user_id")

    try:
        with db_cursor() as cur:
            cur.execute("SELECT username FROM users WHERE id = %s", (user_id,))
            result = cur.fetchone()
            if result:
                username = result[0]  # extract string instead of tuple
    except psycopg2.OperationalError:
        # Database unavailable — safe message
        return html.Div(
            className="error-container",
            children=[
                html.H3("Error de conexión con la base de datos."),
                html.P("Por favor, intenta nuevamente más tarde."),
                html.A(
                    html.Button("Volver al inicio", className="button-secondary"),
                    href="/inicio"
                )
            ]
        )
    except Exception as e:
        # Unexpected error
        print("Error al obtener información del usuario:", e)
        return html.Div(
            className="error-container",
            children=[
                html.H3("Ocurrió un error inesperado."),
                html.A(
                    html.Button("Volver al inicio", className="button-secondary"),
                    href="/inicio"
                )
            ]
        )

    # Regular profile layout
    return html.Div(
        className="principal",
        children=[
            html.H2("Perfil", className="profile-title"),

            html.Div(
                className="profile-info",
                children=[
                    html.Ul(
                        children=[
                            html.H4(f"Bienvenido, {username}", className=""),
                            html.Li([html.B("Nombre de usuario: "), username]),
                            html.A(
                                html.Button("Cerrar sesión", type="button", className="button volver justify-content-center"),
                                href="/logout"
                            ),
                        ]
                    )
                ],
            ),

            html.Div(
                className="header-buttons",
                children=[
                    html.A(
                        html.Button("Volver a página principal", type="button", className="button-secondary justify-content-center"),
                        href="/inicio"
                    )
                ]
            ),
        ]
    )
