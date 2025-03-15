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
                    placeholder="Type the title of a song", debounce=True, required=True, autoFocus=True,
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