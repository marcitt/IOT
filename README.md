# IOT

## Setup
Setup virtual environment: 

```
# MACOS
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements_20_12_24.txt
```

## Running Live Plots

```
# Streamlit Live Plot for Attention:
streamlit run st_attention_live_plot.py
```
Will show a live plot for attention - using custom yolov8 model trained on focused & unfocused data 

```
# Streamlit Both Live Plots
streamlit run st_live_live_plots.py
```
Plots live plots for both attention & text on screen - can be useful for observing relationships between amount of text on screen & how focused the user is

## Linking to Spotify Data (Basic Client Credientials Workflow)
- User will provide a link to a playlist
- Tracks will be ranked according to current environmental conditions