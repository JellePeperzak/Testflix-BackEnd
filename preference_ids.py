import pandas as pd

all_data_path = "datasets/raw_data.csv"
raw_data_path = "datasets/preference_ids.csv"
new_path = "preference_ids.csv"

df = pd.read_csv(raw_data_path, header=0)
df_all = pd.read_csv(all_data_path, header=0)

df_pref_movies = df[df['item_type'] == 'movie']
df_pref_series = df[df['item_type'] == 'series']
df_all_movies = df_all[df_all['item_type'] == 'movie']
df_all_series = df_all[df_all['item_type'] == 'series']

df_all_movies_filtered = df_all_movies[df_all_movies['genres'].str.contains('Romance', case=False, na=False)]
df_all_series_filtered = df_all_series[df_all_series['genres'].str.contains('Fantasy', case=False, na=False)]
df_pref_movies_filtered = df_pref_movies[df_pref_movies['genres'].str.contains('Romance', case=False, na=False)]
df_pref_series_filtered = df_pref_series[df_pref_series['genres'].str.contains('Fantasy', case=False, na=False)]

unique_genres = set(genre.strip() for genre_list in df_pref_series['genres'].dropna() for genre in genre_list.split(','))
unique_genres_list = [genre for genre in unique_genres if len(genre) > 0]
unique_genres_list = sorted(unique_genres_list)

genre_count_list = []
for genre in unique_genres_list:
    genre_count_list.append(int(df_pref_series['genres'].str.contains(genre, case=False, na=False).sum()))

index = -1
for genre in unique_genres_list:
    index +=1
    print(f"{genre}: {genre_count_list[index]}")

df.to_json('preferences.json', orient='records', lines=True)

'''preference_ids = {
    'Action': ['tt0102034', 'tt0103359', 'tt0103584'], 
    'Adventure': ['tt0103639', 'tt0106057', 'tt0106179'], 
    'Animation': ['tt0101414', 'tt0116583', 'tt0118298'], 
    'Comedy': ['tt0103484', 'tt0105415', 'tt0105929'], 
    'Crime': ['tt0123948', 'tt0141842', 'tt0203259'], 
    'Drama': ['tt0104990', 'tt0105695', 'tt0118300'], 
    'Fantasy': ['tt0103874', 'tt0450385'], 
    'Horror': ['tt0120082', 'tt0130018', 'tt8362852'], 
    'Mystery': ['tt0114746'], 
    'Romance': ['tt0103484', 'tt0103874', 'tt0106080'], 
    'Sci-Fi': ['tt0106950', 'tt0114746', 'tt0303461'], 
    'Thriller': ['tt0111257', 'tt0117998', 'tt0306414']
}

unique_ids = set()

for ids in preference_ids.values():
    unique_ids.update(ids)

df_filtered = df[df['imdb_id'].isin(unique_ids)]'''



'''unique_genres_all = set(genre.strip() for genre_list in df_all['genres'].dropna() for genre in genre_list.split(','))
unique_genres_all_list = [genre for genre in unique_genres_all if len(genre) > 0]
unique_genres_all_list = sorted(unique_genres_all_list)

genre_count_all_list = []
for genre in unique_genres_all_list:
    genre_count_all_list.append(int(df_all['genres'].str.contains(genre, case=False, na=False).sum()))


unique_genres = set(genre.strip() for genre_list in df_movies['genres'].dropna() for genre in genre_list.split(','))
unique_genres_list = [genre for genre in unique_genres if len(genre) > 0]
unique_genres_list = sorted(unique_genres_list)

genre_count_list = []
for genre in unique_genres_list:
    genre_count_list.append(int(df_series['genres'].str.contains(genre, case=False, na=False).sum()))

index = -1
for genre in unique_genres_list:
    index +=1
    print(f"{genre}: {genre_count_list[index]}")

missing_genres = list(set(unique_genres_all_list) ^ set(unique_genres_list))

print(missing_genres)'''

'''
raw_data_path = "datasets/raw_data.csv"
new_path = "datasets/raw_data.csv"
genres_to_remove = ['Biography', 'Music', 'Family']
regex_genre = r'\b'


df = pd.read_csv(raw_data_path, header=0)

unique_genres = set(genre.strip() for genre_list in df['genres'].dropna() for genre in genre_list.split(','))
unique_genres_list = [genre for genre in unique_genres if len(genre) > 0]
unique_genres_list = sorted(unique_genres_list)

def get_items(df):
    result = []
    item_types = []
    if len(df.index) > 0:
        result.append(df['imdb_id'].iloc[0])
        item_types.append(df['item_type'].iloc[0])
    if len(df.index) > 1:
        result.append(df['imdb_id'].iloc[1])
        item_types.append(df['item_type'].iloc[1])
    if len(df.index) > 2:
        if item_types[0] == item_types[1]:
            if item_types[0] == 'movie':
                df = df[df['item_type'] == 'series']
                if len(df.index) > 0:
                    result.append(df['imdb_id'].iloc[0])
                    item_types.append(df['item_type'].iloc[0])
            else:
                df = df[df['item_type'] == 'movie']
                if len(df.index) > 0:
                    result.append(df['imdb_id'].iloc[0])
                    item_types.append(df['item_type'].iloc[0])
        else:
            result.append(df['imdb_id'].iloc[2])
            item_types.append(df['item_type'].iloc[2])
    return result
    
genres_forbidden = []
preference_ids = {}
df_placeholder = df.copy()

for genre in unique_genres_list:
    if len(genres_forbidden) > 0:
        pattern = '|'.join(genres_forbidden)
        df_filtered = df[(~df['genres'].str.contains(pattern, case=False, na=False)) & (df['genres'].str.contains(genre, case=False, na=False))]
        if len(df_filtered.index) == 0:
            genres_forbidden = []
    if len(genres_forbidden) == 0:
        df_filtered = df[df['genres'].str.contains(genre, case=False, na=False)]
    
    print(f'Genre: {genre}, Dataframe size: {len(df_filtered.index)}')

    df_filtered = df_filtered.reset_index()

    item_ids = get_items(df_filtered)
    preference_ids[genre] = item_ids
    genres_forbidden.append(genre)

print(preference_ids)
'''