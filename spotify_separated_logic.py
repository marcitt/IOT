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

# better to create a function to create the OAuth Object - prevents potential errors
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
    )


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

sp_oauth = create_spotify_oauth()
auth_url = sp_oauth.get_authorize_url()
# print(f"Please go to this URL and authorize the app: {auth_url}")

token_info = sp_oauth.get_access_token(
    "authorization_code_received_here"
)  # Authorization code from UR

# print(token_info)

info = get_current_track(token_info["access_token"])

if info:
    print(info["name"])