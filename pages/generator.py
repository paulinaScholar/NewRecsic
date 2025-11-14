from dash import html, dcc, callback, Input, Output, State, ALL, no_update
import dash, re, base64, json, uuid
import dash_bootstrap_components as dbc
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from .config import DATASET_PATH_3
from flask import session

df = pd.read_csv(DATASET_PATH_3)
print(df.columns)

metricas = [
    "danceability", "energy", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence", "tempo"
]

df = df.dropna(subset=metricas)

cols_for_duplicates = [
    "trackName", "artistName", "danceability","energy","key","loudness",
    "mode","speechiness","acousticness","instrumentalness","liveness",
    "valence","tempo"
]

# Drop rows where these columns are duplicated
df = df.drop_duplicates(subset=cols_for_duplicates, keep="first")


def recommend_by_metrics(usuario_input, exacto=False, top_n=11):
    df_copy = df.copy()

    song_name = usuario_input.get("trackName")
    artist_name = usuario_input.get("artistName")

    # Si hay canción seleccionada, usarla como referencia
    if song_name:
        if artist_name:
            base_song = df_copy[
                (df_copy["trackName"].str.lower() == song_name.lower()) &
                (df_copy["artistName"].str.lower() == artist_name.lower())
            ]
        else:
            base_song = df_copy[df_copy["trackName"].str.lower() == song_name.lower()]

        if not base_song.empty:
            user_vector = base_song.iloc[0][metricas].values
        else:
            user_vector = [usuario_input.get(m, 0) for m in metricas]
    else:
        user_vector = [usuario_input.get(m, 0) for m in metricas]

    # Cálculo exacto o por distancia
    if exacto:
        query = " & ".join([f"{col} == {val}" for col, val in usuario_input.items() if col in metricas])
        resultados = df_copy.query(query)
    else:
        X = df_copy[metricas].fillna(0)
        distancias = euclidean_distances([user_vector], X)[0]
        df_copy["distancia"] = distancias
        resultados = df_copy.sort_values("distancia").head(top_n)

    return resultados[["trackName", "artistName"] + metricas]



generator_layout = dbc.Container([
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                dcc.Store(id="recommendation-stored"), # recomendations saved in temp memory

                html.H1("🎶 Recomendador por Métricas", className="text-center mb-4"),

                html.P("Busca una canción y revisa sus métricas:", className="text-center"),

                # Cancion
                dbc.Row([
                    dbc.Col([
                        html.Div(
                            style = { "position": "relative", "marginBottom": "20px"},
                            children = [
                                dbc.InputGroup([
                                    dbc.InputGroupText("🎵 Canción"),
                                    dbc.Input(
                                        id="song-input", 
                                        type="text",
                                        inputMode="text",
                                        pattern=".*", 
                                        placeholder="Ejemplo: Gangnam Style",
                                        style={
                                            "width": "100%",
                                            "padding": "8px",
                                            "borderRadius": "8px",
                                            "border": "1px solid #ccc"
                                        }
                                    ),
                                    html.Ul(
                                        id="track-suggestions",
                                        style={
                                            "listStyleType": "none",
                                            "padding": "0",
                                            "marginTop": "0",
                                            "border": "1px solid #ccc",
                                            "borderRadius": "8px",
                                            "maxHeight": "150px",
                                            "overflowY": "auto",
                                            "display": "none",
                                            "backgroundColor": "white",
                                            "position": "absolute",
                                            "width": "100%",
                                            "zIndex": "9999",
                                            "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
                                        },
                                    )
                                ])
                            ]
                        )
                    ], md=6),

                    # Artista
                    dbc.Col([
                        dbc.InputGroup([
                            dbc.InputGroupText("👤 Artista (opcional)"),
                            dbc.Input(
                                id="artist-input", 
                                type="text", 
                                placeholder="Ejemplo: PSY",
                                debounce=True,
                                style={
                                    "width": "100%",
                                    "padding": "8px",
                                    "borderRadius": "8px",
                                    "border": "1px solid #ccc",
                                    "marginBottom": "15px"
                                },
                            )
                        ])
                    ], md=6),
                ], className="mb-6"),

                dbc.Row([
                    dbc.Col(dbc.Button("📊 Buscar Métricas", id="search-song", n_clicks=0,
                                       color="info", className="btn-sm w-100")),
                ], className="mb-4 text-center"),
                
                html.Div(id="song-metrics"),  # Aquí se mostrarán las métricas de la canción

                html.Hr(),

                html.P("Ajusta los valores de las métricas para encontrar canciones similares:",
                       className="text-center"),

                # Sliders para métricas
                dbc.Row([
                    dbc.Col([
                        # html.Div([
                        #     html.Span("Hover over me", id="tooltip-target", style={"cursor": "pointer"}),
                        #     dbc.Tooltip("Tooltip text", target="tooltip-target", placement="top"),
                        # ]),

                        html.Label("Bailabilidad"), html.Span(id="DanceInfo-target", className="fa-regular fa-circle-question mx-2", style={"fontSize": "14px", "color": "#808080", "cursor": "pointer"}),
                        dbc.Tooltip("Describe qué tan adecuada es una pista para bailar. Un valor de 0.0 es el menos bailable y 1.0 el más bailable.", target="DanceInfo-target", placement="top"),
                        
                        dcc.Slider(id="slider-danceability", min=0, max=1, step=0.01, value=0.5,
                                   marks={0:"0", 0.5:"0.5", 1:"1"})
                    ]),
                    dbc.Col([
                        html.Label("Energía"), html.Span(id="EnergyInfo-target", className="fa-regular fa-circle-question mx-2", style={"fontSize": "14px", "color": "#808080", "cursor": "pointer"}),
                        dbc.Tooltip("Una medida de 0.0 a 1.0 que representa la intensidad y la actividad. Las pistas enérgicas se sienten rápidas, escandalosas y con mucho ruido.", target="EnergyInfo-target", placement="top"),
                        
                        dcc.Slider(id="slider-energy", min=0, max=1, step=0.01, value=0.5,
                                   marks={0:"0", 0.5:"0.5", 1:"1"})
                    ]),
                ], className="mb-3"),

                dbc.Row([
                    dbc.Col([
                        html.Label("Valencia"), html.Span(id="ValenceInfo-target", className="fa-regular fa-circle-question mx-2", style={"fontSize": "14px", "color": "#808080", "cursor": "pointer"}),
                        dbc.Tooltip("Una medida de 0.0 a 1.0 que describe la 'positividad' musical. Los valores más altos indican un tono más alegre.", target="ValenceInfo-target", placement="top"),
                        
                        dcc.Slider(id="slider-valence", min=0, max=1, step=0.01, value=0.5,
                                   marks={0:"0", 0.5:"0.5", 1:"1"})
                    ]),
                    dbc.Col([
                        html.Label("Tempo"), html.Span(id="TempoInfo-target", className="fa-regular fa-circle-question mx-2", style={"fontSize": "14px", "color": "#808080", "cursor": "pointer"}),
                        dbc.Tooltip("Una medida de 40 a 200 expresada en pulsaciones por minuto (BPM) que indica la velocidad de una pieza musical.", target="TempoInfo-target", placement="top"),
                        
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
                ], className="mb-2 text-center"),
                
                dbc.Row([
                    dbc.Col(dbc.Button("Limpiar Resultados", id="clear-all", n_clicks=0,
                                       className="bg-secondary text-white border-0 btn-sm w-100 ")),
                ], className="mb-4 text-center"),


                html.Div(id="generate-list"),

                html.Div(id="save-list", className="text-end mt-3"),
                html.Div(
                    [
                        dbc.Toast(
                            id="save-toast",
                            header="Aviso",
                            is_open=False,
                            dismissable=True,
                            duration=4000,
                            icon="success",  # Se cambia dinámicamente
                            style={
                                "position": "fixed",
                                "top": 20,
                                "right": 20,
                                "width": 300,
                                "zIndex": 2000,
                            },
                        ),
                    ]
                ),

                html.Hr(),

                dbc.Row([
                    dbc.Col(
                        html.Div(
                            html.Img(
                                src="/static/Recsic-12.png",
                                className="img-fluid",
                                style={ "height": "70px" }
                            ),
                        ), className="text-center"
                    ),
                ]),
                

                html.Hr(),

                dbc.Row([
                    dbc.Col(dbc.Button("🏠 Volver al Inicio", href="/",
                                       color="secondary", className="btn-lg w-100")),
                ], className="text-center")
            ])
        ], className="shadow-lg p-4 rounded-3"))
    ], className="mt-5 col-lg-8 justify-content-center")
], className="d-flex justify-content-center col-lg-8")

# ---------------------------------------------
# Callback para mostrar métricas de la canción
# ---------------------------------------------
@callback(
    Output("song-metrics", "children"),
    Input("search-song", "n_clicks"),
    State("song-input", "value"),
    State("artist-input", "value")
)
def show_song_metrics(n_clicks, song_name, artist_name):
    if not n_clicks or not song_name:
        return ""

    song_name = re.escape(song_name)
    artist_name = re.escape(artist_name) if artist_name else None

    # Filtrar por canción
    resultados = df[df["trackName"].str.contains(song_name, case=False, na=False, regex=True)]

    # Si también puso artista, filtrar aún más
    if artist_name:
        resultados = resultados[resultados["artistName"].str.contains(artist_name, case=False, na=False, regex=True)]

    if resultados.empty:
        return dbc.Alert("⚠️ No se encontró esa canción en el dataset.", color="warning")

    resultados = resultados.head(5)

    # Mostrar coincidencias
    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [html.Th("Canción"), html.Th("Artista")] +
                    [html.Th(m) for m in metricas]
                )
            ),
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

# -----------------------------
# Callback para recomendaciones
# -----------------------------
@callback(
    Output("generate-list", "children"),
    Output("recommendation-stored", "data"),
    Input("generate-button", "n_clicks"),
    State("song-input", "value"),
    State("artist-input", "value"),
    State("slider-danceability", "value"),
    State("slider-energy", "value"),
    State("slider-valence", "value"),
    State("slider-tempo", "value"),
    State("exact-match", "value"),
    prevent_initial_call = True
)
def update_generator(n_clicks, song_name, artist_name, danceability, energy, valence, tempo, exact_match):
    if not n_clicks:
        return dash.exceptions.PreventUpdate

    usuario_input = {
        "trackName": song_name,
        "artistName": artist_name,
        "danceability": danceability,
        "energy": energy,
        "valence": valence,
        "tempo": tempo
    }

    exacto = "exacto" in exact_match
    recomendaciones = recommend_by_metrics(usuario_input, exacto=exacto)

    if recomendaciones.empty:
        alert = dbc.Alert("⚠️ No se encontraron canciones con esos parámetros.",
                         color="warning", className="text-center")
        return alert, []

    table = dbc.Table(
        [
            html.Thead(html.Tr([
                html.Th("Canción"), html.Th("Artista"),
                html.Th("Danceability"), html.Th("Energy"),
                html.Th("Valence"), html.Th("Tempo")
            ],className="table-active")),
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

    store_data = recomendaciones[["trackName", "artistName"]].to_dict("records")

    return table, store_data

# ------------------------------------
# Callback para sliders
# ------------------------------------
@callback(
    Output("slider-danceability", "value"),
    Output("slider-energy", "value"),
    Output("slider-valence", "value"),
    Output("slider-tempo", "value"),
    Input("song-input", "value"),
    Input("artist-input", "value"),
    prevent_initial_call=True
)
def update_sliders(song_name, artist_name):
    if not song_name:
        # Si no hay canción seleccionada, no cambiar los sliders
        raise dash.exceptions.PreventUpdate

    # Buscar la canción en el dataset
    if artist_name:
        song = df[
            (df["trackName"].str.lower() == song_name.lower()) &
            (df["artistName"].str.lower() == artist_name.lower())
        ]
    else:
        song = df[df["trackName"].str.lower() == song_name.lower()]

    if song.empty:
        raise dash.exceptions.PreventUpdate

    # Obtener las métricas de la canción seleccionada
    song_data = song.iloc[0]
    return (
        float(song_data["danceability"]),
        float(song_data["energy"]),
        float(song_data["valence"]),
        float(song_data["tempo"])
    )


# ------------------------------------
# Callback para autocomplete canciones
# ------------------------------------
@callback(
    Output("song-input", "value"),
    Output("artist-input", "value"),
    Output("track-suggestions", "children"),
    Output("track-suggestions", "style"),
    Input("song-input", "value"),
    Input({"type": "track-suggestion", "index": ALL}, "n_clicks"),
    State({"type": "track-suggestion", "index": ALL}, "id"),
    prevent_initial_call=True,
)
def update_track_autocomplete(value, n_clicks, ids):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    #  Si se hace clic en una sugerencia
    if "track-suggestion" in triggered_id:
        if not any(n_clicks):
            raise dash.exceptions.PreventUpdate
        clicked_index = n_clicks.index(max(n_clicks))
        selected = ids[clicked_index]["index"]

        # Decodificar a base64 JSON para permitir caracteres especiales
        try:
            decoded = base64.urlsafe_b64decode(selected.encode()).decode()
            data = json.loads(decoded)
            track, artist = data.get("track", ""), data.get("artist", "")
        except Exception:
            track, artist = "", ""

        return track, artist, [], {"display": "none"}

    # Mientras el usuario escribe...
    if not value:
        return "", "", [], {"display": "none"}

    # Escapar caracteres especiales del texto ingresado
    song_value = re.escape(value.strip())

    # Buscar coincidencias seguras por nombre de canción
    matches = df[df["trackName"].astype(str).str.contains(song_value, case=False, na=False, regex=True)]

    if matches.empty:
        return value, "", [html.Li("Sin resultados", style={"padding": "8px", "color": "#777"})], {"display": "block"}

    # Crear lista de sugerencias (con IDs codificados)
    suggestions = []
    for _, row in matches[["trackName", "artistName"]].dropna().head(6).iterrows():
        track = row["trackName"]
        artist = row["artistName"]

        # Codificar la información como JSON base64
        encoded_id = base64.urlsafe_b64encode(json.dumps({"track": track, "artist": artist}).encode()).decode()

        suggestions.append(
            html.Li(
                f"{track} — {artist}",
                n_clicks=0,
                id={"type": "track-suggestion", "index": encoded_id},
                style={
                    "padding": "8px",
                    "cursor": "pointer",
                    "borderBottom": "1px solid #eee",
                    "whiteSpace": "nowrap",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                },
                title=f"{track} — {artist}"  # Tooltip al pasar el mouse
            )
        )

    return value, "", suggestions, {"display": "block"}

# ---------------------------------
# Callback para limpiar resultados
# ---------------------------------
@callback(
    Output("song-input", "value", allow_duplicate=True),
    Output("artist-input", "value", allow_duplicate=True),
    Output("slider-danceability", "value", allow_duplicate=True),
    Output("slider-energy", "value", allow_duplicate=True),
    Output("slider-valence", "value", allow_duplicate=True),
    Output("slider-tempo", "value", allow_duplicate=True),
    Output("song-metrics", "children", allow_duplicate=True),
    Output("generate-list", "children", allow_duplicate=True),
    Input("clear-all", "n_clicks"),
    prevent_initial_call=True,
)
def clear_all(n_clicks):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate

    # Reinicia todos los valores
    return "", "", 0.5, 0.5, 0.5, 120, [], []

# --------------------------------------
# Callback para comprobar session activa
# --------------------------------------
@callback(
    Output("save-list", "children"),
    Input("generate-button", "n_clicks"),
    prevent_initial_call=True
)
def show_save_button(n_clicks):
    if "user_id" not in session:
        return ""

    return dbc.Button(
                "💾 Guardar lista",
                id="btn-saveList",
                color="success",
                className="btn-sm mb-2",
                n_clicks=0
            )

# ---------------------------
# Callback para guardar lista
# ---------------------------
@callback(
    Output("save-toast", "is_open"),
    Output("save-toast", "header"),
    Output("save-toast", "icon"),
    Input("btn-saveList", "n_clicks"),
    State("recommendation-stored", "data"),
    prevent_initial_call=True
)
def save_recommendations(n_clicks, data):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate

    # Verificar sesión activa
    if "user_id" not in session:
        return True, "Debes iniciar sesión para guardar tu lista", "warning"

    # Verificar que haya datos
    if not data:
        return True, "No hay lista generada para guardar.", "secondary"

    user_id = session["user_id"]
    list_id = str(uuid.uuid4())

    try:
        from db import db_cursor
        with db_cursor() as cur:
            for row in data:
                cur.execute("""
                    INSERT INTO user_recommendations (user_id, track_name, artist_name, list_id)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, row["trackName"], row["artistName"], list_id))

        return True, "Tu lista se guardó correctamente", "success"

    except Exception as e:
        print("Error al guardar:", e)
        return True, "Ocurrió un error al guardar la lista", "danger"
