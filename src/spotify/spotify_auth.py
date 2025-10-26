import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
<<<<<<< HEAD
        client_id="69d53a8c1d1347678e02a0f6f6f5a555",
        client_secret="bf4e1a18cf4a4e68afbb929d844c734d",
=======
        client_id="0000",
        client_secret="0000",
>>>>>>> e3ea3870e4e2bd04fb129258635620f5855303c7
        redirect_uri="http://localhost:5000/callback",
        scope=["user-library-read", "user-top-read", "user-read-playback-state", "user-read-recently-played"]
    ))
    return sp
