import pandas as pd

raw_data_path = 'datasets/raw_data.csv'

df = pd.read_csv(raw_data_path, header=0)

imdb_ids = []

for _, row in df.iterrows():
    imdb_id = row['imdb_id']
    if len(imdb_id) == 8:
        imdb_id = imdb_id.replace('tt', 'tt0')
    imdb_ids.append(imdb_id)

df['imdb_id'] = imdb_ids

df.to_csv(raw_data_path, index=False)

'''
--- REMOVE EXCLUDED GENRES FROM THE DATASET ---
raw_data_path = 'datasets/raw_data.csv'

df = pd.read_csv(raw_data_path, header=0)

genres_to_remove = ['War', 'Sport', 'History', 'Documentary', 'Musical', 'Game-Show', 'Short', 'News', 'Reality-TV', 'Western', 'Talk-Show', 'Biography', 'Music', 'Family']

df['genres'] = df['genres'].apply(
    lambda x: ','.join([genre for genre in x.split(',') if genre not in genres_to_remove])
)

print(df[df['imdb_id'] == 'tt993846']['genres'])

df.to_csv(raw_data_path, index=False)
'''

'''
--- FORMAT THE FILE IDS AND ADD THEM TO THE DATASET ---
raw_data_path = 'formattedDriveURLs.csv'

df = pd.read_csv(raw_data_path, header=0)

file_ids = []
for _, row in df.iterrows():
    illegal_phrases = ['https://drive.google.com/file/d/', '/view?usp=drive_link']
    file_id = row['shareURL']
    for phrase in illegal_phrases:
        file_id = file_id.replace(phrase, "")
    file_ids.append(file_id)

df['fileID'] = file_ids

print(df.head())

df.to_csv(raw_data_path, index=False)
'''

'''
--- CREATE WORKSHEETS TO MANUALLY PUT BANNER_URLS INTO IN GOOGLE SHEETS ---
old_path_movies = "dataset_documentation/9_top100_movies.csv"
old_path_series = "dataset_documentation/9_top100_series.csv"
new_path_movies = "dataset_documentation/10_top100_movies_worksheet.csv"
new_path_series = "dataset_documentation/10_top100_series_worksheet.csv"

df_movies = pd.read_csv(old_path_movies, header=0)
df_series = pd.read_csv(old_path_series, header=0)

df_movies = df_movies[[col for col in df_movies.columns if col != 'banner_url'] + ['banner_url']]
df_movies['banner_url'] = ''

df_series = df_series[[col for col in df_series.columns if col != 'banner_url'] + ['banner_url']]
df_series['banner_url'] = ''

df_movies.to_csv(new_path_movies, index=False)
df_series.to_csv(new_path_series, index=False)
'''

'''
--- REMOVE ALL ITEMS THAT ARE ALREADY IN THE DATASET ---
- No items were duplicates

old_path_movies = "dataset_documentation/9_top100_movies.csv"
old_path_series = "dataset_documentation/9_top100_series.csv"
current_dataset_path = "datasets/raw_data.csv"

df_current = pd.read_csv(current_dataset_path, header=0)
df_movies = pd.read_csv(old_path_movies, header=0)
df_series = pd.read_csv(old_path_series, header=0)

df_movies = df_movies[~df_movies['imdb_id'].isin(df_current['imdb_id'])]
df_series= df_movies[~df_series['imdb_id'].isin(df_current['imdb_id'])]

print(f"Amount of rows remaining for movies: {len(df_movies)}")
print(f"Amount of rows remaining for series: {len(df_series)}")
'''

'''
--- GET TOP 100 ITEMS PER ITEM_TYPE ---
old_path = "dataset_documentation/8_dataset_all_data.csv"
df_old = pd.read_csv(old_path, header=0)

df_filtered = df_old[(df_old['banner_url'].str.contains('clearlogo', case=False, na=False)) | (df_old['banner_url'] == 'UNAVAILABLE')]
df_filtered = df_filtered.sort_values(by='rating_votecount', ascending=False)

df_movies = df_filtered[df_filtered['item_type'] == 'movie'].head(100)
df_series = df_filtered[df_filtered['item_type'] == 'series'].head(100)

print(f"Amount of rows remaining for movies: {len(df_movies)}")
print(f"Amount of rows remaining for series: {len(df_series)}")

df_movies.to_csv(new_path_movies, index=False)
df_series.to_csv(new_path_series, index=False)
'''