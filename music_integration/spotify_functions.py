import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

import requests

from dotenv import load_dotenv

import time

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/redirect"
SCOPE = "user-read-currently-playing"
SPOTIFY_GET_CURRENT_TRACK_URL = "https://api.spotify.com/v1/me/player/currently-playing"
# SCOPE = "user-library-read"

from music_integration.lyricalness.compute_lyricalness import compute_lyricalness
from music_integration.bpm.get_bpm import get_song_bpm

# Client credentials method does not require authorization
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


# Client credentials method does not require authorization
def playlist_bpm(playlist_id, sp):
    playlist = sp.playlist_tracks(playlist_id)
    tracks = []
    artists = []
    bpm_list = []
    for item in playlist["items"]:
        artist = item["track"]["artists"][0]["name"]
        track = item["track"]["name"]

        tracks.append(item["track"]["name"])
        artists.append(item["track"]["artists"][0]["name"])

        bpm = get_song_bpm(track, artist)

        bpm_list.append(bpm)

    return tracks, artists, bpm_list


# Authorization is needed for anything that is going to need user data (e.g. getting playlists)
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
    )


# this will get the current track the user is playing
def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status_code == 204:
        return None

    resp_json = response.json()

    track_id = resp_json["item"]["id"]
    track_name = resp_json["item"]["name"]
    artists = resp_json["item"]["artists"]
    artists_names = ", ".join(
        [artist["name"] for artist in artists]
    )  # list comprehension
    link = resp_json["item"]["external_urls"]["spotify"]

    current_track_info = {
        "id": track_id,
        "name": track_name,
        "artists": artists_names,
        "link": link,
    }

    return current_track_info


# sp_oauth = create_spotify_oauth()
# auth_url = sp_oauth.get_authorize_url()
# print(f"Please go to this URL and authorize the app: {auth_url}")
# token_info = sp_oauth.get_access_token()
# info = get_current_track(token_info["access_token"])
# if info:
#     print(info["name"])

# code references:
# Spotify OAuth: Automating Discover Weekly Playlist - Full Tutorial - YouTube: https://www.youtube.com/watch?v=mBycigbJQzA
# Python Spotify API #2 - Setting Up The Endpoints - YouTube: https://www.youtube.com/watch?v=XZA_s-vfGKQ
# Get Currently Playing Track with Spotify API (Python Tutorial) - YouTube: https://www.youtube.com/watch?v=yKz38ThJWqE
