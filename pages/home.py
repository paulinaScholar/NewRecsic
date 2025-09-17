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
