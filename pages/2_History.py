import streamlit as st
import pandas as pd
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt


path = "./data/merged_df.pkl"

path_local = r"C:\Users\paulh\Desktop\Spotify\data\merged_df.pkl"

df = pd.read_pickle(path)

st.write("### Metrics per year")
st.markdown("""---""")

df["year"] = df["year"].astype(int)

# Convert the 'date' column to datetime
df["date"] = pd.to_datetime(df["year"], format="%Y")

# Define a dictionary to map numerical data to string data
mapping = {
    0: "C",
    1: "C♯",
    2: "D",
    3: "D♯",
    4: "E",
    5: "F",
    6: "F♯",
    7: "G",
    8: "G#",
    9: "A",
    10: "A#",
    11: "B",
}

# Replace numerical data in column 'A' with string data using the mapping dictionary
df["Key"] = df["key"].replace(mapping)


# Define the bin edges
tempo_bins = [0, 80, 90, 100, 110, 120, 130, 140, 160, 300]

# Define the bin labels
tempo_labels = [
    "0-80 BPM",
    "80-90 BPM",
    "90-100 BPM",
    "100-110 BPM",
    "110-120 BPM ",
    "120-130 BPM",
    "130-140 BPM",
    "140-160 BPM",
    "160-250 BPM",
]

other_bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

other_labels = ["0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"]


df["Tempo"] = pd.cut(df["tempo"], bins=tempo_bins, labels=tempo_labels)
df["Danceability"] = pd.cut(df["danceability"], bins=other_bins, labels=other_labels)
df["Speechiness"] = pd.cut(df["speechiness"], bins=other_bins, labels=other_labels)
df["Instrumentalness"] = pd.cut(df["instrumentalness"], bins=other_bins, labels=other_labels)
df["Liveness"] = pd.cut(df["liveness"], bins=other_bins, labels=other_labels)
df["Valence"] = pd.cut(df["valence"], bins=other_bins, labels=other_labels)

KEY = '"The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1 (Spotify API)."'

TEMPO = '"The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration (Spotify API)."'

DANCEABLITY = '"Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable (Spotify API). "'

SPEECHINESS = '"Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks (Spotify API)."'

INSTRUMENTALNESS = '"Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0 (Spotify API)."'

LIVENESS = '"Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live (Spotify API)."'

VALENCE = '"A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)(Spotify API)."'


metrics = [
    "Key",
    "Tempo",
    "Danceability",
"Speechiness","Instrumentalness", "Liveness","Valence"]

selected_metric = st.radio("Select a metric:", metrics)



# Group the DataFrame by 'Name' and 'Year' and count the occurrences
counts = df.groupby([selected_metric, "year"]).size().reset_index(name="Count")
# Pivot the counts DataFrame to have names as columns and years as index
pivoted = counts.pivot(index="year", columns=selected_metric, values="Count")
pivoted = pivoted.reset_index(drop=False)
# df = pivoted.reset_index()
# Melt the data to long format


melted_data = pd.melt(
    pivoted, id_vars="year", var_name=selected_metric, value_name="Count"
)
melted_data = melted_data.dropna()



if selected_metric == "Key":
    st.write("#### Key")
    st.write(f"###### {KEY}")
elif selected_metric == "Tempo":
    st.write("#### Tempo")
    st.write(f"###### {TEMPO}")
elif selected_metric == "Danceability":
    st.write("#### Danceability")
    st.write(f"###### {DANCEABLITY}")
elif selected_metric == "Speechiness":
    st.write("#### Speechiness")
    st.write(f"###### {SPEECHINESS}")
elif selected_metric == "Instrumentalness":
    st.write("#### Instrumentalness")
    st.write(f"###### {INSTRUMENTALNESS}")
elif selected_metric == "Liveness":
    st.write("#### Liveness")
    st.write(f"###### {LIVENESS}")
elif selected_metric == "Valence":
    st.write("#### Valence")
    st.write(f"###### {VALENCE}")
    


# Create the stacked bar plot using Altair
chart = (
    alt.Chart(melted_data)
    .mark_bar()
    .encode(x=alt.X("year:O", title=""),
            y=alt.X("Count:Q"),
            color=selected_metric)
    .interactive()
)

# Specify the order of the legend

if selected_metric == "Tempo":
    custom_sort_order = tempo_labels
    chart = chart.encode(
        color=alt.Color(
            "Tempo:N", sort=custom_sort_order, legend=alt.Legend(title="Tempo")
        ),
    )


st.altair_chart(chart, use_container_width=True)
st.markdown("""---""")

melted_data["Normalized_count"] = melted_data.groupby("year")["Count"].apply(
    lambda x: x / x.sum()
)
chart = (
    alt.Chart(melted_data)
    .mark_bar()
    .encode(x=alt.X("year:O", title=""),
            y=alt.Y("Normalized_count:Q"),
            color=selected_metric)
    .interactive()
)

if selected_metric == "Tempo":
    custom_sort_order = tempo_labels
    chart = chart.encode(
        color=alt.Color(
            "Tempo:N", sort=custom_sort_order, legend=alt.Legend(title="Tempo")
        ),
    )
elif selected_metric == "Danceability":
    custom_sort_order = other_labels
    chart = chart.encode(
        color=alt.Color(
            "Danceability:N",
            sort=custom_sort_order,
            legend=alt.Legend(title="Danceability"),
        ),
    )

# chart


st.altair_chart(chart, use_container_width=True)
