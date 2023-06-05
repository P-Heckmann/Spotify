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

metrics = [
    "Key",
    "Tempo",
    "Danceability",
"Speechiness","Instrumentalness", "Liveness","Valence"]

selected_metric = st.radio("Select a metric:", metrics)

# selectbox

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
