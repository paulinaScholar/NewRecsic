from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from flask import session
from src.spotify import spotify_data
import traceback
# print("dashboard.py imported")


# --------------------------------------------------------------------
# Función de seguridad para obtener datos sin romper el dashboard
# --------------------------------------------------------------------
def safe_get(fn, sp, *args, **kwargs):
    try:
        return fn(sp, *args, **kwargs)
    except Exception as e:
        print(f"[dashboard] Error in {getattr(fn, '__name__', str(fn))}: {e}")
        traceback.print_exc()
        return None


# --------------------------------------------------------------------
# Figuras / Gráficos
# --------------------------------------------------------------------
def make_genres_figure(top_genres):
    if not top_genres:
        return go.Figure()

    names = [g.get("name", "") for g in top_genres]
    values = [g.get("count", 0) for g in top_genres]

    fig = px.pie(
        names=names,
        values=values,
        title="Top Géneros",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", y=-0.15)
    )
    return fig


def make_listening_days_graph(listening_days):
    if not listening_days:
        return go.Figure()

    days = list(listening_days.keys())
    counts = list(listening_days.values())

    fig = go.Figure(data=[go.Bar(x=days, y=counts)])
    fig.update_layout(
        title="Hábitos musicales",
        xaxis_title="Día",
        yaxis_title="Canciones escuchadas",
        height=360,
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig


def make_heatmap(listening_hours):
    if not listening_hours:
        return go.Figure()

    try:
        fig = px.imshow(
            listening_hours,
            labels=dict(x="Hora", y="Día", color="Canciones"),
            x=[f"{h}:00" for h in range(24)],
            y=["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"],
            color_continuous_scale="Greens",
            title="Mapa de calor de horas de escucha"
        )

        fig.update_layout(height=360, margin=dict(l=10, r=10, t=40, b=10))
        return fig

    except Exception as e:
        print("[dashboard] heatmap creation failed:", e)
        traceback.print_exc()
        return go.Figure()


# --------------------------------------------------------------------
# Tarjetas de estadísticas rápidas
# --------------------------------------------------------------------
def make_dashboard_cards(top_artist_today, monthly_listening, song_playcount):
    return {
        "artist_name": top_artist_today.get("artist") if top_artist_today else None,
        "artist_minutes": top_artist_today.get("minutes") if top_artist_today else None,
        "monthly_listening": monthly_listening or 0,
        "song": song_playcount.get("song") if song_playcount else None,
        "song_count": song_playcount.get("count") if song_playcount else None
    }


# --------------------------------------------------------------------
# Iniciales para el círculo tipo vinilo
# --------------------------------------------------------------------
def artist_initials(name: str):
    if not name:
        return "??"
    parts = name.split()
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


# --------------------------------------------------------------------
# Tarjeta tipo ticket “Recsumen”
# --------------------------------------------------------------------
def generate_ticket_component(sp):

    ticket = safe_get(spotify_data.get_ticket_data, sp) or {}

    top_genres = ticket.get("top_genres") or safe_get(spotify_data.get_top_genres, sp) or []
    top_artist_today = ticket.get("top_artist_today") or safe_get(spotify_data.get_top_artist_today, sp) or {}
    song_playcount = ticket.get("song_playcount") or safe_get(spotify_data.get_song_playcount, sp) or {}
    monthly_listening = ticket.get("monthly_listening") or safe_get(spotify_data.get_monthly_listening, sp) or 0
    top_tracks = safe_get(spotify_data.get_recently_played, sp, 10) or []

    table_rows = []
    for idx, track in enumerate(top_tracks, start=1):
        name = track.get("name", "Unknown")
        artist = track.get("artist", "Unknown")

        table_rows.append(
            html.Tr([
                html.Td(str(idx), style={"width": "6%", "fontWeight": "700"}),
                html.Td([
                    html.Div(name, style={"fontWeight": "600"}),
                    html.Div(artist, style={"fontSize": "0.85rem", "color": "#bfbfbf"})
                ]),
                html.Td("", style={"width": "14%"})
            ])
        )

    album_icon = html.Div(
        artist_initials(top_artist_today.get("artist")),
        style={
            "width": "84px",
            "height": "84px",
            "borderRadius": "50%",
            "backgroundColor": "#111",
            "color": "white",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "fontSize": "28px",
            "fontWeight": "700",
            "margin": "0 auto 10px auto",
            "boxShadow": "0 6px 18px rgba(0,0,0,0.6)"
        }
    )

    return dbc.Card(
        dbc.CardBody([
            html.Div([
                album_icon,
                html.H4("Recsumen", className="card-title text-center", style={"color": "white"}),

                html.P(
                    f"Artista del día: {top_artist_today.get('artist')} — {top_artist_today.get('minutes')} min"
                    if top_artist_today.get("artist") else "Artista del día: —",
                    style={"color": "#e8e8e8"}
                ),
                html.P(
                    f"Top canción: '{song_playcount.get('song')}' — {song_playcount.get('count')} reproducciones"
                    if song_playcount.get("song") else "Top canción: —",
                    style={"color": "#e8e8e8"}
                ),
                html.P(
                    "Top Géneros: " + (", ".join([g["name"] for g in top_genres]) if top_genres else "—"),
                    style={"color": "#cfcfcf"}
                ),

                html.Hr(style={"borderColor": "#2b2b2b"}),

                html.Table(
                    [html.Thead(html.Tr([
                        html.Th("QTY", style={"width": "6%"}),
                        html.Th("ITEM"),
                        html.Th("DUR.")
                    ], style={"color": "#cfcfcf"}))] +
                    table_rows +
                    [html.Tr([
                        html.Td("TOTAL", colSpan=2, style={"fontWeight": "700"}),
                        html.Td(str(len(top_tracks)), style={"fontWeight": "700"})
                    ])]
                )
            ], style={
                "backgroundColor": "#121212",
                "padding": "18px",
                "borderRadius": "14px",
                "boxShadow": "0 6px 20px rgba(0,0,0,0.7)"
            })
        ]),
        className="m-2",
        style={"border": "none"}
    )


# --------------------------------------------------------------------
# Layout del Dashboard
# --------------------------------------------------------------------
def dashboard_layout():
    print("[dashboard] Building layout...")

    # 🚨 CORREGIDO: ya no se pasa "session"
    sp_client = get_spotify_client()

    if not sp_client:
        print("[dashboard] No Spotify session detected ❌")
        return dbc.Container([
            html.H2("No has iniciado sesión con Spotify", className="text-center text-danger mt-5"),
            dbc.Button("Iniciar sesión con Spotify", href="/login_spotify",
                       color="success", className="d-block mx-auto mt-3")
        ])

    print("[dashboard] Spotify session detected ✅")

    ticket = safe_get(spotify_data.get_ticket_data, sp_client) or {}
    top_genres = ticket.get("top_genres") or safe_get(spotify_data.get_top_genres, sp_client) or []
    listening_days = safe_get(spotify_data.get_listening_days, sp_client) or {}
    listening_hours = safe_get(spotify_data.get_listening_hours, sp_client)
    top_artist_today = ticket.get("top_artist_today") or safe_get(spotify_data.get_top_artist_today, sp_client)
    monthly_listening = ticket.get("monthly_listening") or safe_get(spotify_data.get_monthly_listening, sp_client)
    song_playcount = ticket.get("song_playcount") or safe_get(spotify_data.get_song_playcount, sp_client)

    genres_fig = make_genres_figure(top_genres)
    listening_days_fig = make_listening_days_graph(listening_days)
    heatmap_fig = make_heatmap(listening_hours)
    cards = make_dashboard_cards(top_artist_today, monthly_listening, song_playcount)

    return html.Div(
        [
            dbc.Container(fluid=True, className="p-3", children=[

                html.H1("Spotify Dashboard", className="text-white bg-dark p-3 rounded"),

                dbc.Row([
                    dbc.Col(dcc.Graph(figure=genres_fig), md=6),
                    dbc.Col(dcc.Graph(figure=listening_days_fig), md=6)
                ]),

                html.Hr(),

                dbc.Row([dbc.Col(dcc.Graph(figure=heatmap_fig), md=12)]),

                html.Hr(),

                dbc.Row([
                    dbc.Col(dbc.Card(dbc.CardBody([
                        html.H5("Artista del día"),
                        html.P(f"{cards['artist_name']} — {cards['artist_minutes']} min"
                               if cards['artist_name'] else "—")
                    ])), md=4),
                    dbc.Col(dbc.Card(dbc.CardBody([
                        html.H5("Escucha mensual"),
                        html.P(f"{cards['monthly_listening']} minutos")
                    ])), md=4),
                    dbc.Col(dbc.Card(dbc.CardBody([
                        html.H5("Canción más escuchada"),
                        html.P(f"{cards['song']} — {cards['song_count']}"
                               if cards['song'] else "—")
                    ])), md=4)
                ]),

                html.Hr(),

                generate_ticket_component(sp_client),

                dbc.Button("Inicio", href="/", color="secondary", className="mt-3 d-block mx-auto")
            ])
        ],
        style={"backgroundColor": "#0f0f0f", "minHeight": "100vh"}
    )
