import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

os.environ["SPOTIPY_CLIENT_ID"] = "54b3ffcb9b85494aa3ca79a540013c94"
os.environ["SPOTIPY_CLIENT_SECRET"] = "68d913a2f09f4086ab7ab1244816d99b"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8080"


spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

df = pd.read_pickle(".\data\hot_100.pkl")

list_df = df.to_dict(orient="records")

for item in list_df:
    try:
        result = spotify.search(
            f"""track:{item['title']} artist:{item['artist']}""", type="track", limit=1
        )
        if len(result["tracks"]["items"]) > 0:
            item["spotify_uri"] = result["tracks"]["items"][0]["uri"]
        else:
            item["spotify_uri"] = np.nan
    except spotipy.client.SpotifyException as e:
        item["spotify_uri"] = str(e.http_status) + " - " + e.msg

df = pd.DataFrame(list_df)

df = df.dropna()
df = df[~df["spotify_uri"].str.contains("Not found")]

df.to_pickle(r"C:\Users\paulh\Desktop\Data Science Projects\data\songs.pkl")
