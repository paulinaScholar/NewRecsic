# spotify_auth.py
from flask import session, redirect, request
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from server_instance import server
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# --- Configuración de scopes ---
SPOTIPY_SCOPES = (
    "user-read-private "
    "user-read-email "
    "user-top-read "
    "user-read-recently-played "
    "user-read-currently-playing "
    "user-read-playback-state "
    "user-read-playback-position "
    "user-library-read "
    "playlist-read-private"
)

# --- Función para obtener el objeto SpotifyOAuth ---
def get_spotify_oauth():
    # Cache persistente por usuario (útil para desarrollo)
    cache_path = ".spotify-token-cache"
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),  # Debe coincidir EXACTO con Spotify Dashboard
        scope=SPOTIPY_SCOPES,
        cache_path=cache_path
    )

# --- Rutas de autenticación ---
@server.route("/login_spotify")
def login_spotify():
    session.pop("token_info", None)  # Limpiar token anterior
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@server.route("/callback")
def callback():
    sp_oauth = get_spotify_oauth()
    code = request.args.get("code")
    if not code:
        return "Error: No se recibió código de autorización", 400

    # Obtener token de acceso
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect("/dashboard")

@server.route("/logout_spotify")
def logout_spotify():
    session.pop("token_info", None)
    return redirect("/inicio")

# --- Funciones auxiliares ---
def get_spotify_client():
    token_info = session.get("token_info")
    if not token_info:
        return None

    sp_oauth = get_spotify_oauth()

    # Refrescar token si está expirado
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = token_info

    return Spotify(auth=token_info["access_token"])

def is_user_authenticated():
    return "token_info" in session

# --- Función segura para llamadas a Spotify ---
def safe_spotify_call(fn, *args, **kwargs):
    """
    Ejecuta la función fn(sp, *args, **kwargs) solo si el usuario está autenticado.
    Si no lo está, redirige al login de Spotify.
    """
    sp = get_spotify_client()
    if not sp:
        return redirect("/login_spotify")
    try:
        return fn(sp, *args, **kwargs)
    except Exception as e:
        print(f"[Spotify Error] {e}")
        return None

