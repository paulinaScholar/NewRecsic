from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

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
            dbc.Col(html.Label("¿Cómo te sientes hoy? 😊"), width=12, className="text-center")
        ], className="mb-2"),

        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id="mood-dropdown",
                options=[{"label": mood, "value": mood} for mood in available_moods],
                placeholder="Selecciona tu estado de ánimo..."
            ), width=6, className="mx-auto")
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dbc.Button("🎵 Obtener recomendaciones", id="recommend-button", n_clicks=0, color="primary", className="btn-lg"), width=12, className="text-center")
        ], className="mb-4"),

        html.Hr(),

        dbc.Row([
            dbc.Col(html.H3("Canciones Recomendadas  🎧"), width=12, className="text-center")
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(html.Ul(id="recommendations-list"), width=12)
        ], className="mb-4"),

        html.Hr(),

        dbc.Row([         # Volver a Home
            dbc.Col(dbc.Button("🏠 Home", href="/", color="secondary", className="btn-lg"), width=12, className="text-center")
        ], className="mb-4")
    ], className="mt-4")
])

# Callback para actualizar recomendaciones
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
            return [html.Li("No recommendations available for this mood 😢")] 
        
        return [
            html.Li(
                html.A(f"{row['name']} - {row['artist']}", href=f"https://open.spotify.com/track/{row['id']}", target="_blank"),
                style={"fontSize": "18px"}
            ) for _, row in recommended_songs.iterrows()
        ]
    return []
