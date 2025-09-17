from .spotify_auth import get_spotify_client
import datetime
import random

def get_listening_days():
    sp = get_spotify_client()
    results = sp.current_user_recently_played(limit=50)  
    if results and "items" in results:
        days_of_week = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        listening_counts = {day: 0 for day in days_of_week.values()}

        for track in results["items"]:
            played_at = track["played_at"]
            date_obj = datetime.datetime.strptime(played_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            day_of_week = date_obj.weekday()
            listening_counts[days_of_week[day_of_week]] += 1

        return listening_counts
    return {}

def get_recently_played():
    sp = get_spotify_client()
    results = sp.current_user_recently_played(limit=5)
    if results and "items" in results:
        tracks = [
            {
                "name": track["track"]["name"],
                "artist": track["track"]["artists"][0]["name"],
                "link": track["track"]["external_urls"]["spotify"]
            }
            for track in results["items"]
        ]
        return tracks
    return []

def get_top_artists():
    sp = get_spotify_client()
    results = sp.current_user_top_artists(limit=5)
    if results and "items" in results:
        artists = [
            {
                "name": artist["name"],
                "link": artist["external_urls"]["spotify"]
            }
            for artist in results["items"]
        ]
        return artists
    return []

# 🔹 Obtener los géneros principales
def get_top_genres():
    sp = get_spotify_client()
    results = sp.current_user_top_artists(limit=20)  
    genre_count = {}

    if results and "items" in results:
        for artist in results["items"]:
            for genre in artist["genres"]:
                genre_count[genre] = genre_count.get(genre, 0) + 1

        sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
        return [{"name": genre, "count": count} for genre, count in sorted_genres[:5]]  # Top 5 géneros

    return []

# 🔹 Obtener trivia divertida sobre el historial musical
def get_music_trivia():
    sp = get_spotify_client()
    results = sp.current_user_top_tracks(limit=50)  

    if results and "items" in results:
        total_duration = sum(track["duration_ms"] for track in results["items"]) / 60000  # Minutos
        most_popular = max(results["items"], key=lambda x: x["popularity"])["name"]
        least_popular = min(results["items"], key=lambda x: x["popularity"])["name"]

        trivia = [
            f"ESCUCHASTE UN TOTAL DE {int(total_duration)} MINUTOS DE PARTE DE TU TOP 50 🎵",
            f"TU CANCION MAS POPULAR ES '{most_popular}' 🌟",
            f"TU GEMA OCULTA ES'{least_popular}', NADIE SABE DE ELLA! 🎶",
            f"TIENES UN EXCELENTE GUSTO, ESCUCHAS JOYAS QUE NO APARECEN EN LOS TOP 50 🎧"
        ]

        return trivia

    return ["We need more data to generate fun facts! Keep listening to more music! 🎶"]

# 🔹 Obtener los podcasts más escuchados
def get_top_podcasts():
    sp = get_spotify_client()
    results = sp.current_user_top_artists(limit=10)  

    podcasts = [
        {"name": artist["name"], "link": artist["external_urls"]["spotify"]}
        for artist in results["items"] if "podcast" in artist["genres"]
    ]

    return podcasts[:5] if podcasts else [{"name": "No podcast data available!", "link": "#"}]

def search_track(track_name, limit=5):
    sp = get_spotify_client()
    results = sp.search(q=track_name, type="track", limit=limit)
    tracks = results["tracks"]["items"]

    if not tracks:
        print("No se ha encontrado la cancion.")
        return
    
    for idx, track in enumerate(tracks):
        artists = ", ".join([artist["name"] for artist in track["artists"]])
        print(f"{idx+1}. 🎵 {track['name']} - {artists}")
        print(f"   🔗 Spotify URL: {track['external_urls']['spotify']}")
        print(f"   📀 Album: {track['album']['name']}")
        print("-" * 50)

# Example: Search for "The Weeknd"
# search_artist("The Weekend")
