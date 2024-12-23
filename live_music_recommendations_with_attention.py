import streamlit as st
from PIL import ImageGrab
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os

# ml imports
# import torch
# import torchvision
# import torchaudio

# from ultralytics import YOLO

import deezer

from sklearn import preprocessing

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# custom IOT functions:
from music_integration.spotify_functions import playlist_lyricalness
from music_integration.spotify_functions import playlist_bpm
from OCR.detect_screen_text import detect_text

from attention_detection.detect_attention import measure_attention_and_score

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
    placeholder="https://open.spotify.com/playlist/6DyMf846DRvYGOw3cEGyeD?si=8b7cea1b799e4aaf",
    value="https://open.spotify.com/playlist/6DyMf846DRvYGOw3cEGyeD?si=8b7cea1b799e4aaf",
)

table_placeholder = st.empty()
text_placeholder = st.empty()
attention_placeholder = st.empty()
motivation_placeholder = st.empty()
recommendation_placeholder = st.empty()
desired_lyricalness_placeholder = st.empty()
desired_bpm_placeholder = st.empty()

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
    y_1 = min_lyricalness
    y_0 = max_lyricalness
    x = reading

    return y_0 + (x - x_0) * ((y_1 - y_0) / (x_1 - x_0))  # interpolation


min_motivation_metric = 0
max_motivation_metric = 1
max_bpm = 300
min_bpm = 30


def compute_desired_BPM(reading):
    if reading < min_motivation_metric:
        reading = min_motivation_metric

    if reading > max_motivation_metric:
        reading = max_motivation_metric

    x_0 = min_motivation_metric
    x_1 = max_motivation_metric
    y_1 = min_bpm
    y_0 = max_bpm
    x = reading

    return y_0 + (x - x_0) * ((y_1 - y_0) / (x_1 - x_0))  # interpolation


playlist_URI = playlist_URL.split("/")[-1].split("?")[0]

tracks, artists, lyricalness = playlist_lyricalness(playlist_id=playlist_URI, sp=sp)
tracks, artists, bpm = playlist_bpm(playlist_id=playlist_URI, sp=sp)

motivation_metric = 0.5 #this metric gets updated throughout the loop - it acts a bit like a rolling average

attention_display = ""

for seconds in range(50):
    text_reading = detect_text()
    attention_reading, score = measure_attention_and_score()

    if attention_reading < 0.5:
        motivation_metric = motivation_metric - score*0.01
        attention_display="Distracted"
    if attention_reading > 0.5:
        motivation_metric = motivation_metric + score * 0.01
        attention_display = "Focused"

    if motivation_metric > 1:
        motivation_metric = 1
    if motivation_metric < 0:
        motivation_metric = 0

    desired_lyricalness = compute_desired_lyricalness(text_reading)
    desired_bpm = compute_desired_BPM(motivation_metric)

    lyricalness_differences = [abs(x - desired_lyricalness) for x in lyricalness]
    lyricalness_differences = preprocessing.normalize(
        np.array([lyricalness_differences])
    )
    lyricalness_differences = list(lyricalness_differences[0])

    bpm_differences = [abs(x - desired_bpm) for x in bpm]
    bpm_differences = preprocessing.normalize(
        np.array([bpm_differences])
    )
    bpm_differences = list(bpm_differences[0])

    text_placeholder.text(f"Current number of words on screen: {text_reading}")
    attention_placeholder.text(f"Current user state: {attention_display}")
    motivation_placeholder.text(f"Current motivation metric: {round(motivation_metric,2)}")
    desired_lyricalness_placeholder.text(
        f"Desired lyricalness: {round(desired_lyricalness,2)}"
    )

    desired_bpm_placeholder.text(
        f"Desired bpm: {round(desired_bpm,2)}"
    )

    BPM_weighting = 0.45775001
    lyrical_weighting = 0.54224999

    # weightings are assigned using feature importance from the random forest code
    summative = [
        round((BPM_weighting * bpm) + (lyrical_weighting * lyric),2)
        for bpm, lyric in zip(bpm_differences, lyricalness_differences)
    ]

    dict = {
        "titles": tracks,
        "artists": artists,
        "lyricalness": lyricalness,
        "bpm": bpm,
        "norm lyrical diff": lyricalness_differences,
        "norm bpm diff": bpm_differences,
        "norm summary diff": summative
    }

    df = pd.DataFrame.from_dict(dict)
    sorted_df = df.sort_values(by="norm summary diff")

    table_placeholder.table(sorted_df)


    # recommendation_placeholder.text(f"Next recommended song: {sorted_df['titles'][0]}")

    time.sleep(1)
