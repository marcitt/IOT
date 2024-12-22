# DESE71003 – SENSING AND INTERNET OF THINGS COURSEWORK SUBMISSION

# Setup

## Virtual Environment Setup
```
# MACOS
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```
## .env requirements
```
CLIENT_ID=
CLIENT_SECRET=

SUPABASE_URL=
SUPABASE_API_KEY=

SPOTIFY_ACCESS_TOKEN=
```

# Demos

## Testing Attention Detection Models
These can be run in a jupyter notebook which avoids some of the issues presented by OpenCV in MacOS environment by using ipywidgets

The weights for each version of the model are stored in the repo and can be loaded by running the relevant cells 


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
- User will provide a link to a _public_ playlist (authorization workflow is required for private playlists)
- Tracks will be ranked according to current environmental conditions 
```
# Streamlit Live Plot for Attention:
streamlit run spotify_test.py
```

## Labelling Setup Process (not required just for reference)

```
!git clone https://github.com/tzutalin/labelImg

```
!pip install pyqt5 lxml --upgrade
!cd labelImg && pyrcc5 -o libs/resources.py resources.qrc
```


