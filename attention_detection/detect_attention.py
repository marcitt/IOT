# this module gets the users attention

import cv2
import time
import numpy as np

# ml imports
import torch
import torchvision
import torchaudio

import os
from ultralytics import YOLO

model = YOLO("attention_detection/model_iterations/v2/weights/last.pt")

def measure_attention():
    cam = cv2.VideoCapture(0)
    time.sleep(0.11) # give a bit of time to sleep to avoid glare 
    _, img = cam.read()

    results = model(img)[0]

    for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result

            if class_id == 16: #focused
                return 2 + score*0.2
                break
            if class_id == 15: #unfoucsed
                return 1 - score*0.2
                break
    
    return None