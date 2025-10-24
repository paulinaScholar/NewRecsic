from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from src.spotify.spotify_data import (
    get_top_genres, 
    get_top_podcasts, 
    get_listening_days,
    get_listening_hours,
    get_top_artist_today,
    get_monthly_listening,
    get_song_playcount,
    get_top_artists,
    get_recently_played
)

# Datos base
top_genres = get_top_genres()
top_podcasts = get_top_podcasts()
listening_days = get_listening_days()
listening_hours = get_listening_hours()
top_artist_today = get_top_artist_today()
monthly_listening = get_monthly_listening()
song_playcount = get_song_playcount()
top_artists = get_top_artists()
recently_played = get_recently_played()

# Procesar días de escucha
days, counts = (list(listening_days.keys()), list(listening_days.values())) if listening_days else ([], [])
listening_days_graph = {
    "data": [go.Bar(x=days, y=counts, marker=dict(color="#1DB954"))],
    "layout": go.Layout(title="Hábitos musicales", xaxis_title="Día", yaxis_title="Canciones escuchadas", height=400)
}

# Gráfico de géneros
genres_graph = px.pie(
    names=[genre["name"] for genre in top_genres],
    values=[genre["count"] for genre in top_genres],
    title="Top Géneros",
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.Blues
)

# Heatmap de horas
if listening_hours:
    heatmap_fig = px.imshow(
        listening_hours,
        labels=dict(x="Hora del día", y="Día de la semana", color="Canciones"),
        x=[f"{h}:00" for h in range(24)],
        y=["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"],
        color_continuous_scale="Greens",
        title="Mapa de calor de horas de escucha"
    )
else:
    heatmap_fig = go.Figure()

# Layout
dashboard_layout = html.Div([
    dbc.Container([
        dbc.Row([dbc.Col(
            html.H1("Spotify Dashboard", className="text-center text-white bg-dark p-4 mb-4 rounded"), width=12
        )]),

        dbc.Row([dbc.Col(dbc.Card([
            dbc.CardHeader("Dashboard Overview", className="bg-primary text-white"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=genres_graph), width=6, className="col-md-12"),
                    dbc.Col(dcc.Graph(figure=listening_days_graph), width=6, className="col-md-12")
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
                                    f"{top_artist_today['artist']} - {top_artist_today['minutes']} minutos escuchados" 
                                    if top_artist_today["artist"] else "Hoy no escuchaste música",
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
                                html.P(f"{monthly_listening} minutos de música este mes", className="card-text")
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
                                    f"'{song_playcount['song']}' - {song_playcount['count']} reproducciones" 
                                    if song_playcount["song"] else "No hay canción destacada todavía",
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
                                                f"Artista del día: {top_artist_today['artist']}" 
                                                if top_artist_today["artist"] else "Hoy no escuchaste música",
                                                className="text-center"
                                            ),
                                            html.H5(f"Escucha mensual: {monthly_listening} minutos", className="text-center"),
                                            html.H5(
                                                f"Canción más escuchada: '{song_playcount['song']}' ({song_playcount['count']} reproducciones)"
                                                if song_playcount["song"] else "No hay canción destacada",
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
                        html.Li(html.A(podcast["name"], href=podcast["link"], target="_blank", className="text-decoration-none text-primary")) 
                        for podcast in top_podcasts
                    ]), width=12)
                ]),
                html.Hr(),
                dbc.Row([dbc.Col(html.H3("Top 5 Artistas", className="text-center mb-3"), width=12)]),
                dbc.Row([dbc.Col(html.Ul([
                    html.Li(html.A(artist["name"], href=artist["link"], target="_blank", className="text-decoration-none text-success", style={"fontSize": "18px"})) 
                    for artist in top_artists
                ]), width=12)], className="mb-4"),

                dbc.Row([dbc.Col(html.H3("Escuchado Recientemente", className="text-center mb-3"), width=12)]),
                dbc.Row([dbc.Col(html.Ul([
                    html.Li(f"{track['name']} - {track['artist']}", style={"fontSize": "18px"}) for track in recently_played
                ]), width=12)], className="mb-4"),
            ])
        ], className="shadow mb-4"))]),

        dbc.Row([dbc.Col(dbc.Button("Inicio", href="/", color="secondary", className="mt-3"), width=12, className="text-center")])
    ], className="p-4")
])