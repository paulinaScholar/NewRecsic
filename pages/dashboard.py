from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .config import DATASET_PATH_1, DATASET_PATH_2
from flask import session

df_main = pd.read_csv(DATASET_PATH_2)
df_csv1 = pd.read_csv(DATASET_PATH_1)


def clean_dataframe(df, required_columns):
    df_clean = df.copy()
    if required_columns:
        existing = [c for c in required_columns if c in df_clean.columns]
        if existing:
            df_clean = df_clean.dropna(subset=existing)
    return df_clean


def make_top_artists_figure(df):
    artist_col = "artistName" if "artistName" in df.columns else "artist"
    df_clean = clean_dataframe(df, [artist_col])
    if df_clean.empty:
        return go.Figure()
    top_artists = df_clean[artist_col].value_counts().head(10)
    fig = px.bar(
        top_artists,
        x=top_artists.index,
        y=top_artists.values,
        labels={"x": "Artista", "y": "Cantidad de canciones"},
        title="Top 10 Artistas"
    )
    fig.update_layout(height=360)
    return fig


def make_top_songs_list(df):
    name_col = "trackName" if "trackName" in df.columns else "name"
    artist_col = "artistName" if "artistName" in df.columns else "artist"
    pop_col = "msPlayed" if "msPlayed" in df.columns else "popularity"

    required = [c for c in [name_col, artist_col, pop_col] if c]
    df_clean = clean_dataframe(df, required)

    if df_clean.empty:
        return html.P("No hay datos disponibles", className="text-white")

    df_unique = df_clean.drop_duplicates(subset=[name_col, artist_col])
    top_songs = df_unique.nlargest(10, pop_col).reset_index(drop=True)

    items = []
    for i, row in top_songs.iterrows():
        items.append(
            dbc.ListGroupItem(
                [
                    html.Strong(f"{i+1}. {row[name_col]}"),
                    html.Span(f" — {row[artist_col]} (Reproducciones: {row[pop_col]})", className="text-muted")
                ],
                className="bg-dark text-white border-secondary"
            )
        )
    return dbc.ListGroup(items, flush=True)


def make_danceability_energy_scatter(df):
    dance_col = "danceability" if "danceability" in df.columns else None
    energy_col = "energy" if "energy" in df.columns else None
    size_col = "msPlayed" if "msPlayed" in df.columns else None
    name_col = "trackName" if "trackName" in df.columns else "name"
    artist_col = "artistName" if "artistName" in df.columns else "artist"

    df_clean = clean_dataframe(df, [dance_col, energy_col, size_col])
    if df_clean.empty:
        return go.Figure()

    fig = px.scatter(
        df_clean,
        x=dance_col,
        y=energy_col,
        size=size_col,
        color="valence" if "valence" in df_clean.columns else None,
        hover_data=[col for col in [name_col, artist_col] if col in df_clean.columns],
        title="Danceability vs Energy"
    )
    fig.update_layout(height=360)
    return fig


def make_duration_histogram(df):
    if "duration_ms" not in df.columns:
        return go.Figure()
    fig = px.histogram(
        df,
        x="duration_ms",
        nbins=20,
        labels={"duration_ms": "Duración (ms)"},
        title="Distribución de Duración de Canciones"
    )
    fig.update_layout(height=360)
    return fig


def make_dashboard_cards(df):
    artist_col = "artistName" if "artistName" in df.columns else "artist"
    df_clean = clean_dataframe(df, [artist_col, "msPlayed"])
    if df_clean.empty:
        return {"top_artist": None, "top_song": None, "avg_popularity": None, "total_songs": 0}

    top_artist = df_clean[artist_col].value_counts().idxmax()
    top_song = df_clean.loc[df_clean["msPlayed"].idxmax()]["trackName"]
    avg_popularity = round(df_clean["msPlayed"].mean(), 2)
    total_songs = len(df_clean)
    return {
        "top_artist": top_artist,
        "top_song": top_song,
        "avg_popularity": avg_popularity,
        "total_songs": total_songs
    }


def make_mood_pie(df):
    if "mood" not in df.columns:
        return go.Figure()
    mood_counts = df["mood"].value_counts()
    fig = px.pie(
        names=mood_counts.index,
        values=mood_counts.values,
        title="Distribución de emociones"
    )
    fig.update_layout(height=360)
    return fig


def make_top_songs_by_condition(df, condition_col, condition_value, top_n=5):
    name_col = "trackName" if "trackName" in df.columns else ("name" if "name" in df.columns else None)
    artist_col = "artistName" if "artistName" in df.columns else ("artist" if "artist" in df.columns else None)
    pop_col = "msPlayed" if "msPlayed" in df.columns else "popularity"

    if not name_col or not artist_col or condition_col not in df.columns:
        return html.P("Datos insuficientes", className="text-white")

    if condition_col == "energy":  # si es energy usamos > condición
        df_cond = df[df[condition_col] >= condition_value]
    else:
        df_cond = df[df[condition_col] == condition_value]

    df_cond = df_cond.drop_duplicates(subset=[name_col, artist_col])
    top_songs = df_cond.nlargest(top_n, pop_col) if pop_col in df_cond.columns else df_cond.head(top_n)

    items = []
    for i, row in top_songs.iterrows():
        items.append(
            dbc.ListGroupItem(
                [
                    html.Strong(f"{i+1}. {row[name_col]}"),
                    html.Span(f" — {row[artist_col]} (Reproducciones: {row.get(pop_col, '—')})", className="text-muted")
                ],
                className="bg-dark text-white border-secondary"
            )
        )
    return dbc.ListGroup(items, flush=True)


def dashboard_layout():
    # Dataset principal
    cards = make_dashboard_cards(df_main)
    top_artists_fig = make_top_artists_figure(df_main)
    top_songs_list = make_top_songs_list(df_main)
    fig_dance_energy = make_danceability_energy_scatter(df_main)
    fig_duration = make_duration_histogram(df_main)

    # Dataset 1
    fig_mood = make_mood_pie(df_csv1)
    top_happy_songs = make_top_songs_by_condition(df_csv1, "mood", "Happy")
    top_energetic_songs = make_top_songs_by_condition(df_csv1, "energy", 0.7)

    return html.Div([
        dbc.Container(fluid=True, className="p-3", children=[
            html.H1("Dashboard de Canciones", className="text-white bg-dark p-3 rounded"),

            # Tarjetas
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody([html.H5("Artista con más canciones"), html.P(cards["top_artist"] or "—")])), md=3),
                dbc.Col(dbc.Card(dbc.CardBody([html.H5("Canción más popular"), html.P(cards["top_song"] or "—")])), md=3),
                dbc.Col(dbc.Card(dbc.CardBody([html.H5("Promedio Reproducciones"), html.P(str(cards["avg_popularity"]))])), md=3),
                dbc.Col(dbc.Card(dbc.CardBody([html.H5("Total de canciones"), html.P(str(cards["total_songs"]))])), md=3)
            ]),

            html.Hr(),

            # Graficoz dataset principal
            dbc.Row([
                dbc.Col(dcc.Graph(figure=top_artists_fig), md=6),
                dbc.Col(top_songs_list, md=6)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_dance_energy), md=6),
                dbc.Col(dcc.Graph(figure=fig_duration), md=6)
            ]),

            html.Hr(),

            # Dataset 1 d emociones y top canciones
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_mood), md=6),
                dbc.Col([
                    html.H5("Top 5 Canciones Felices"),
                    top_happy_songs,
                    html.Hr(),
                    html.H5("Top 5 Canciones Energéticas"),
                    top_energetic_songs
                ], md=6)
            ]),

            dbc.Button("Inicio", href="/", color="secondary", className="mt-4 d-block mx-auto")
        ])
    ], style={"backgroundColor": "#0f0f0f", "minHeight": "100vh"})
