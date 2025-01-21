import pandas as pd

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


#df_raw.to_csv(new_path, index=False)