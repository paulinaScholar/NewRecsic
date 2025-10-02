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
        dbc.Row([dbc.Col(html.P("Bienvenido! Encuentra tu top de canciones, artistas y recomendaciones musicales."), width=12)], className="mb-3"),

        # Añadir un nuevo botón "Dashboard" junto a "Get Recommendations"
        dbc.Row([
            dbc.Col(dbc.Button("🎧 Obtener Recomendaciones", href="/recommendations", color="primary", size="lg"), width={"size": 6, "offset": 3}),
            dbc.Col(dbc.Button("📊 Dashboard", href="/dashboard", color="secondary", size="lg"), width={"size": 6, "offset": 0}),
            dbc.Col(dbc.Button("Generador", href="/generator", color="secondary", size="lg"), width={"size": 6, "offset": 0})
        ], className="mb-4 text-center"),

        html.Hr(),

        # About Section
        dbc.Row([dbc.Col(html.H3("Sobre"), width=12)]),
        dbc.Row([
            dbc.Col([html.P("Recsic es muy fácil de usar! Has clic en 'Recomendaciones', escribe el nombre de una canción y Recsic generará una lista de 10 canciones similares."),
                     html.P("Seguimos en desarrollo así que, ¡recuerda visitarnos en el futuro!")], width=6),
            dbc.Col(html.Img(src="/assets/spotify.png", style={"max-width": "50px"}), width=6)
        ], className="mb-4"),

        html.Hr(),

        # Stats Section
        dbc.Row([dbc.Col(html.H3("Estadísticas 📊"), width=12, className="text-center")], className="mb-4"),

        # Top Artists
        dbc.Row([dbc.Col(html.H4("Top 5 Artistas 🎤"), width=12, className="text-center")], className="mb-3"),
        dbc.Row([dbc.Col(html.Ul([html.Li(html.A(artist["name"], href=artist["link"], target="_blank", style={"fontSize": "18px"})) for artist in top_artists]), width=12)], className="mb-4"),

        # Recently Played Songs
        dbc.Row([dbc.Col(html.H3("Escuchado Recientemente 🎵"), width=12, className="text-center")], className="mb-4"),
        dbc.Row([dbc.Col(html.Ul([html.Li(f"{track['name']} - {track['artist']} ", style={"fontSize": "18px"}) for track in recently_played]), width=12)], className="mb-4"),

        html.Hr(),

        # Skills Section
        dbc.Row([dbc.Col(html.H3("Atributos Musicales 🎼"), width=12)]),
        dbc.Row([
            dbc.Col(html.Div([html.H6("Acousticness", style={"color": "#6f42c1"}), html.P("Una medida de confianza de 0,0 a 1,0 sobre si la pista es acústica. 1,0 representa una confianza alta.")]), width=4),
            dbc.Col(html.Div([html.H6("Danceability", style={"color": "#6f42c1"}), html.P("Describe qué tan adecuada es una pista para bailar. Un valor de 0.0 es el menos bailable y 1.0 el más bailable.")]), width=4),
            dbc.Col(html.Div([html.H6("Energy", style={"color": "#6f42c1"}), html.P("Una medida de 0.0 a 1.0 que representa la intensidad y la actividad. Las pistas enérgicas se sienten rápidas, escandalosas y con mucho ruido.")]), width=4),
        ], className="mb-3"),

        dbc.Row([
            dbc.Col(html.Div([html.H6("Instrumentalness", style={"color": "#6f42c1"}), html.P("Predice si una pista no contiene voces. Un valor cercano a 1.0 indica una mayor probabilidad de ausencia vocal.")]), width=4),
            dbc.Col(html.Div([html.H6("Loudness", style={"color": "#6f42c1"}), html.P("La sonoridad general de una pista en decibelios (dB). Los valores suelen oscilar entre -60 y 0 dB.")]), width=4),
            dbc.Col(html.Div([html.H6("Valence", style={"color": "#6f42c1"}), html.P("Una medida de 0.0 a 1.0 que describe la 'positividad' musical. Los valores más altos indican un tono más alegre.")]), width=4),
        ], className="mb-3"),

        html.Hr(),
    ], className="mt-4")
])
