from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from src.spotify import spotify_data 
import traceback
print("dashboard.py imported")

def safe_get(fn, *args, **kwargs):
    """Call a data function and return None on error (and log)."""
    try:
        return fn(*args, **kwargs)
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
        names=names,
        values=values,
        title="Top Géneros",
        hole=0.4,
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
            labels=dict(x="Hora del día", y="Día de la semana", color="Canciones"),
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
    # safe extraction
    artist_name = None
    artist_minutes = None
    if top_artist_today and isinstance(top_artist_today, dict):
        artist_name = top_artist_today.get("artist")
        artist_minutes = top_artist_today.get("minutes")

    song = None
    song_count = None
    if song_playcount and isinstance(song_playcount, dict):
        song = song_playcount.get("song")
        song_count = song_playcount.get("count")

    return {
        "artist_name": artist_name,
        "artist_minutes": artist_minutes,
        "monthly_listening": monthly_listening or 0,
        "song": song,
        "song_count": song_count
    }

def dashboard_layout():
    print("[dashboard] building layout (loading data)")


    try:
        print("calling get_top_genres ")
    # Lazy load data — failures are caught by safe_get
        top_genres = safe_get(spotify_data.get_top_genres) or []
        print("top genres done: ", len(top_genres))
    except:
        print("[dashboard] failed early",e )
        traceback.print_exc()
        return html.Div("Early dashboard failure")

    top_podcasts = safe_get(spotify_data.get_top_podcasts) or []
    listening_days = safe_get(spotify_data.get_listening_days) or {}
    listening_hours = safe_get(spotify_data.get_listening_hours) or None
    top_artist_today = safe_get(spotify_data.get_top_artist_today) or {}
    monthly_listening = safe_get(spotify_data.get_monthly_listening) or 0
    song_playcount = safe_get(spotify_data.get_song_playcount) or {}
    top_artists = safe_get(spotify_data.get_top_artists) or []
    recently_played = safe_get(spotify_data.get_recently_played) or []

    # Build figures
    try:
        genres_fig = make_genres_figure(top_genres)
    except Exception as e:
        print("[dashboard] genres_fig error:", e)
        genres_fig = go.Figure()

    listening_days_fig = make_listening_days_graph(listening_days)
    heatmap_fig = make_heatmap(listening_hours)

    cards = make_dashboard_cards(top_artist_today, monthly_listening, song_playcount)

    # Build layout
    try:
        layout = html.Div([
            dbc.Container([
                dbc.Row([dbc.Col(
                    html.H1("Spotify Dashboard", className="text-center text-white bg-dark p-4 mb-4 rounded"), width=12
                )]),

                dbc.Row([dbc.Col(dbc.Card([
                    dbc.CardHeader("Dashboard Overview", className="bg-primary text-white"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(dcc.Graph(figure=genres_fig), width=6, className="col-md-12"),
                            dbc.Col(dcc.Graph(figure=listening_days_fig), width=6, className="col-md-12")
                        ]),
                        html.Hr(),

                        dbc.Row([dbc.Col(dcc.Graph(figure=heatmap_fig), width=12)]),
                        html.Hr(),

                        dbc.Row([
                            dbc.Col(html.H3("Estadísticas Detalladas", className="text-center mb-4"), width=12),

                            # Card 1: Top Artist Today
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H5("Artista del día", className="card-title"),
                                        html.P(
                                            f"{cards['artist_name']} - {cards['artist_minutes']} minutos escuchados" 
                                            if cards['artist_name'] else "Hoy no escuchaste música",
                                            className="card-text"
                                        )
                                    ]),
                                    className="shadow mb-3"
                                ),
                                md=4
                            ),

                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H5("Escucha mensual", className="card-title"),
                                        html.P(f"{cards['monthly_listening']} minutos de música este mes", className="card-text")
                                    ]),
                                    className="shadow mb-3"
                                ),
                                md=4
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H5("Canción más escuchada", className="card-title"),
                                        html.P(
                                            f"'{cards['song']}' - {cards['song_count']} reproducciones" 
                                            if cards['song'] else "No hay canción destacada todavía",
                                            className="card-text"
                                        )
                                    ]),
                                    className="shadow mb-3"
                                ),
                                md=4
                            ),
                        ]),
                        html.Hr(),
                        dbc.Row(
                            className="justify-content-center my-5",
                            children=[
                                dbc.Col(
                                    html.Div(
                                        style={
                                            "background-image": "url('/static/disco.png')",
                                            "background-size": "cover",
                                            "background-position": "center",
                                            "height": "650px",
                                            "border-radius": "20px",
                                            "position": "relative",
                                            "display": "flex",
                                            "align-items": "center",
                                            "justify-content": "center",
                                            "color": "white",
                                            "text-shadow": "2px 2px 5px rgba(0,0,0,0.8)",
                                            "box-shadow": "0 8px 20px rgba(0,0,0,0.5)"
                                        },
                                        children=[
                                            html.Div(
                                                [
                                                    html.H2("Mi Álbum Musical", className="fw-bold text-center mb-3"),
                                                    html.H4(
                                                        f"Artista del día: {cards['artist_name']}" 
                                                        if cards['artist_name'] else "Hoy no escuchaste música",
                                                        className="text-center"
                                                    ),
                                                    html.H5(f"Escucha mensual: {cards['monthly_listening']} minutos", className="text-center"),
                                                    html.H5(
                                                        f"Canción más escuchada: '{cards['song']}' ({cards['song_count']} reproducciones)"
                                                        if cards['song'] else "No hay canción destacada",
                                                        className="text-center"
                                                    ),
                                                ],
                                                style={
                                                    "background-color": "rgba(0, 0, 0, 0.5)",
                                                    "padding": "25px",
                                                    "border-radius": "15px"
                                                }
                                            )
                                        ]
                                    ),
                                    md=8
                                )
                            ]
                        ),

                        dbc.Row([
                            dbc.Col(html.H3("Top Podcasts", className="text-center mb-3"), width=12),
                            dbc.Col(html.Ul([
                                html.Li(html.A(podcast.get("name", "unknown"), href=podcast.get("link", "#"), target="_blank", className="text-decoration-none text-primary")) 
                                for podcast in top_podcasts
                            ]), width=12)
                        ]),
                        html.Hr(),
                        dbc.Row([dbc.Col(html.H3("Top 5 Artistas", className="text-center mb-3"), width=12)]),
                        dbc.Row([dbc.Col(html.Ul([
                            html.Li(html.A(artist.get("name", "unknown"), href=artist.get("link", "#"), target="_blank", className="text-decoration-none text-success", style={"fontSize": "18px"})) 
                            for artist in top_artists
                        ]), width=12)], className="mb-4"),

                        dbc.Row([dbc.Col(html.H3("Escuchado Recientemente", className="text-center mb-3"), width=12)]),
                        dbc.Row([dbc.Col(html.Ul([
                            html.Li(f"{track.get('name','?')} - {track.get('artist','?')}", style={"fontSize": "18px"}) for track in recently_played
                        ]), width=12)], className="mb-4"),
                    ])
                ], className="shadow mb-4"))]),

                dbc.Row([dbc.Col(dbc.Button("Inicio", href="/", color="secondary", className="mt-3"), width=12, className="text-center")])
            ], className="p-4")
        ])
        print("[dashboard] layout built successfully")
        return layout

    except Exception as e:
        print("[dashboard] layout build failed:", e)
        traceback.print_exc()
        return html.Div([
            html.H2("Error building dashboard"),
            html.Pre(str(e)),
        ])
