import os
from flask import Flask, session

from dotenv import load_dotenv

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

redirect_uri = "http://localhost:5000/callback"
scope = "playlist-read-private"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64) #store in env or credentials manager

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)

@app.route("/")
def home():
    # validate token allows us to check if we have a valid token that hasn't expired
    # what is the cache handler?  
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_playlists'))

if __name__ == '__main__':
    app.run(debug=True)


# REFERENCES:
# https://www.youtube.com/watch?v=2if5xSaZJlg
