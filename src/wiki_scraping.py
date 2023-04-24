import pandas as pd
import numpy as np

urls = []
for year in range(1958, 2023):
    urls.append(
        f"https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_top-ten_singles_in_{year}"
    )

rows = []
for url, year in zip(urls, range(1958, 2023)):
    print(year)
    dfs = pd.read_html(url)

    row_num = []
    for df in dfs:
        row_num.append(df.shape[0])

    year_df = dfs[row_num.index(max(row_num))]
    year_df = year_df.iloc[:, :6]

    columns = ["entry_date", "title", "artist", "peak", "peak_date", "weeks_top_ten"]
    year_df.columns = columns

    year_df = year_df[
        ~pd.to_numeric(year_df["peak"], errors="coerce").isna()
    ].reset_index(drop=True)
    year_df["year"] = year
    rows.extend(year_df.to_dict(orient="records"))

df = pd.DataFrame(rows)

to_replace = ["/", "\\\\", "(", ")", "'", ":", "."]

for item in to_replace:
    df["title"] = df["title"].str.replace(item, "", regex=False)


df.to_pickle(r"C:\Users\paulh\Desktop\Data Science Projects\data\hot_100.pkl")
