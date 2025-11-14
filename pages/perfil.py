import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from flask import session
from db import db_cursor
import psycopg2

def perfil_layout():
    # Si no hay sesión → redirigir
    if "user_id" not in session:
        return dcc.Location(href="/login", id="redirect-login")

    username = "Desconocido"
    user_id = session.get("user_id")

    try:
        with db_cursor() as cur:
            cur.execute("SELECT username FROM users WHERE id = %s", (user_id,))
            result = cur.fetchone()
            if result:
                username = result[0]
    except psycopg2.OperationalError:
        return html.Div(
            className="error-container",
            children=[
                html.H3("Error de conexión con la base de datos."),
                html.P("Por favor, intenta nuevamente más tarde."),
                html.A(html.Button("Volver al inicio", className="button-secondary"), href="/inicio")
            ]
        )
    except Exception as e:
        print("Error al obtener información del usuario:", e)
        return html.Div(
            className="error-container",
            children=[
                html.H3("Ocurrió un error inesperado."),
                html.A(html.Button("Volver al inicio", className="button-secondary"), href="/inicio")
            ]
        )

    # Layout principal
    return html.Div(
        className="principal",
        children=[
            html.H2("Perfil", className="profile-title"),

            html.Div(
                className="profile-info",
                children=[
                    html.Div([
                        html.H4(f"Bienvenido, {username}"),
                        html.P(f"Nombre de usuario: {username}"),
                        html.A(
                            html.Button("Cerrar sesión", type="button", className="button volver"),
                            href="/logout"
                        ),
                    ]),

                    html.Hr(),

                    html.H2("📜 Historial de listas guardadas", className="text-center my-4"),
                    html.Div(id="history-container"),
                    dcc.Interval(id="refresh-history", interval=60*1000, n_intervals=0)
                ]
            ),

            html.Div(
                className="header-buttons",
                children=[
                    html.A(
                        html.Button("Volver a página principal", type="button", className="button-secondary"),
                        href="/inicio"
                    )
                ]
            ),
        ]
    )

#-----------------------------------
# Callback para ver historial de rec
#-----------------------------------
@callback(
    Output("history-container", "children"),
    Input("refresh-history", "n_intervals")
)
def load_user_history(_):
    if "user_id" not in session:
        return dbc.Alert("Debes iniciar sesión para ver tu historial.", color="warning")

    user_id = session["user_id"]

    try:
        with db_cursor() as cur:
            cur.execute("""
                SELECT list_id, created_at, array_agg(track_name || ' — ' || artist_name) AS songs
                FROM user_recommendations
                WHERE user_id = %s
                GROUP BY list_id, created_at
                ORDER BY created_at DESC;
            """, (user_id,))
            results = cur.fetchall()

        if not results:
            return dbc.Alert("Aún no has guardado ninguna lista.", color="secondary")

        cards = []
        for list_id, created_at, songs in results:
            card = dbc.Card(
                dbc.CardBody([
                    html.H5(f"Lista del {created_at.strftime('%d/%m/%Y %H:%M')}", className="card-header text-white bg-secondary"),
                    html.Ul([html.Li(song) for song in songs]),
                    html.Small(f"ID: {list_id}", className="text-muted")
                ]),
                className="mb-3 shadow-sm card border-primary"
            )
            cards.append(card)

        return cards

    except Exception as e:
        print("Error al cargar historial:", e)
        return dbc.Alert("Error al cargar el historial.", color="danger")
