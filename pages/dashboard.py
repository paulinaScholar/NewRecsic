from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from flask import session
from src.spotify import spotify_data
import traceback
from src.spotify.spotify_auth import get_spotify_client

print("dashboard.py imported")

# --- Funciones auxiliares ---
def safe_get(fn, sp, *args, **kwargs):
    try:
        return fn(sp, *args, **kwargs)
    except Exception as e:
        print(f"[dashboard] Error in {fn.__name__}: {e}")
        traceback.print_exc()
        return None

def make_genres_figure(top_genres):
    if not top_genres:
        return go.Figure()
    names = [g.get("name", "") for g in top_genres]
    values = [g.get("count", 0) for g in top_genres]
    return px.pie(
        names=names, values=values, title="Top Géneros", hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues
    )

def make_listening_days_graph(listening_days):
    if not listening_days:
        return go.Figure()
    days = list(listening_days.keys())
    counts = list(listening_days.values())
    fig = go.Figure(data=[go.Bar(x=days, y=counts, marker=dict(color="#1DB954"))])
    fig.update_layout(title="Hábitos musicales", xaxis_title="Día", yaxis_title="Canciones escuchadas", height=400)
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
        return fig
    except Exception as e:
        print("[dashboard] heatmap creation failed:", e)
        traceback.print_exc()
        return go.Figure()

def make_dashboard_cards(top_artist_today, monthly_listening, song_playcount):
    return {
        "artist_name": top_artist_today.get("artist") if top_artist_today else None,
        "artist_minutes": top_artist_today.get("minutes") if top_artist_today else None,
        "monthly_listening": monthly_listening or 0,
        "song": song_playcount.get("song") if song_playcount else None,
        "song_count": song_playcount.get("count") if song_playcount else None
    }

# ---
def generate_ticket_component(sp):
    top_tracks = safe_get(spotify_data.get_top_tracks, sp, 10) or []
    top_artist_today = safe_get(spotify_data.get_top_artist_today, sp) or {}
    song_playcount = safe_get(spotify_data.get_song_playcount, sp) or {}
    top_genres = safe_get(spotify_data.get_top_genres, sp) or []

    # Crear filas de tracks
    table_rows = []
    for track in top_tracks:
        track_artists = ", ".join([a["name"] for a in track["artists"]])
        table_rows.append(
            html.Tr([
                html.Td(track["id"], style={"width": "5%"}),
                html.Td(f"{track['name']} - {track_artists}"),
                html.Td(f"{int(track['duration_ms']/60000)} min", style={"width": "15%"})
            ])
        )

    # Tarjeta estilo vinilo
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                # Circulo vinilo en el fondo
                html.Div(style={
                    "width": "100px",
                    "height": "100px",
                    "backgroundColor": "#222",
                    "borderRadius": "50%",
                    "margin": "0 auto 20px auto",
                    "boxShadow": "0 0 20px rgba(0,0,0,0.7)"
                }),
                html.H4("Recsumen", className="card-title text-center text-white"),
                html.Hr(style={"borderColor": "gray"}),
                html.P(
                    f"Artista del día: {top_artist_today.get('artist')} - {top_artist_today.get('minutes')} min"
                    if top_artist_today.get("artist") else "No escuchaste música hoy",
                    className="text-white"
                ),
                html.P(
                    f"Top canción: '{song_playcount.get('song')}' - {song_playcount.get('count')} reproducciones"
                    if song_playcount.get("song") else "Sin canción destacada",
                    className="text-white"
                ),
                html.P(
                    "Top Géneros: " + ", ".join([g["name"] for g in top_genres])
                    if top_genres else "Sin datos",
                    className="text-white"
                ),
                html.Hr(style={"borderColor": "gray"}),
                html.Table(
                    [html.Thead(html.Tr([
                        html.Th("QTY"), html.Th("ITEM"), html.Th("DURACIÓN")
                    ]))] +
                    table_rows +
                    [html.Tr([html.Td("TOTAL", colSpan=2), html.Td(f"{len(top_tracks)} tracks")])]
                )
            ], style={
                "backgroundColor": "#1e1e1e",
                "padding": "20px",
                "borderRadius": "15px",
                "boxShadow": "0 0 20px rgba(0,0,0,0.8)"
            })
        ]),
        className="m-3"
    )



# --- Layout del Dashboard ---
def dashboard_layout():
    print("[dashboard] Building layout...")
    sp_client = get_spotify_client()
    if not sp_client:
        print("[dashboard] No Spotify session detected ❌")
        return html.Div(
            dbc.Container([
                dbc.Row([dbc.Col(html.H2("No has iniciado sesión con Spotify",
                                         className="text-center text-danger mt-5"), width=12)]),
                dbc.Row([dbc.Col(html.A("Iniciar sesión con Spotify", href="/login_spotify", target="_blank",
                                        className="btn btn-success mt-3"), width=12, className="text-center")])
            ])
        )

    print("[dashboard] Spotify session detected ✅")
    try:
        top_genres = safe_get(spotify_data.get_top_genres, sp_client) or []
        listening_days = safe_get(spotify_data.get_listening_days, sp_client) or {}
        listening_hours = safe_get(spotify_data.get_listening_hours, sp_client) or None
        top_artist_today = safe_get(spotify_data.get_top_artist_today, sp_client) or {}
        monthly_listening = safe_get(spotify_data.get_monthly_listening, sp_client) or 0
        song_playcount = safe_get(spotify_data.get_song_playcount, sp_client) or {}
    except Exception as e:
        print("[dashboard] Error loading Spotify data:", e)
        traceback.print_exc()
        return html.Div("Error al cargar los datos del dashboard.")

    genres_fig = make_genres_figure(top_genres)
    listening_days_fig = make_listening_days_graph(listening_days)
    heatmap_fig = make_heatmap(listening_hours)
    cards = make_dashboard_cards(top_artist_today, monthly_listening, song_playcount)

    return html.Div([
        dbc.Container([
            dbc.Row([dbc.Col(html.H1("Spotify Dashboard", className="text-center text-white bg-dark p-4 mb-4 rounded"), width=12)]),
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader("Dashboard Overview", className="bg-primary text-white"),
                    dbc.CardBody([
                        dbc.Row([dbc.Col(dcc.Graph(figure=genres_fig), width=6),
                                 dbc.Col(dcc.Graph(figure=listening_days_fig), width=6)]),
                        html.Hr(),
                        dbc.Row([dbc.Col(dcc.Graph(figure=heatmap_fig), width=12)]),
                        html.Hr(),
                        dbc.Row([
                            dbc.Col(html.H3("Estadísticas Detalladas", className="text-center mb-4"), width=12),
                            dbc.Col(dbc.Card(dbc.CardBody([
                                html.H5("Artista del día", className="card-title"),
                                html.P(f"{cards['artist_name']} - {cards['artist_minutes']} minutos escuchados" if cards['artist_name'] else "Hoy no escuchaste música", className="card-text")
                            ]), className="shadow mb-3"), md=4),
                            dbc.Col(dbc.Card(dbc.CardBody([
                                html.H5("Escucha mensual", className="card-title"),
                                html.P(f"{cards['monthly_listening']} minutos de música este mes", className="card-text")
                            ]), className="shadow mb-3"), md=4),
                            dbc.Col(dbc.Card(dbc.CardBody([
                                html.H5("Canción más escuchada", className="card-title"),
                                html.P(f"'{cards['song']}' - {cards['song_count']} reproducciones" if cards['song'] else "No hay canción destacada todavía", className="card-text")
                            ]), className="shadow mb-3"), md=4),
                        ]),
                        html.Hr(),
                        dbc.Row([dbc.Col(generate_ticket_component(sp_client), width=12)])
                    ])
                ], className="shadow mb-4"))
            ]),
            dbc.Row([dbc.Col(dbc.Button("Inicio", href="/", color="secondary", className="mt-3"), width=12, className="text-center")])
        ], className="p-4")
    ])
