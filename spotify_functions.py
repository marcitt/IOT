import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from lyricalness.lyricalness import compute_lyricalness

def playlist_lyricalness(playlist_id, sp):
    playlist = sp.playlist_tracks(playlist_id)
    tracks = []
    artists = []
    lyricalness = []
    for item in playlist["items"]:
        artist = item["track"]["artists"][0]["name"]
        track = item["track"]["name"]

        tracks.append(item["track"]["name"])
        artists.append(item["track"]["artists"][0]["name"])

        lyricalness_metric = compute_lyricalness(artist, track)

        if lyricalness_metric:
            lyricalness.append(lyricalness_metric)
        else:
            # make assumption lyricalness is average
            lyricalness.append(200)

    return tracks, artists, lyricalness
