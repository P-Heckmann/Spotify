import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up the client credentials
client_credentials_manager = SpotifyClientCredentials(
    client_id="54b3ffcb9b85494aa3ca79a540013c94",
    client_secret="68d913a2f09f4086ab7ab1244816d99b",
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


df = pd.read_pickle("./data/songs.pkl")


# Define a function to get audio features for a list of track URIs
def get_audio_features(uris):
    features_list = []
    for uri in uris:
        features = sp.audio_features(uri)
        features_list.append(features[0])
    return features_list


# Define a DataFrame with track URIs
df = pd.read_pickle("./data/songs.pkl")

# Call the function to get audio features for the tracks
audio_features = get_audio_features(df["spotify_uri"].tolist())

# filter out invalid entry
data = [i for i in audio_features if i is not None]

# Convert the list of audio features into a DataFrame
audio_features_df = pd.DataFrame(data)

audio_features_df = audio_features_df.rename(columns={"uri": "spotify_uri"})

# Merge the original DataFrame with the audio features DataFrame
merged_df = pd.merge(df, audio_features_df, on="spotify_uri", how="left")

merged_df.to_pickle("./data/merged_df.pkl")

