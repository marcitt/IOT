import streamlit as st
from PIL import ImageGrab
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px  # interactive charts
import pandas as pd
import random
import time
import os
import datetime
import cv2
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import os

from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Authentication - use of client cred
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret,
)


sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# playlist_id = "5sqTWC2JizYpImP7XLEUya"

# playlist = sp.playlist_tracks(playlist_id)
# tracks = []
# artists = []
# for item in playlist["items"]:
#     tracks.append(item["track"]["name"])
#     artists.append(item["track"]["artists"][0]["name"])

from spotify_functions import playlist_lyricalness

st.title("Dashboard")
playlist_URL = st.text_input(
    label="Spotify playlist:",
    placeholder="https://open.spotify.com/playlist/2gxanso58gjX1oYISHXEG3?si=4493f3927f714154",
    value="https://open.spotify.com/playlist/2gxanso58gjX1oYISHXEG3?si=4493f3927f714154",
)

table_placeholder = st.empty()

playlist_URI = playlist_URL.split("/")[-1].split("?")[0]

tracks, artists, lyricalness = playlist_lyricalness(playlist_id=playlist_URI, sp=sp)

dict = {
    "titles": tracks,
    "artists": artists,
    "lyricalness": lyricalness,
}

df = pd.DataFrame.from_dict(dict)

table_placeholder.table(df)
