import streamlit as st
from PIL import ImageGrab
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os

from sklearn import preprocessing

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# custom IOT functions:
from spotify_functions import playlist_lyricalness
from detect_screen_text import detect_text

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Authentication - use of client cred
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret,
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

st.title("Queuing Songs based on Environmental Conditions")
playlist_URL = st.text_input(
    label="Spotify playlist:",
    placeholder="https://open.spotify.com/playlist/2gxanso58gjX1oYISHXEG3?si=4493f3927f714154",
    value="https://open.spotify.com/playlist/2gxanso58gjX1oYISHXEG3?si=4493f3927f714154",
)

table_placeholder = st.empty()
text_placeholder = st.empty()
recommendation_placeholder = st.empty()
desired_lyricalness_placeholder = st.empty()

min_lyricalness = 0
max_lyricalness = 600
max_text = 700
min_text = 20

def compute_desired_lyricalness(reading):
    if reading < min_text:
        reading = min_text

    if reading > max_text:
        reading = max_text

    x_0 = min_text
    x_1 = max_text
    y_0 = min_lyricalness
    y_1 = max_lyricalness
    x = reading

    return y_0 + (x - x_0) * ((y_1 - y_0) / (x_1 - x_0)) #interpolation


playlist_URI = playlist_URL.split("/")[-1].split("?")[0]

tracks, artists, lyricalness = playlist_lyricalness(playlist_id=playlist_URI, sp=sp)

for seconds in range(35):
    text_reading = detect_text()

    desired_lyricalness = compute_desired_lyricalness(text_reading)

    lyricalness_differences = [
        abs(x - desired_lyricalness) for x in lyricalness
    ]
    lyricalness_differences = preprocessing.normalize(np.array([lyricalness_differences]))
    lyricalness_differences = list(lyricalness_differences[0])

    text_placeholder.text(f"Current number of words on screen: {text_reading}")
    desired_lyricalness_placeholder.text(f"Desired lyricalness: {round(desired_lyricalness,4)}")

    dict = {
        "titles": tracks,
        "artists": artists,
        "lyricalness": lyricalness,
        "difference": lyricalness_differences
    }

    df = pd.DataFrame.from_dict(dict)
    sorted_df = df.sort_values(by="difference")

    table_placeholder.table(df)

    recommendation_placeholder.text(f"Next recommended song: {df["titles"][0]}")

    time.sleep(1)
