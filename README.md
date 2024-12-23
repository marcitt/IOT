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

**Most recent time-series data is available at: `time_series_data/datasets/music-listening-data-23-12-24-8AM.csv`** this has been downloaded from Supabase

# Machine Learning

## OCR
- The Pytesseract OCR wrapper is used to collect data on screen


## Attention Detection
A custom YOLO model was trained on 'focused' and 'distracted' images which can then be used to track the user's attention level 

**Notebooks used for training are included in:**
1. `attention_detection/attention_model_training_yolov5.ipynb` 
2. `attention_detection/attention_model_training_yolov8.ipynb`

**Notebook for Model Testing**
1. `attention_detection/model_test.ipynb`

These can be run in a jupyter notebook which avoids some of the issues presented by OpenCV in MacOS environment by using ipywidgets.

**Models**
A total of 5 different models were trained, the weights for each of these models are stored as:
- `attention_detection/model_iterations/v5/weights/best.pt`
- `attention_detection/model_iterations/v4/weights/best.pt` etc.

1. Model 1 was trained on Yolov5s with 75 images per class ["focused","distracted"] over ~100 epochs
2. Model 2 was trained on Yolov8n with 75 images per class over 500 epochs
3. Model 3 was trained on Yolov8n with 200 images per class over 20 epochs
4. Model 4 was trained on Yolov8n with 200 images per class over 100 epochs
4. Model 5 was trained on Yolov8n with 200 images per class over 350 epochs

Model 5 showed the most optimal performance and was applied for the majority of attention data collection tasks.

# Data Collection

## Data Collection for Attention Detection Model Training
- 7 experiments were defined to collect data for training the YOLO attention detection model, 200 images were collected for each class 'focused' and 'distracted'
- 7 experiments include 4 experiments to collect 'focused' image classes: report-writing (focused/100imgs), research (focused/75imgs), programming (focused/25imgs), planning (focused/10imgs)
- 3 experiments to collect 'distracted' image classes: highly-distracted (distracted/105imgs), distracted (distracted/80imgs), semi-distracted (distracted/15 imgs)

Notebooks used for data collection are included in:
1. `attention_detection/data_collection_images.ipynb`

A few sample images are included in 
`attention_detection/exps` however the full dataset is not uploaded to GitHub (stored on local device).

The full dataset of labels is included in `attention_detection/training_data/labels` which was used in training models v3-v5.

## Time-Series Data Collection
### Time-Series On-Screen Text Data Collectiom
- Text detection function `detect_text()` is kept in `OCR/detect_screen_text.py` which can then be imported into relevant files e.g. streamlit app
- The number of on-screen words is detected using `detect_text()`
- The number of words is then inserted into a column in a Supabase table along with a timestamp and several other recorded metrics

Code available in: `OCR/detect_screen_text.py`

### Time-series Data Collection for User Attention Level
Similary to `detect_text()` the attention detection model was then used to collect time series data, inserting either a DISTRACTED or FOCUSED state, the class score and the model version into the Supabase table along with the timestamp, previously mentioned text reading and song data:

### Time-series Data Collection for Current Playing Song
- In conjunction with data collected through the laptop's hardware data is also collected through Spotify's API
- Using OAuth Authorization and `spotipy` the user's currently playing song is also included in the table INSERT, which will allow us to see how the currently playing song influences attention.

Code available in: `live_data_collection.py` and `music_integration/spotify_functions.py`

## Music metadata Collection
Along with time-series data collection music metadata is collected:

### Lyricalness
- Lyrics are extracted from Genius API using BeautifulSoup
- A lyricalness measure is computed using this data
Code available in: `music_integration/lyricalness/compute_lyricalness.py`

### BPM
- Song BPM data is collected using artist & track name and the deezer client's search functionality 

Code available in: `music_integration/bpm/get_bpm.py` and `music_integration/deezer_functions.py`

# Analysis

## Music Metadata Analysis

### Lyricalness Analysis
Analysis is performed on the collected lyrics data in order to define the lyricalness metric.

### BPM Analysis
Analysis is performed on the collected BPM data in order to define the average values to fill in missing data.

## Time Series Analysis
The available data stored in Supabase provides enough resources to investigate the correlation between lyrics, BPM, on-screen text and attention levels. The data is downloaded locally to a csv and some pre-processing steps are applied to prepare it for analysis (i.e. filling empty values using averages).

A random forest classifer is then trained on this data and the results are used to investigate the importance of different metrics on attention:

The respective feature importances are:
1. Amount of text = 0.5416286
2. BPM = 0.21180063
3. Lyrics = 0.24657078

The effect of lyrics has a stronger influence on focus than BPM - therefore when making reccommendations to the user this should be weighted more strongly.

It makes sense the amount of text on screen correlates the most strongly with focus, as focus is likely to be much higher when more text is on screen as tasks that require a high degree of focus such as reading or writing are likely taking place.

# Applying the Data (Web App)

## Linking to Spotify Data (Basic Client Credientials Workflow)
- User will provide a link to a _public_ playlist (this will only require the client credientials workflow)
- Tracks will be ranked according to current environmental conditions (user attention + volume of onscreen text) and a song will be recommended.
- This creates a foundation for any next steps (e.g. controlling user's spotify playback)

```
# Streamlit Live Plot for Attention:
streamlit run spotify_test.py
```

## Controlling User's Listening Experience (User Authorization Workflow)
- This version of the code will get either the user's current queue or a user's playlist. The code will then perform the same ranking approach.


# Demos

## Running Live Plots

```
# Streamlit Live Plot for Attention:
streamlit run live_music_recommendations.py
```
Will show a live plot for attention - using custom yolov8 model trained on focused & unfocused data 

```
# Streamlit Both Live Plots
streamlit run st_live_plots.py
```
Plots live plots for both attention & text on screen - can be useful for observing relationships between amount of text on screen & how focused the user is



## Labelling Setup Process (not required just for reference)

```
!git clone https://github.com/tzutalin/labelImg

```

```
!pip install pyqt5 lxml --upgrade
!cd labelImg && pyrcc5 -o libs/resources.py resources.qrc
```

## Key Links / Sources
- [A collection of music APIs, databases, and related tools](https://gist.github.com/0xdevalias/eba698730024674ecae7f43f4c650096#audio-identification)
- [Spotify OAuth: Automating Discover Weekly Playlist - Full Tutorial - YouTube](https://www.youtube.com/watch?v=mBycigbJQzA)
- [Python Spotify API #3 - Retrieving Users Songs - YouTube](https://www.youtube.com/watch?v=1TYyX8soQ8M)
- [Deep Drowsiness Detection using YOLO, Pytorch and Python - YouTube](https://www.youtube.com/watch?v=tFNJGim3FXw&t=1971s)
- [Train Yolov8 object detection on a custom dataset | Step by step guide | Computer vision tutorial - YouTube](https://www.youtube.com/watch?v=m9fH9OWn8YM)
