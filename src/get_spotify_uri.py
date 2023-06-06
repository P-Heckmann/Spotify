import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# Set the required environment variables for Spotify API authentication
os.environ["SPOTIPY_CLIENT_ID"] = "..."
os.environ["SPOTIPY_CLIENT_SECRET"] = "..."
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8080"

# Initialize the Spotify API client
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Read the pickle file "hot_100.pkl" into a DataFrame
df = pd.read_pickle(".\data\hot_100.pkl")

# Convert the DataFrame to a list of dictionaries
list_df = df.to_dict(orient="records")

# Iterate over each item in the list and query the Spotify API for track information
for item in list_df:
    try:
        # Search for a track based on the item's title and artist using the Spotify API
        result = spotify.search(
            f"""track:{item['title']} artist:{item['artist']}""", type="track", limit=1
        )
        if len(result["tracks"]["items"]) > 0:
            # Store the URI of the first track in the search result
            item["spotify_uri"] = result["tracks"]["items"][0]["uri"]
        else:
            # If no track is found, set the URI as NaN
            item["spotify_uri"] = np.nan
    except spotipy.client.SpotifyException as e:
        # If an exception occurs, store the exception details in the URI
        item["spotify_uri"] = str(e.http_status) + " - " + e.msg

# Create a new DataFrame from the updated list of dictionaries
df = pd.DataFrame(list_df)

# Drop rows with NaN values in the "spotify_uri" column
df = df.dropna()

# Filter out rows where the "spotify_uri" column contains the string "Not found"
df = df[~df["spotify_uri"].str.contains("Not found")]

# Save the DataFrame as a pickle file named "songs.pkl"
df.to_pickle(r"./data/songs.pkl")
