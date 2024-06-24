import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


path = "./data/merged_df.pkl"

path_local = r"C:\Users\paulh\Desktop\Spotify\data\merged_df.pkl"

df = pd.read_pickle(path_local)

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


# Group the DataFrame by 'Name' and 'Year' and count the occurrences
counts = df.groupby(['key', 'year']).size().reset_index(name='Count')

# Pivot the counts DataFrame to have names as columns and years as index
pivoted = counts.pivot(index='year', columns='key', values='Count')



#chart = alt.Chart(pivoted).mark_bar().encode(
#    alt.X('year:O', bin=alt.Bin(step=1), title='Year'),
#    alt.Y('count()', title='Frequency')
#).interactive()

#st.altair_chart(chart, use_container_width=True)


# Create a stacked bar chart using the pivoted DataFrame
fig, pivoted = plt.subplots()
pivoted.plot(kind='bar', stacked=True, figsize=(15,6))

plt.ylabel('Count')
plt.xlabel('')
# Move the legend outside the figure
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

st.pyplot(fig)


# group the dataframe by year and normalize the count column
counts['normalized_count'] = counts.groupby('year')['Count'].apply(lambda x: x / x.sum())

# Pivot the counts DataFrame to have names as columns and years as index
pivoted_normalized = counts.pivot(index='year', columns='key', values='normalized_count')

# Create a stacked bar chart using the pivoted DataFrame
pivoted_normalized.plot(kind='bar', stacked=True, figsize=(15,6))

plt.ylabel('Count')
plt.xlabel('')
# Move the legend outside the figure
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')