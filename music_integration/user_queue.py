# doing some testing on how to get user's queue - unfortunately requires spotify premium to add tracks to queue

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


from spotipy.oauth2 import SpotifyOAuth
import spotipy

# Define your app credentials
scope = "user-read-currently-playing user-read-playback-state"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=scope,
    )
)

track_uri = "1jdMtDMjbzjgMCfX4SfxtR"
sp.add_to_queue(track_uri)

