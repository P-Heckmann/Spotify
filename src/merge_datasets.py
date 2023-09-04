import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up the client credentials for Spotify API authentication
client_credentials_manager = SpotifyClientCredentials(
    client_id="...",
    client_secret="...",
)

# Create a Spotify API client
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Read the DataFrame from a pickle file
df = pd.read_pickle("./data/songs.pkl")

# Define a function to get audio features for a list of track URIs
def get_audio_features(uris):
    features_list = []
    for uri in uris:
        # Get the audio features for each track URI
        features = sp.audio_features(uri)
        features_list.append(features[0])
    return features_list

# Call the get_audio_features function to retrieve audio features for the track URIs in the DataFrame
audio_features = get_audio_features(df["spotify_uri"].tolist())

# Filter out any invalid entries from the audio features list
data = [i for i in audio_features if i is not None]

# Convert the list of audio features into a DataFrame
audio_features_df = pd.DataFrame(data)

# Rename the "uri" column to "spotify_uri"
audio_features_df = audio_features_df.rename(columns={"uri": "spotify_uri"})

# Merge the original DataFrame with the audio features DataFrame based on the "spotify_uri" column
merged_df = pd.merge(df, audio_features_df, on="spotify_uri", how="left")

# Drop any rows with missing values
merged_df = merged_df.dropna()

# Save the merged DataFrame as a pickle file named "merged_df.pkl"
merged_df.to_pickle(r"./data/merged_df.pkl")

