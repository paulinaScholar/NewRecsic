import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="0000",
        client_secret="0000",
        redirect_uri="http://localhost:5000/callback",
        scope=["user-library-read", "user-top-read", "user-read-playback-state", "user-read-recently-played"]
    ))
    return sp
