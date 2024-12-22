import deezer
import requests

client = deezer.Client()


def get_song_bpm(track, artist):
    try:
        result = client.search(track=track, artist=artist)

        if result:
            print(f"getting bpm for {track} by {artist}")
            bpm = result[0].bpm
            if bpm:
                return bpm
            else:
                print("BPM not found")
                return None
        else:
            print("Song not found")
            return None

    # GPT-4 was used to generate error handling code here:
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 403:
            print(
                "403 Error: Access Forbidden. Please check your API key or authentication."
            )
        else:
            print(f"HTTP error occurred: {http_err}")  # For other HTTP errors
    except Exception as err:
        print(f"An error occurred: {err}")
