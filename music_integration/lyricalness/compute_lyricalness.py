# this module defines relevant methods for extracting song data in relation to lyrics

from bs4 import BeautifulSoup
import re

import requests

import os


def prepare_url(artist, song):
    artist_lower = artist.lower()
    artist_clean = re.sub(
        r"[^a-zA-Z0-9 ]", "", artist_lower
    )  # remove non alphanumeric characters + keep spaces using a regular expression
    # reference: https://flexiple.com/python/remove-non-alphanumeric-characters-python

    artist_url = artist_clean.replace(" ", "-").capitalize()  # convert to kebab case

    song_lower = song.lower()
    song_clean = re.sub(
        r"[^a-zA-Z0-9 ]", "", song_lower
    )  # remove non alphanumeric characters + keep spaces
    song_url = song_clean.replace(" ", "-")  # convert to kebab case

    # prepre for genius format:
    url = "https://genius.com/" + artist_url + "-" + song_url + "-lyrics"

    return url


def get_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, "html.parser")
    lyrics_divs = html.find_all("div", attrs={"data-lyrics-container": "true"})

    if not lyrics_divs:
        print(f"Could not find lyrics for {url}")
        return None

    lyrics = "\n".join([div.get_text(separator="\n") for div in lyrics_divs])
    lyrics = re.sub(r"[\(\[].*?[\)\]]", "", lyrics)
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])

    return lyrics
    # reference: https://medium.com/@rachit.lsoni/scraping-song-lyrics-a-fun-and-practical-guide-c0b07e8e7312


def compute_lyricalness(artist, song):
    url = prepare_url(artist, song)
    lyrics = get_lyrics(url)

    if lyrics:
        # for initial implementation use simple measure of number of words per song
        lyricalness = len(lyrics.split())

        # to make the measure more complex we can divide it by the maxium lyricalness which should set the value to less than 1
        # values in the range 0-1 are much easier to interpret 

        # the maxium lyricalness appears to be around ~700
        # there we could return:
        # lyricalness = lyricalness/700

        # it would be useful to do more complex analysis - potentially looking at measures of dispersion or frequency?

        return lyricalness
    else:
        return None
        # from testing average lyricalness was determined to be around 275
        # therefore if it is more useful to return a value this can be returned instead
        # return 275
