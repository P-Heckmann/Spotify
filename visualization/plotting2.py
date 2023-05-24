import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle('data\merged_df.pkl')

df = df.dropna()


df['year'] = df['year'].astype(int)

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['year'], format='%Y')


# Group the data by year and calculate the sum of the 'value' column for each group
grouped_by_year = df[df['date'].dt.year == 2011]

# Count how often each year appears in the 'date' column
count_by_year = df['date'].dt.year.value_counts()#.reset_index()

#number = count_by_year.loc[count_by_year['index']== 2022]

count_by_year.plot.bar(figsize=(15,5))


df['key'].unique()

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


# Create a stacked bar chart using the pivoted DataFrame
pivoted.plot(kind='bar', stacked=True, figsize=(15,6))

plt.ylabel('Count')
plt.xlabel('')
# Move the legend outside the figure
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# normalize for each year!

counts

# group the dataframe by year and normalize the count column
counts['normalized_count'] = counts.groupby('year')['Count'].apply(lambda x: x / x.sum())


pivoted_normalized = counts.pivot(index='year', columns='key', values='normalized_count')


# Create a stacked bar chart using the pivoted DataFrame
pivoted_normalized.plot(kind='bar', stacked=True, figsize=(15,6))

plt.ylabel('Count')
plt.xlabel('')
# Move the legend outside the figure
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')