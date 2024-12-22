import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

from dotenv import load_dotenv

from flask import Flask, request, url_for, session, redirect
import time

load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/redirect"
# SCOPE = "user-read-currently-playing"
SCOPE = "user-library-read"

app.secret_key = os.getenv("APP_SECRET_KEY")
app.config["SESSION_COOKIE_NAME"] = "My Cookie"
TOKEN_INFO = "token_info"


@app.route("/")
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/redirect")
def redirectPage():

    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info

    return "redirect"

@app.route("/getTracks")
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        redirect(url_for("login", _external=True))
    sp = spotipy.Spotify(auth=token_info["access_token"])
    return sp.current_user_saved_tracks(limit=50,offset=0)

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info["expires_at"] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info


# better to create a function to create the OAuth Object - prevents potential errors
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for("redirectPage", _external=True),
        scope=SCOPE,
    )

if __name__ == "__main__":
    app.run(port=5000)

# code references:
# Spotify OAuth: Automating Discover Weekly Playlist - Full Tutorial - YouTube: https://www.youtube.com/watch?v=mBycigbJQzA
# Python Spotify API #2 - Setting Up The Endpoints - YouTube: https://www.youtube.com/watch?v=XZA_s-vfGKQ
