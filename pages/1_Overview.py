import streamlit as st
import pandas as pd
import altair as alt




path = "./data/merged_df.pkl"

path_local = r"C:\Users\paulh\Desktop\Spotify\data\merged_df.pkl"

df = pd.read_pickle(path_local)



#NUMBER_OF_ENTRIES = len(df)

#df.describe()

st.write("### Welcome to the Billboard analyser")
st.markdown("""---""")

NUMBER_OF_ENTRIES = len(df)


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




for metric, name in zip(metrics,metrics_name) :
    st.write(f"#### {name}")
    
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

    

