from supabase import create_client, Client
import time
from datetime import datetime, date

import os
from dotenv import load_dotenv

from OCR.detect_screen_text import detect_text
from ultralytics import YOLO

# ml imports
import torch
import torchvision
import torchaudio

import cv2

from music_integration.spotify_functions import get_current_track, create_spotify_oauth

load_dotenv()

model_verson = "v4"

model = YOLO(f"attention_detection/model_iterations/{model_verson}/weights/best.pt")


supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(supabase_url=supabase_url, supabase_key=supabase_key)

sp_oauth = create_spotify_oauth()
auth_url = sp_oauth.get_authorize_url()
print(f"Please go to this URL and authorize the app: {auth_url}")
token_info = sp_oauth.get_access_token()


for samples in range(1000):

    print("DETECT ATTENTION")
    cam = cv2.VideoCapture(0)
    time.sleep(0.11)  # give a bit of time to sleep to avoid glare
    _, img = cam.read()

    results = model(img)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        attention = f"{results.names[int(class_id)].upper()}"

    print("DETECT TEXT")
    text_reading = detect_text()

    print("DETECT SONG")
    info = get_current_track(token_info["access_token"])
    name = info["name"]
    artists = info["artists"]
    track_id = info["id"]

    timestamp = str(datetime.now())

    print("INSERT")
    rresponse = (
        supabase.table("Text+Attention+Spotify")
        .insert(
            {
                "timestamp": timestamp,
                "text-reading": text_reading,
                "attention-class": attention,
                "class-score": round(score, 6),
                "model-version": f"attention-detection-{model_verson}",
                "track-title": name,
                "artist": artists,
                "track-id": str(track_id),
            }
        )
        .execute()
    )

    delay = 15
    print(f"wait {delay} seconds")
    time.sleep(delay)
    print("resume collection")
