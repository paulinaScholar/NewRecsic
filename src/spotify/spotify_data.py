from .spotify_auth import get_spotify_client
import datetime
from dateutil import parser

def get_listening_days(sp):
    results = sp.current_user_recently_played(limit=50)  
    days_of_week = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    listening_counts = {day: 0 for day in days_of_week.values()}

    if results and "items" in results:
        for track in results["items"]:
            played_at = parser.isoparse(track["played_at"])
            day_of_week = played_at.weekday()
            listening_counts[days_of_week[day_of_week]] += 1

    return listening_counts

def get_recently_played(sp, limit=5):
    results = sp.current_user_recently_played(limit=limit)
    tracks = []
    if results and "items" in results:
        for track in results["items"]:
            tracks.append({
                "name": track["track"]["name"],
                "artist": track["track"]["artists"][0]["name"],
                "link": track["track"]["external_urls"]["spotify"]
            })
    return tracks

def get_top_artists(sp, limit=5):
    results = sp.current_user_top_artists(limit=limit)
    artists = []
    if results and "items" in results:
        for artist in results["items"]:
            artists.append({
                "name": artist["name"],
                "link": artist["external_urls"]["spotify"]
            })
    return artists

def get_top_genres(sp, limit=5):
    results = sp.current_user_top_artists(limit=20)
    genre_count = {}

    if results and "items" in results:
        for artist in results["items"]:
            for genre in artist["genres"]:
                genre_count[genre] = genre_count.get(genre, 0) + 1

    sorted_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)
    return [{"name": genre, "count": count} for genre, count in sorted_genres[:limit]]

def get_top_artist_today(sp):
    today = datetime.datetime.utcnow().date()
    results = sp.current_user_recently_played(limit=50)
    artist_minutes = {}

    if results and "items" in results:
        for track in results["items"]:
            played_at = parser.isoparse(track["played_at"]).date()
            if played_at == today:
                for artist in track["track"]["artists"]:
                    name = artist["name"]
                    artist_minutes[name] = artist_minutes.get(name, 0) + (track["track"]["duration_ms"] / 60000)

    if artist_minutes:
        top_artist = max(artist_minutes.items(), key=lambda x: x[1])
        return {"artist": top_artist[0], "minutes": int(top_artist[1])}
    return {"artist": None, "minutes": 0}

def get_monthly_listening(sp):
    now = datetime.datetime.utcnow()
    current_month = now.month
    results = sp.current_user_recently_played(limit=50)
    total_minutes = 0

    if results and "items" in results:
        for track in results["items"]:
            played_at = parser.isoparse(track["played_at"])
            if played_at.month == current_month:
                total_minutes += track["track"]["duration_ms"] / 60000
    return int(total_minutes)

def get_song_playcount(sp):
    results = sp.current_user_recently_played(limit=50)
    playcount = {}

    if results and "items" in results:
        for track in results["items"]:
            song_name = track["track"]["name"]
            playcount[song_name] = playcount.get(song_name, 0) + 1

    if playcount:
        most_played = max(playcount.items(), key=lambda x: x[1])
        return {"song": most_played[0], "count": most_played[1]}
    return {"song": None, "count": 0}

def get_listening_hours(sp):
    results = sp.current_user_recently_played(limit=50)
    heatmap_data = [[0 for _ in range(24)] for _ in range(7)]

    if results and "items" in results:
        for track in results["items"]:
            played_at = parser.isoparse(track["played_at"])
            weekday = played_at.weekday()
            hour = played_at.hour
            heatmap_data[weekday][hour] += 1

    return heatmap_data

def get_ticket_data(sp):
    return {
        "top_genres": get_top_genres(sp),
        "top_artist_today": get_top_artist_today(sp),
        "song_playcount": get_song_playcount(sp),
        "monthly_listening": get_monthly_listening(sp)
    }
