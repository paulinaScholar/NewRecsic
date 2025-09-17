from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
<<<<<<< HEAD

# Cargar dataset de canciones
songs_df = pd.read_csv("data_moods.csv")

# Obtener lista única de estados de ánimo disponibles
available_moods = songs_df["mood"].unique()

# Layout de la página de recomendaciones
recommendations_layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Recsic Mood 🎶"), width=12, className="text-center")
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(html.Label("How are you feeling today? 😊"), width=12, className="text-center")
        ], className="mb-2"),

        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id="mood-dropdown",
                options=[{"label": mood, "value": mood} for mood in available_moods],
                placeholder="Selecciona tu estado de ánimo..."
            ), width=6, className="mx-auto")
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Button("🎵 Get recommendation", id="recommend-button", n_clicks=0, color="primary", className="btn-lg"), width=12, className="text-center")
        ], className="mb-4"),

        html.Hr(),

        dbc.Row([
            dbc.Col(html.H3("Recommended Songs 🎧"), width=12, className="text-center")
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(html.Ul(id="recommendations-list"), width=12)
        ], className="mb-4"),

        html.Hr(),

        dbc.Row([         # Volver a Home
            dbc.Col(dbc.Button("🏠 Home", href="/", color="secondary", className="btn-lg"), width=12, className="text-center")
=======
from .config import DATASET_PATH_1

songs_df = pd.read_csv(DATASET_PATH_1)
available_moods = songs_df["mood"].unique()

recommendations_layout = html.Div([
    dbc.Container([
        # Título de la Página
        dbc.Row([
            dbc.Col(html.H1("🎶 Recsic Mood", className="text-center fw-bold text-primary"), width=12)
        ], className="mb-3"),

        # Pregunta de estado de ánimo
        dbc.Row([
            dbc.Col(html.H4("¿How are you feeling today? 😊", className="text-center text-secondary"), width=12)
        ], className="mb-2"),

        # Elegir estado de ánimo
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id="mood-dropdown",
                options=[{"label": mood.title(), "value": mood} for mood in available_moods],
                placeholder="Select your mood...",
                className="shadow-sm"
            ), width=6, className="mx-auto")
        ], className="mb-4"),

        # Botón de recomendación
        dbc.Row([
            dbc.Col(dbc.Button("🎵 Get Recommendation", id="recommend-button", n_clicks=0, 
                               color="primary", className="btn-lg shadow"), 
                    width=12, className="text-center")
        ], className="mb-4"),

        # Separador
        html.Hr(className="my-4"),

        # Título de la sección de recomendaciones
        dbc.Row([
            dbc.Col(html.H3("🎧 Recommended Songs", className="text-center fw-bold text-info"), width=12)
        ], className="mb-3"),

        # Lista de recomendaciones
        dbc.Row([
            dbc.Col(dbc.ListGroup(id="recommendations-list"), width=8, className="mx-auto")
        ], className="mb-4"),

        # Separador
        html.Hr(className="my-4"),

        # Botón para volver a Home
        dbc.Row([
            dbc.Col(dbc.Button("🏠 Home", href="/", color="secondary", className="btn-lg shadow"), width=12, className="text-center")
>>>>>>> 116654978 (Gran actualizacion del proyecto Recsic)
        ], className="mb-4")
    ], className="mt-4")
])

<<<<<<< HEAD
# Callback para actualizar recomendaciones
=======
>>>>>>> 116654978 (Gran actualizacion del proyecto Recsic)
@callback(
    Output("recommendations-list", "children"),
    Input("recommend-button", "n_clicks"),
    Input("mood-dropdown", "value")
)
def update_recommendations(n_clicks, selected_mood):
    if n_clicks > 0 and selected_mood:
        filtered_songs = songs_df[songs_df["mood"] == selected_mood]
        recommended_songs = filtered_songs.sample(n=min(5, len(filtered_songs))) if not filtered_songs.empty else pd.DataFrame()

        if recommended_songs.empty:
<<<<<<< HEAD
            return [html.Li("No recommendations available for this mood 😢")] 
        
        return [
            html.Li(
                html.A(f"{row['name']} - {row['artist']}", href=f"https://open.spotify.com/track/{row['id']}", target="_blank"),
                style={"fontSize": "18px"}
=======
            return [dbc.ListGroupItem("😢 No recommendations available for this mood.", className="text-center text-danger")]

        return [
            dbc.ListGroupItem(
                html.A(f"{row['name']} - {row['artist']}", href=f"https://open.spotify.com/track/{row['id']}", 
                       target="_blank", className="text-decoration-none text-dark fw-bold"),
                className="list-group-item-action"
>>>>>>> 116654978 (Gran actualizacion del proyecto Recsic)
            ) for _, row in recommended_songs.iterrows()
        ]
    return []
