<<<<<<< HEAD
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from src.spotify.spotify_data import search_track

#Layout página de generador de lista de canciones 
generator_layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Escribe una canción"), width=12, className="text/center")
        ], className="mb-4"),

        dbc.Row([       #Input Song
            dbc.Col([dcc.Input(id="input-generate", type="text", 
                    placeholder="Type the title of a song", debounce=True, autoFocus=True,
                    style={'marginRight':'10px', 'width': '100%', 'margin-bottom': '10px'})
            ])
        ]),

        dbc.Row([
            dbc.Col(html.Div(id='generate-list'))   #Prueba para mostrar lista 
        ]),

        dbc.Row([
            dbc.Col(dbc.Button("Generate", id="generate-button", n_clicks=0, color="primary", className="btn-lg"),
                    width=12, className="text-center")
        ], className='mb-4'),

        html.Div(id="generate-list"),

        dbc.Row([         # Volver a Home
            dbc.Col(dbc.Button("🏠 Home", href="/", color="secondary", className="btn-lg"), width=12, className="text-center")
        ], className="mb-4")
    ], className="mt-4")
])

#Callback para obtener lista de canciones similares
@callback(
    Output("generate-list", "children"),
    Input("generate-button", "n_clicks"),
    Input("input-generate", "value")
)

    # Muestra titulo de la canción al presionar boton
def update_generator(n_clicks, valueSong):
    songInput = ""
    if n_clicks:
        songInput = valueSong
        return[
            search_track(songInput),
            dbc.Row([dbc.Col(html.H4("Found Tracks 🎤"), width=12, className="text-center")], className="mb-3"),
            dbc.Row([dbc.Col(songInput)]),
        ]
    return []
=======
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from .config import DATASET_PATH_2

df = pd.read_csv(DATASET_PATH_2)

metricas = ["danceability", "energy", "speechiness", "acousticness",
            "instrumentalness", "liveness", "valence", "tempo"]

df = df.dropna(subset=metricas)
df.drop_duplicates(inplace=True)

def recommend_by_metrics(usuario_input, exacto=False, top_n=10):
    df_copy = df.copy()

    if exacto:
        query = " & ".join([f"{col} == {val}" for col, val in usuario_input.items()])
        resultados = df_copy.query(query)
    else:
        X = df_copy[metricas].fillna(0)
        user_vector = [usuario_input.get(m, 0) for m in metricas]

        distancias = euclidean_distances([user_vector], X)[0]
        df_copy["distancia"] = distancias
        resultados = df_copy.sort_values("distancia").head(top_n)

    return resultados[["trackName", "artistName"] + metricas]

generator_layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H1("🎶 Recomendador por Métricas", className="text-center mb-4"),

                html.P("Busca una canción y revisa sus métricas:", className="text-center"),

                dbc.Row([
                    dbc.Col([
                        dbc.InputGroup([
                            dbc.InputGroupText("🎵 Canción"),
                            dbc.Input(id="song-input", type="text", placeholder="Ejemplo: Gangnam Style")
                        ])
                    ], md=6),

                    dbc.Col([
                        dbc.InputGroup([
                            dbc.InputGroupText("👤 Artista (opcional)"),
                            dbc.Input(id="artist-input", type="text", placeholder="Ejemplo: PSY")
                        ])
                    ], md=6),
                ], className="mb-3"),

                dbc.Row([
                    dbc.Col(dbc.Button("📊 Buscar Métricas", id="search-song", n_clicks=0,
                                       color="info", className="btn-lg w-100")),
                ], className="mb-4 text-center"),

                html.Div(id="song-metrics"),

                html.Hr(),

                html.P("Ajusta los valores de las métricas para encontrar canciones similares:",
                       className="text-center"),

                dbc.Row([
                    dbc.Col([
                        html.Label("Danceability"),
                        dcc.Slider(id="slider-danceability", min=0, max=1, step=0.01, value=0.5,
                                   marks={0:"0", 0.5:"0.5", 1:"1"})
                    ]),
                    dbc.Col([
                        html.Label("Energy"),
                        dcc.Slider(id="slider-energy", min=0, max=1, step=0.01, value=0.5,
                                   marks={0:"0", 0.5:"0.5", 1:"1"})
                    ]),
                ], className="mb-3"),

                dbc.Row([
                    dbc.Col([
                        html.Label("Valence"),
                        dcc.Slider(id="slider-valence", min=0, max=1, step=0.01, value=0.5,
                                   marks={0:"0", 0.5:"0.5", 1:"1"})
                    ]),
                    dbc.Col([
                        html.Label("Tempo"),
                        dcc.Slider(id="slider-tempo", min=40, max=200, step=1, value=120,
                                   marks={40:"40", 120:"120", 200:"200"})
                    ]),
                ], className="mb-3"),

                dbc.Checklist(
                    options=[{"label": "Coincidencia Exacta", "value": "exacto"}],
                    value=[],
                    id="exact-match",
                    switch=True,
                    className="mb-3"
                ),

                dbc.Row([
                    dbc.Col(dbc.Button("🎧 Buscar Canciones", id="generate-button", n_clicks=0,
                                       color="primary", className="btn-lg w-100")),
                ], className="mb-4 text-center"),

                html.Div(id="generate-list"),

                html.Hr(),

                dbc.Row([
                    dbc.Col(dbc.Button("🏠 Volver al Inicio", href="/",
                                       color="secondary", className="btn-lg w-100")),
                ], className="text-center")
            ])
        ], className="shadow-lg p-4 rounded-3"))
    ], className="mt-5 justify-content-center")
], className="d-flex justify-content-center")

@callback(
    Output("song-metrics", "children"),
    Input("search-song", "n_clicks"),
    State("song-input", "value"),
    State("artist-input", "value")
)
def show_song_metrics(n_clicks, song_name, artist_name):
    if not n_clicks or not song_name:
        return ""

    resultados = df[df["trackName"].str.contains(song_name, case=False, na=False)]

    if artist_name:
        resultados = resultados[resultados["artistName"].str.contains(artist_name, case=False, na=False)]

    if resultados.empty:
        return dbc.Alert("⚠️ No se encontró esa canción en el dataset.", color="warning")

    return dbc.Table(
        [
            html.Thead(html.Tr([html.Th("Canción"), html.Th("Artista")] + [html.Th(m) for m in metricas])),
            html.Tbody([
                html.Tr([
                    html.Td(row["trackName"]),
                    html.Td(row["artistName"]),
                ] + [html.Td(round(row[m], 3)) for m in metricas])
                for _, row in resultados.iterrows()
            ])
        ],
        bordered=True,
        hover=True,
        responsive=True,
        className="mt-3"
    )

@callback(
    Output("generate-list", "children"),
    Input("generate-button", "n_clicks"),
    Input("slider-danceability", "value"),
    Input("slider-energy", "value"),
    Input("slider-valence", "value"),
    Input("slider-tempo", "value"),
    Input("exact-match", "value")
)
def update_generator(n_clicks, danceability, energy, valence, tempo, exact_match):
    if not n_clicks:
        return []

    usuario_input = {
        "danceability": danceability,
        "energy": energy,
        "valence": valence,
        "tempo": tempo
    }

    exacto = "exacto" in exact_match
    recomendaciones = recommend_by_metrics(usuario_input, exacto=exacto)

    if recomendaciones.empty:
        return dbc.Alert("⚠️ No se encontraron canciones con esos parámetros.",
                         color="warning", className="text-center")

    return dbc.Table(
        [
            html.Thead(html.Tr([html.Th("Canción"), html.Th("Artista"),
                                html.Th("Danceability"), html.Th("Energy"),
                                html.Th("Valence"), html.Th("Tempo")])),
            html.Tbody([
                html.Tr([
                    html.Td(row["trackName"]),
                    html.Td(row["artistName"]),
                    html.Td(round(row["danceability"], 2)),
                    html.Td(round(row["energy"], 2)),
                    html.Td(round(row["valence"], 2)),
                    html.Td(round(row["tempo"], 1))
                ]) for _, row in recomendaciones.iterrows()
            ])
        ],
        bordered=True,
        hover=True,
        responsive=True,
        className="mt-4"
    )
>>>>>>> 116654978 (Gran actualizacion del proyecto Recsic)
