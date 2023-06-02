import streamlit as st
import pandas as pd
import altair as alt


st.write("# Welcome to the Billboard analyser")

path = "./data/merged_df.pkl"

path_local = r"C:\Users\paulh\Desktop\Spotify\data\merged_df.pkl"

df = pd.read_pickle(path_local)



#NUMBER_OF_ENTRIES = len(df)

#df.describe()

chart = alt.Chart(df).mark_bar().encode(
    alt.X('year:O', bin=alt.Bin(step=1), title='Year'),
    alt.Y('count()', title='Frequency')
).properties(
    title='Songs per year'
)
chart

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

st.markdown("""---""")
st.write(f"#### Key")

chart = alt.Chart(df).mark_bar().encode(
    alt.X('key:O', title='Key'),
    alt.Y('count()', title='Frequency')
).interactive()
chart
st.altair_chart(chart, use_container_width=True)


st.markdown("""---""")
st.write(f"#### Tempo")

x_range = (50,220)
chart = alt.Chart(df).mark_bar().encode(
    alt.X('tempo',bin=alt.Bin(step=10),scale=alt.Scale(domain=x_range),  title='tempo (bpm)'),
    alt.Y('count()', title='Frequency')
).interactive()

chart
st.altair_chart(chart, use_container_width=True)

metrics = ["danceability","speechiness","instrumentalness",
           "liveness","valence","duration_m","time_signature"
           ]

for metric in metrics():
    st.markdown("""---""")
    st.write(f"#### {metric}")

    chart = alt.Chart(df).mark_bar().encode(
        alt.X(metric, bin=alt.Bin(step=0.1),  title='tempo (bpm)'),
        alt.Y('count()', title='Frequency')
    ).interactive()
    chart
    st.altair_chart(chart, use_container_width=True)



