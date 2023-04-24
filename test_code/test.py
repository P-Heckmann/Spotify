import pandas as pd

# df = pd.read_pickle('.\data\hot_100.pkl')

# df = df.loc[df['artist']== 'Genesis']

df = pd.read_pickle("./data/songs.pkl")


to_replace = ["[", "]", "*"]
for item in to_replace:
    df["weeks_top_ten"] = df["weeks_top_ten"].str.replace(item, "", regex=False)

# convert the 'weeks_top_ten' column to integers
df["weeks_top_ten"] = df["weeks_top_ten"].astype(int)

# sort by salary in descending order
df_sorted = df.sort_values(by="weeks_top_ten", ascending=False)
