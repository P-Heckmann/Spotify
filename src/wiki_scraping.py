import pandas as pd

# Define a list to store the URLs of Wikipedia pages
urls = []
for year in range(1958, 2023):
    urls.append(
        f"https://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_top-ten_singles_in_{year}"
    )

# Create an empty list to store rows of data
rows = []
for url, year in zip(urls, range(1958, 2023)):
    print(year)
    
    # Read HTML tables from the Wikipedia page
    dfs = pd.read_html(url)

    # Find the table with the maximum number of rows
    row_num = []
    for df in dfs:
        row_num.append(df.shape[0])

    year_df = dfs[row_num.index(max(row_num))]
    year_df = year_df.iloc[:, :6]

    # Rename the columns of the selected table
    columns = ["entry_date", "title", "artist", "peak", "peak_date", "weeks_top_ten"]
    year_df.columns = columns

    # Filter out rows where the "peak" column cannot be converted to numeric values
    year_df = year_df[
        ~pd.to_numeric(year_df["peak"], errors="coerce").isna()
    ].reset_index(drop=True)

    # Add a new column for the year
    year_df["year"] = year
    
    # Append the rows of the selected table to the list
    rows.extend(year_df.to_dict(orient="records"))

# Create a DataFrame from the list of rows
df = pd.DataFrame(rows)

# Define a list of characters to be replaced in the "title" column
to_replace = ["/", "\\\\", "(", ")", "'", ":", "."]

# Replace characters in the "title" column
for item in to_replace:
    df["title"] = df["title"].str.replace(item, "", regex=False)

# Save the DataFrame as a pickle file named "hot_100.pkl"
df.to_pickle(r"./data/hot_100.pkl")

