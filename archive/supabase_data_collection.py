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

load_dotenv()

model = YOLO("attention_detection/model_iterations/v2/weights/best.pt")


supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_API_KEY")

supabase: Client = create_client(supabase_url=supabase_url, supabase_key=supabase_key)

for samples in range(5000):

    print("DETECT ATTENTION")
    cam = cv2.VideoCapture(0)
    time.sleep(0.11) # give a bit of time to sleep to avoid glare 
    _, img = cam.read()

    results = model(img)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        attention = f"{results.names[int(class_id)].upper()}"

    print("DETECT TEXT")
    text_reading = detect_text()

    timestamp = str(datetime.now())


    print("INSERT")
    rresponse = (
        supabase.table("Text-Attention-Detection")
        .insert(
            {
                "timestamp": timestamp,
                "text-reading": text_reading,
                "attention-class": attention,
                "class-score": round(score, 6),
                "model-version": "attention-detection-v2"
            }
        )
        .execute()
    )
