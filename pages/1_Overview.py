import streamlit as st
import pandas as pd
import altair as alt




path = "./data/merged_df.pkl"

path_local = r"C:\Users\paulh\Desktop\Spotify\data\merged_df.pkl"

df = pd.read_pickle(path)




st.write("### Welcome to the Billboard analyser")
st.markdown("""---""")

NUMBER_OF_ENTRIES = len(df)
FIRST_YEAR = df["year"].min()
LAST_YEAR = 2021

DANCEABLITY = '"Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable (Spotify API). "'

SPEECHINESS = '"Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks (Spotify API)."'

INSTRUMENTALNESS = '"Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0 (Spotify API)."'

LIVENESS = '"Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live (Spotify API)."'

VALENCE = '"A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)(Spotify API)."'





st.write(f"#### Number of songs: {NUMBER_OF_ENTRIES}")
st.write(f"#### From {FIRST_YEAR} to {LAST_YEAR}")
st.markdown("""---""") 

chart = alt.Chart(df).mark_bar().encode(
    alt.X('year:O', bin=alt.Bin(step=1), title='Year'),
    alt.Y('count()', title='Frequency')
).interactive()

st.altair_chart(chart, use_container_width=True)

# Define a dictionary to map numerical data to string data
mapping = {0: 'C',
           1: 'C♯',
           2: 'D',
           3: 'D♯',
           4: 'E',
           5: 'F',
           6: 'F♯',
           7: 'G',
           8: 'G#',
           9: 'A',
           10: 'A#',
           11: 'B',
           }

# Replace numerical data in column 'A' with string data using the mapping dictionary
df['key'] = df['key'].replace(mapping)

df['duration_m'] = df['duration_ms'] / 60000

df['time_signature'] = df['time_signature'].astype(int)

st.markdown("""---""")
st.write(f"#### Key")

chart = alt.Chart(df).mark_bar().encode(
    alt.X('key:O', title='Key'),
    alt.Y('count()', title='Frequency')
).interactive()

st.altair_chart(chart, use_container_width=True)


st.markdown("""---""")
st.write(f"#### Tempo")

x_range = (50,220)
chart = alt.Chart(df).mark_bar().encode(
    alt.X('tempo',bin=alt.Bin(step=10),scale=alt.Scale(domain=x_range),  title='Beats per minute'),
    alt.Y('count()', title='Frequency')
).interactive()


st.altair_chart(chart, use_container_width=True)



metrics = ["danceability","speechiness","instrumentalness",
           "liveness","valence"]

metrics_name = ["Danceability","Speechiness","Instrumentalness",
           "Liveness","Valence"]

info_list = [DANCEABLITY,SPEECHINESS, INSTRUMENTALNESS, LIVENESS, VALENCE]


for metric, name, info in zip(metrics,metrics_name,info_list):
    st.write(f"#### {name}")
    st.write(f"###### {info}")
    
    chart = alt.Chart(df).mark_bar().encode(
    alt.X(metric,bin=alt.Bin(step=0.10), title=name),
    alt.Y('count()', title='Frequency')
    ).interactive()
    st.altair_chart(chart, use_container_width=True)
    

st.markdown("""---""")
st.write(f"#### Duration in minutes")

x_range2 = (1,8)

chart = alt.Chart(df).mark_bar().encode(
    alt.X('duration_m', bin=alt.Bin(step=1),scale=alt.Scale(domain=x_range2), title='Minutes'),
    alt.Y('count()', title='Frequency')
).interactive()
st.altair_chart(chart, use_container_width=True)

    

