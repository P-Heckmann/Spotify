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

df['year'] = df['year'].astype(int)

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['year'], format='%Y')

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




# Define the bin edges
tempo_bins = [0,80,90,100,110,120,130,140,160,300]

# Define the bin labels
labels = ['0-80 BPM', '80-90 BPM',
          '90-100 BPM', '100-110 BPM', 
          '110-120 BPM ', '120-130 BPM',
          '130-140 BPM', '140-160 BPM', '160-250 BPM']


df['Tempo'] = pd.cut(df['tempo'], bins=tempo_bins, labels=labels)


metrics = ["key", "tempo" ] #, "danceability","speechiness","instrumentalness", "liveness","valence"]

selected_metric = st.selectbox('Select a metric:', metrics)


# Group the DataFrame by 'Name' and 'Year' and count the occurrences
counts = df.groupby([selected_metric, 'year']).size().reset_index(name='Count')
# Pivot the counts DataFrame to have names as columns and years as index
pivoted = counts.pivot(index='year', columns=selected_metric, values='Count')
pivoted = pivoted.reset_index(drop=False)
#df = pivoted.reset_index()
# Melt the data to long format


melted_data = pd.melt(pivoted, id_vars='year', var_name=selected_metric, value_name='Count')
melted_data = melted_data.dropna()



# Create the stacked bar plot using Altair
chart = alt.Chart(melted_data).mark_bar().encode(
    x='year:O',
    y='Count:Q',
    color=selected_metric, default="key"
).interactive()

# Specify the order of the legend

if selected_metric == "tempo":
    custom_sort_order = labels
    chart = chart.encode(
        color=alt.Color('Tempo:N', sort=custom_sort_order, legend=alt.Legend(title='Tempo')),
)

#chart


st.altair_chart(chart, use_container_width=True)

melted_data['Normalized_count'] = melted_data.groupby('year')['Count'].apply(lambda x: x / x.sum())
chart = alt.Chart(melted_data).mark_bar().encode(
    x='year:O',
    y='Normalized_count:Q',
    color=selected_metric
).interactive()

# Specify the order of the legend
#custom_sort_order = labels
#chart = chart.encode(
#    color=alt.Color('Tempo:N', sort=custom_sort_order, legend=alt.Legend(title='Tempo')),
#)


#chart



st.altair_chart(chart, use_container_width=True)
