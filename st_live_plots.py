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

st.title("Dashboard")

from attention_detection.detect_attention import measure_attention
from OCR.detect_screen_text import detect_text

text_timestamps = []
text_readings = []

attention_timestamps = []
attention_readings = []

attention_placeholder = st.empty()
text_placeholder = st.empty()

for seconds in range(100):
    df_attention = pd.DataFrame(dict(x=attention_timestamps, y=attention_readings))
    fig_attention = px.line(df_attention, x="x", y="y", title="Attention Level")
    attention_placeholder.plotly_chart(fig_attention, key=f"attention-{seconds}")

    attention_timestamps.append(datetime.datetime.now())
    attention_readings.append(measure_attention())

    # text plot
    df_text = pd.DataFrame(dict(x=text_timestamps, y=text_readings))

    fig_text = px.line(df_text, x="x", y="y", title="Text Patterns")
    text_placeholder.plotly_chart(fig_text, key=f"text-{seconds}")

    text_timestamps.append(datetime.datetime.now())
    text_readings.append(detect_text())
