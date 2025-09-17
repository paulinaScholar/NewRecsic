from dash import html, dcc
import dash_bootstrap_components as dbc
from src.spotify.spotify_data import get_top_artists, get_listening_days, get_recently_played
import plotly.graph_objs as go

# Obtener datos desde Spotify API
top_artists = get_top_artists()
listening_days = get_listening_days()
recently_played = get_recently_played()

# Procesar datos para gráficos
days, counts = (list(listening_days.keys()), list(listening_days.values())) if listening_days else ([], [])

# Gráfico de días más escuchados
listening_days_graph = {
<<<<<<< HEAD
    "data": [go.Bar(x=days, y=counts, marker=dict(color="blue"))],
    "layout": go.Layout(title="Listening Habits 📆", xaxis_title="Day", yaxis_title="Songs Played", height=400)
}

# Layout de la página principal (Home)
home_layout = html.Div([
    dbc.Container([
        dbc.Row([dbc.Col(html.H1("Spotify Music Dashboard 🎶"), width=12, className="text-center")], className="mb-4"),
        dbc.Row([dbc.Col(html.P("Welcome! View your top songs, artists, and recommendations."), width=12)], className="mb-3"),

        # Añadir un nuevo botón "Dashboard" junto a "Get Recommendations"
        dbc.Row([
            dbc.Col(dbc.Button("🎧 Get Recommendations", href="/recommendations", color="primary", size="lg"), width={"size": 6, "offset": 3}),
            dbc.Col(dbc.Button("📊 Dashboard", href="/dashboard", color="secondary", size="lg"), width={"size": 6, "offset": 0}),
            dbc.Col(dbc.Button("Generator", href="/generator", color="secondary", size="lg"), width={"size": 6, "offset": 0})
        ], className="mb-4 text-center"),

        html.Hr(),

        # About Section
        dbc.Row([dbc.Col(html.H3("About"), width=12)]),
        dbc.Row([
            dbc.Col([html.P("Recsic is very simple to use! Go to the 'Recommend' page, enter the name of a song and Recsic will generate a list of 10 similar songs."),
                     html.P("We are still under development so make sure to come back later!")], width=6),
            dbc.Col(html.Img(src="/assets/spotify.png", style={"max-width": "50px"}), width=6)
        ], className="mb-4"),

        html.Hr(),

        # Stats Section
        dbc.Row([dbc.Col(html.H3("Your Listening Stats 📊"), width=12, className="text-center")], className="mb-4"),

        # Top Artists
        dbc.Row([dbc.Col(html.H4("Top 5 Artists 🎤"), width=12, className="text-center")], className="mb-3"),
        dbc.Row([dbc.Col(html.Ul([html.Li(html.A(artist["name"], href=artist["link"], target="_blank", style={"fontSize": "18px"})) for artist in top_artists]), width=12)], className="mb-4"),

        # Recently Played Songs
        dbc.Row([dbc.Col(html.H3("Recently Played 🎵"), width=12, className="text-center")], className="mb-4"),
        dbc.Row([dbc.Col(html.Ul([html.Li(f"{track['name']} - {track['artist']} ", style={"fontSize": "18px"}) for track in recently_played]), width=12)], className="mb-4"),

        html.Hr(),

        # Skills Section
        dbc.Row([dbc.Col(html.H3("Music Attributes 🎼"), width=12)]),
        dbc.Row([
            dbc.Col(html.Div([html.H6("Acousticness", style={"color": "#6f42c1"}), html.P("A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence.")]), width=4),
            dbc.Col(html.Div([html.H6("Danceability", style={"color": "#6f42c1"}), html.P("Describes how suitable a track is for dancing. A value of 0.0 is least danceable and 1.0 is most danceable.")]), width=4),
            dbc.Col(html.Div([html.H6("Energy", style={"color": "#6f42c1"}), html.P("A measure from 0.0 to 1.0 representing intensity and activity. Energetic tracks feel fast, loud, and noisy.")]), width=4),
        ], className="mb-3"),

        dbc.Row([
            dbc.Col(html.Div([html.H6("Instrumentalness", style={"color": "#6f42c1"}), html.P("Predicts whether a track contains no vocals. A value closer to 1.0 means higher likelihood of no vocals.")]), width=4),
            dbc.Col(html.Div([html.H6("Loudness", style={"color": "#6f42c1"}), html.P("The overall loudness of a track in decibels (dB). Values typically range between -60 and 0 dB.")]), width=4),
            dbc.Col(html.Div([html.H6("Valence", style={"color": "#6f42c1"}), html.P("A measure from 0.0 to 1.0 describing musical positiveness. Higher values indicate a happier tone.")]), width=4),
        ], className="mb-3"),

        html.Hr(),
    ], className="mt-4")
])
=======
    "data": [go.Bar(x=days, y=counts, marker=dict(color="#1DB954"))],
    "layout": go.Layout(
        title="Listening Habits 📆",
        xaxis_title="Day",
        yaxis_title="Songs Played",
        height=400,
        margin=dict(t=40, l=40, r=40, b=40),
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9"
    )
}

# Layout de la página principal
home_layout = html.Div([
    dbc.Container([
        dbc.Card([
            dbc.CardBody([
                # Título Principal
                html.Div([
                    html.H1("Spotify Music Dashboard 🎶", className="text-center text-primary fw-bold mb-2"),
                    html.P("Welcome! View your top songs, artists, and recommendations.", className="text-center text-muted")
                ]),

                html.Hr(),

                # Botones Principales
                dbc.Row([
                    dbc.Col(dbc.Button("🎧 Get Recommendations", href="/recommendations", color="primary", size="lg", className="w-100"), width=4),
                    dbc.Col(dbc.Button("📊 Dashboard", href="/dashboard", color="success", size="lg", className="w-100"), width=4),
                    dbc.Col(dbc.Button("🎼 Generator", href="/generator", color="secondary", size="lg", className="w-100"), width=4),
                ], className="mb-4"),

                # Sección "About"
                html.Div([
                    html.H3("📢 About", className="text-center text-info fw-bold"),
                    dbc.Row([
                        dbc.Col([
                            html.P("Recsic is very simple to use! Go to the 'Recommend' page, enter the name of a song and Recsic will generate a list of 10 similar songs."),
                            html.P("We are still under development, so make sure to come back later!")
                        ], width=8),
                        dbc.Col(html.Img(src="/assets/spotify.png", style={"max-width": "80px", "display": "block", "margin": "auto"}), width=4)
                    ])
                ], className="mb-4"),

                html.Hr(),

                # Sección de Estadísticas
                html.Div([
                    html.H3("📊 Your Listening Stats", className="text-center text-primary fw-bold mb-4"),

                    # Top 5 Artistas
                    html.H4("🎤 Top 5 Artists", className="text-center text-dark fw-bold mb-3"),
                    html.Ul([
                        html.Li(html.A(artist["name"], href=artist["link"], target="_blank", style={"fontSize": "18px", "color": "#1DB954"})) for artist in top_artists
                    ], className="list-unstyled text-center mb-4"),

                    # Últimas Canciones Escuchadas
                    html.H3("🎵 Recently Played", className="text-center text-dark fw-bold mb-4"),
                    html.Ul([
                        html.Li(f"{track['name']} - {track['artist']}", style={"fontSize": "18px", "color": "#555"}) for track in recently_played
                    ], className="list-unstyled text-center mb-4"),

                    # Gráfico Listening Days
                    dcc.Graph(figure=listening_days_graph, className="mb-4"),
                ]),

                html.Hr(),

                # Sección de Atributos Musicales
                html.Div([
                    html.H3("🎼 Music Attributes", className="text-center text-info fw-bold mb-3"),

                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H6("🎸 Acousticness", className="text-primary fw-bold"),
                                html.P("Confidence from 0.0 to 1.0 of whether the track is acoustic.", className="text-muted")
                            ])
                        ], className="shadow-sm"), width=4),

                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H6("💃 Danceability", className="text-primary fw-bold"),
                                html.P("Describes how suitable a track is for dancing (0.0 to 1.0).", className="text-muted")
                            ])
                        ], className="shadow-sm"), width=4),

                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H6("⚡ Energy", className="text-primary fw-bold"),
                                html.P("Represents intensity and activity (0.0 to 1.0).", className="text-muted")
                            ])
                        ], className="shadow-sm"), width=4),
                    ], className="mb-3"),

                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H6("🎻 Instrumentalness", className="text-primary fw-bold"),
                                html.P("Higher values mean no vocals are present.", className="text-muted")
                            ])
                        ], className="shadow-sm"), width=4),

                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H6("🔊 Loudness", className="text-primary fw-bold"),
                                html.P("Overall loudness in decibels (dB).", className="text-muted")
                            ])
                        ], className="shadow-sm"), width=4),

                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H6("😊 Valence", className="text-primary fw-bold"),
                                html.P("Higher values indicate a happier tone.", className="text-muted")
                            ])
                        ], className="shadow-sm"), width=4),
                    ], className="mb-3")
                ]),

                html.Hr(),
            ])
        ], className="shadow-lg p-4 rounded-4 bg-light")
    ], className="mt-4")
])
>>>>>>> 116654978 (Gran actualizacion del proyecto Recsic)
