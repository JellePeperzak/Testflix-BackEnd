import pandas as pd

raw_data_path = 'datasets/raw_data.csv'
preference_data_path = 'datasets/preference_ids.csv'

df_raw = pd.read_csv(raw_data_path, header=0)
df_pref = pd.read_csv(preference_data_path, header=0)

df_pref.to_json('preferences.json', orient='records', lines=False)

'''
--- GENERATE PREFERENCE ITEMS BASED ON CRITERIA ---
raw_data_path = 'datasets/raw_data.csv'
preference_data_path = 'datasets/preference_ids.csv'

df = pd.read_csv(raw_data_path, header=0)

# Generate a list of all unique genres
unique_genres = []
for _, row in df.iterrows():
    genre_list = row['genres'].split(',')
    for genre in genre_list:
        if not genre in unique_genres:
            unique_genres.append(genre)

# Filter the dataframe to only include items that have three genres
df_three = df[df['genres'].str.count(',') == 2]

# Sort the dataframe descendingly based on rating_votecount (popularity)
df_three_sorted = df_three.sort_values(by='rating_votecount', ascending=False)

genre_counts = {}
for genre in unique_genres:
    genre_counts[genre] = {
        'movie': 0,
        'series': 0
    }
quota_achieved = False

preference_item_ids = []
# Iterate over the rows of the sorted dataframe until there are enough items stored to cover every genre at least twice for movie and series
for _, row in df_three_sorted.iterrows():
    genre_list = row['genres'].split(',')
    item_type = row['item_type']
    overflown = False
    if 'Drama' in genre_list and genre_counts['Drama'][item_type] > 6:
        print(f"{genre} has a count of {genre_counts[genre][item_type]} for {item_type}")
        overflown = True
    if overflown == False:
        for genre in genre_list:
            if overflown == True:
                print("overflown is true")
            if genre_counts[genre][item_type] < 2 or quota_achieved == True:
                preference_item_ids.append(row['imdb_id'])
                for genre in genre_list:
                    genre_counts[genre][item_type] += 1
                break
            else:
                pass
    # Based on testing, the criterium of every genre-item_type combination being represented by at least two 
    # items is achieved once the 30th item is added to the list. If quota_achieved is not set to True, the list
    # will remain at 30 items because there will be no more eligible items due to the 'genre_counts[genre][item_type] < 2' constraint
    if len(preference_item_ids) == 30:
        quota_achieved = True
    if len(preference_item_ids) == 36:
        break

df_preference = df[df['imdb_id'].isin(preference_item_ids)]

print(genre_counts)
print(preference_item_ids)
print(len(preference_item_ids))

print(df_preference.head())
print(len(df_preference))

df_preference.to_csv(preference_data_path, index=False)
'''