# src/spotify/spotify_data.py
import traceback

def safe_call(default):
    """Decorador para evitar que un fallo rompa el dashboard."""
    def decorator(fn):
        def wrapper(sp, *args, **kwargs):
            try:
                return fn(sp, *args, **kwargs)
            except Exception as e:
                print(f"[spotify_data] Error en {fn.__name__}: {e}")
                traceback.print_exc()
                return default
        return wrapper
    return decorator

# ---------------------------
# 🎵 DATOS PÚBLICOS DE SPOTIFY
# ---------------------------

@safe_call([])
def get_top_50_tracks_mexico(sp):
    """Obtiene el Top 50 Canciones México desde playlist pública."""
    playlist_id = "37i9dQZEVXbMXbN3EUUhlg"  # Top 50 México
    data = sp.playlist_items(playlist_id, limit=50)
    tracks = []

    for item in data.get("items", []):
        track = item.get("track", {})
        tracks.append({
            "name": track.get("name"),
            "artists": ", ".join([a.get("name") for a in track.get("artists", [])]),
            "popularity": track.get("popularity"),
            "duration_ms": track.get("duration_ms"),
            "album": track.get("album", {}).get("name"),
            "release_date": track.get("album", {}).get("release_date")
        })
    return tracks

@safe_call([])
def get_top_artists_global(sp, limit=50):
    """Obtiene artistas más populares globalmente usando playlists públicas de Spotify Charts."""
    playlist_id = "37i9dQZF1DXbMDoHDwVN2t"  # Global Top 50
    data = sp.playlist_items(playlist_id, limit=limit)
    artists_count = {}
    
    for item in data.get("items", []):
        track = item.get("track", {})
        for a in track.get("artists", []):
            name = a.get("name")
            if name:
                artists_count[name] = artists_count.get(name, 0) + 1

    top_artists = sorted(artists_count.items(), key=lambda x: x[1], reverse=True)
    return [{"artist": a, "count": c} for a, c in top_artists[:limit]]

@safe_call({})
def get_ticket_data(sp):
    """
    Regresa datos resumidos para el dashboard tipo 'Recsumen':
    - Top 50 canciones México
    - Top artistas globales
    """
    top_tracks = get_top_50_tracks_mexico(sp)
    top_artists = get_top_artists_global(sp)
    
    # Datos resumidos para tarjetas
    top_song = top_tracks[0]["name"] if top_tracks else None
    top_song_artist = top_tracks[0]["artists"] if top_tracks else None

    top_artist_count = top_artists[0]["artist"] if top_artists else None

    return {
        "top_tracks": top_tracks,
        "top_artists": top_artists,
        "top_song": {"name": top_song, "artist": top_song_artist},
        "top_artist": {"artist": top_artist_count}
    }

