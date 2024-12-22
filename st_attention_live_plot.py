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

st.title("Attention Detection Dashboard")

from attention_detection.detect_attention import measure_attention

attention_timestamps = []
attention_readings = []

attention_placeholder = st.empty()

for seconds in range(100):
    df_attention = pd.DataFrame(dict(x=attention_timestamps, y=attention_readings))
    fig_attention = px.line(df_attention, x="x", y="y", title="Attention Plot")
    attention_placeholder.plotly_chart(
        fig_attention, key=f"attention-{seconds}"
    )

    attention_timestamps.append(datetime.datetime.now())
    attention_readings.append(measure_attention())


