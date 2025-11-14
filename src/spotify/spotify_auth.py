# src/spotify/spotify_auth.py
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def get_spotify_client():
    """
    Regresa un cliente Spotify usando credenciales de aplicación
    (no usuario), ideal para obtener top charts o playlists públicas.
    """
    try:
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET")
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return sp
    except Exception as e:
        print("Error creando cliente Spotify:", e)
        return None

