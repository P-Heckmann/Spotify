import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_pickle('data\merged_df.pkl')

df = df.dropna()

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


# Count the occurrences of each category in column 'A'
counts = df['key'].value_counts()

# Plot the results as a bar chart
counts.plot.bar()

# Set the axis labels and title
plt.xlabel('Key')
plt.ylabel('Count')
plt.xticks(rotation=0)
#plt.title('Key')

# Show the plot
plt.show()


