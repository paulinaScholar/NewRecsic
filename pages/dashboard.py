from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .config import DATASET_PATH_2
from flask import session

# Dataset principal
df_main = pd.read_csv(DATASET_PATH_2)


def clean_dataframe(df, required_columns):
    df_clean = df.copy()
    if required_columns:
        existing = [c for c in required_columns if c in df_clean.columns]
        if existing:
            df_clean = df_clean.dropna(subset=existing)
    return df_clean


def make_top_artists_figure(df):
    artist_col = "artistName"
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
    name_col = "trackName"
    artist_col = "artistName"
    pop_col = "msPlayed"  # usamos msPlayed como popularidad

    required = [name_col, artist_col, pop_col]
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
    dance_col = "danceability"
    energy_col = "energy"
    size_col = "msPlayed"
    name_col = "trackName"
    artist_col = "artistName"

    df_clean = clean_dataframe(df, [dance_col, energy_col, size_col])
    if df_clean.empty:
        return go.Figure()

    fig = px.scatter(
        df_clean,
        x=dance_col,
        y=energy_col,
        size=size_col,
        color="valence" if "valence" in df_clean.columns else None,
        hover_data=[name_col, artist_col],
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
    artist_col = "artistName"
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
    if condition_col not in df.columns:
        return html.P("Datos insuficientes", className="text-white")
    df_cond = df[df[condition_col] == condition_value]
    df_cond = df_cond.drop_duplicates(subset=["trackName", "artistName"])
    top_songs = df_cond.nlargest(top_n, "msPlayed") if "msPlayed" in df_cond.columns else df_cond.head(top_n)

    items = []
    for i, row in top_songs.iterrows():
        items.append(
            dbc.ListGroupItem(
                [
                    html.Strong(f"{i+1}. {row['trackName']}"),
                    html.Span(f" — {row['artistName']} (Reproducciones: {row.get('msPlayed', '—')})", className="text-muted")
                ],
                className="bg-dark text-white border-secondary"
            )
        )
    return dbc.ListGroup(items, flush=True)


def dashboard_layout():
    # Dashboard principal
    cards = make_dashboard_cards(df_main)
    top_artists_fig = make_top_artists_figure(df_main)
    top_songs_list = make_top_songs_list(df_main)
    fig_dance_energy = make_danceability_energy_scatter(df_main)
    fig_duration = make_duration_histogram(df_main)
    fig_mood = make_mood_pie(df_main)
    top_happy_songs = make_top_songs_by_condition(df_main, "mood", "Happy")
    top_energetic_songs = make_top_songs_by_condition(df_main, "energy", 0.7)  # energy > 0.7

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

            # Gráficos
            dbc.Row([
                dbc.Col(dcc.Graph(figure=top_artists_fig), md=6),
                dbc.Col(top_songs_list, md=6)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(figure=fig_dance_energy), md=6),
                dbc.Col(dcc.Graph(figure=fig_duration), md=6)
            ]),

            html.Hr(),

            # Top canciones por condición
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
