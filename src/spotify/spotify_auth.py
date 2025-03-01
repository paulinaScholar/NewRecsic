import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="e8924ad5551f47098c6633a842da8bd6",
        client_secret="e26d8ac769614f8ab9bcc6498496b5d3",
        redirect_uri="http://localhost:5000/callback",
        scope=["user-library-read", "user-top-read", "user-read-playback-state", "user-read-recently-played"]
    ))
    return sp
