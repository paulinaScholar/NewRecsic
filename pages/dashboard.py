from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from src.spotify.spotify_data import get_top_genres, get_music_trivia, get_top_podcasts, get_listening_days
<<<<<<< HEAD
from dash_bootstrap_templates import load_figure_template

load_figure_template(["PULSE"])

# Obtener datos desde Spotify API
=======

>>>>>>> 116654978 (Gran actualizacion del proyecto Recsic)
top_genres = get_top_genres()
trivia_facts = get_music_trivia()
top_podcasts = get_top_podcasts()
listening_days = get_listening_days()

<<<<<<< HEAD
# Procesar datos para gráficos
days, counts = (list(listening_days.keys()), list(listening_days.values())) if listening_days else ([], [])

# Gráfico de días más escuchados
listening_days_graph = {
    "data": [go.Bar(x=days, y=counts, marker=dict(color="blue"))],
    "layout": go.Layout(title="Listening Habits 📆", xaxis_title="Day", yaxis_title="Songs Played", height=400, template="PULSE")
}
# 🎵 Sección de Géneros principales
=======
days, counts = (list(listening_days.keys()), list(listening_days.values())) if listening_days else ([], [])

listening_days_graph = {
    "data": [go.Bar(x=days, y=counts, marker=dict(color="#1DB954"))],
    "layout": go.Layout(title="Listening Habits 📆", xaxis_title="Day", yaxis_title="Songs Played", height=400)
}

>>>>>>> 116654978 (Gran actualizacion del proyecto Recsic)
genres_graph = px.pie(
    names=[genre["name"] for genre in top_genres],
    values=[genre["count"] for genre in top_genres],
    title="Top Music Genres 🎼",
<<<<<<< HEAD
    hole=0.3,
    template="PULSE",
)

# 📌 Layout de la página Dashboard
dashboard_layout = html.Div([
    dbc.Container([
        # 🎧 Título principal
        dbc.Row([
            dbc.Col(html.H1("🎛️ Spotify Dashboard"), width=12, className="text-center")
        ], className="mb-4"),

        # 🏆 Géneros Principales
        dbc.Row([
            dbc.Col(html.H3("Top Music Genres 🎼"), width=12, className="text-center")
        ], className="mb-3"),

        dbc.Row([
            dbc.Col(dcc.Graph(figure=genres_graph), width=12)
        ], className="mb-4"),

        html.Hr(),
        
        # Listening Days Graph
        dbc.Row([dbc.Col(dcc.Graph(figure=listening_days_graph), width=12)], className="mb-4"),

        html.Hr(),

        # 🎲 Trivia Musical
        dbc.Row([
            dbc.Col(html.H3("🎵 Fun Music Trivia!"), width=12, className="text-center")
        ], className="mb-3"),

        dbc.Row([
            dbc.Col(html.Div(id="trivia-container", className="text-center"), width=12)
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Button("🎲 Get Random Trivia", id="trivia-button", color="primary"), width={"size": 6, "offset": 3})
        ], className="mb-4 text-center"),

        html.Hr(),

        # 🎙️ Podcasts Destacados
        dbc.Row([
            dbc.Col(html.H3("Top Podcasts 🎙️"), width=12, className="text-center")
        ], className="mb-3"),

        dbc.Row([
            dbc.Col(html.Ul([
                html.Li(html.A(podcast["name"], href=podcast["link"], target="_blank", style={"fontSize": "18px"})) for podcast in top_podcasts
            ]), width=12)
        ], className="mb-4"),

        html.Hr(),

        # 🔙 Botón para volver a Home
        dbc.Row([
            dbc.Col(dbc.Button("🏠 Home", href="/", color="secondary"), width={"size": 6, "offset": 3})
        ], className="mb-4 text-center"),

        html.Hr()
    ], className="mt-4")
])

# 🎲 Callback para Trivia aleatoria
=======
    hole=0.4,
    color_discrete_sequence=px.colors.sequential.Blues
)

dashboard_layout = html.Div([
    dbc.Container([
        dbc.Row([dbc.Col(html.H1("🎛️ Spotify Dashboard", className="text-center text-white bg-dark p-4 mb-4 rounded"), width=12)]),

        dbc.Row([dbc.Col(dbc.Card([
            dbc.CardHeader("Dashboard Overview", className="bg-primary text-white"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(dcc.Graph(figure=genres_graph), width=6),
                    dbc.Col(dcc.Graph(figure=listening_days_graph), width=6)
                ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col(html.H3("🎵 Fun Music Trivia!", className="text-center"), width=12),
                    dbc.Col(html.Div(id="trivia-container", className="text-center text-muted mb-3"), width=12),
                    dbc.Col(dbc.Button("🎲 Get Random Trivia", id="trivia-button", color="primary", className="mt-2"), width=12, className="text-center")
                ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col(html.H3("Top Podcasts 🎙️", className="text-center"), width=12),
                    dbc.Col(html.Ul([
                        html.Li(html.A(podcast["name"], href=podcast["link"], target="_blank", className="text-decoration-none text-primary")) for podcast in top_podcasts
                    ]), width=12)
                ])
            ])
        ], className="shadow mb-4"))]),

        dbc.Row([dbc.Col(dbc.Button("🏠 Home", href="/", color="secondary", className="mt-3"), width=12, className="text-center")])
    ], className="p-4")
])

>>>>>>> 116654978 (Gran actualizacion del proyecto Recsic)
@callback(
    Output("trivia-container", "children"),
    Input("trivia-button", "n_clicks")
)
def show_random_trivia(n_clicks):
    if n_clicks:
        return html.P(f"🎶 {trivia_facts[n_clicks % len(trivia_facts)]}", style={"fontSize": "18px", "fontStyle": "italic"})
    return html.P("Click the button for a fun fact! 🎵", style={"fontSize": "18px", "fontStyle": "italic"})
