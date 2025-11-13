
from flask import session, redirect, request
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from server_instance import server
import os
from dotenv import load_dotenv

load_dotenv()

# --- Scopes ---
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

# --- Configuración OAuth (sin cache global) ---
def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=SPOTIPY_SCOPES,
        cache_path=None,   # ❗ Evita tokens compartidos entre usuarios
        show_dialog=True   # Mantiene permisos actualizados
    )

# --- LOGIN ---
@server.route("/login_spotify")
def login_spotify():
    session.pop("token_info", None)
    sp_oauth = get_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# --- CALLBACK ---
@server.route("/callback")
def callback():
    sp_oauth = get_spotify_oauth()
    code = request.args.get("code")

    if not code:
        return "Error: No se recibió código de autorización", 400

    # Spotipy v2 usa este método correctamente
    token_info = sp_oauth.get_access_token(code, as_dict=True)

    if not token_info:
        return "Error obteniendo el token de Spotify", 400

    # Guardar token por usuario en la sesión
    session["token_info"] = token_info

    return redirect("/dashboard")

# --- LOGOUT ---
@server.route("/logout_spotify")
def logout_spotify():
    session.pop("token_info", None)
    return redirect("/inicio")

# --- CLIENTE SPOTIFY ---
def get_spotify_client():
    token_info = session.get("token_info")

    if not token_info:
        return None

    sp_oauth = get_spotify_oauth()

    # Refrescar token si expiró
    if sp_oauth.is_token_expired(token_info):
        refreshed_token = sp_oauth.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = refreshed_token
        token_info = refreshed_token

    return Spotify(auth=token_info["access_token"])

# --- Comprobar autenticación ---
def is_user_authenticated():
    return "token_info" in session

# --- Función segura ---
def safe_spotify_call(fn, *args, **kwargs):
    sp = get_spotify_client()
    if not sp:
        return redirect("/login_spotify")
    try:
        return fn(sp, *args, **kwargs)
    except Exception as e:
        print(f"[Spotify Error] {e}")
        return None

