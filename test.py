import pandas as pd

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

print(len(unique_genres))

'''import pandas as pd

data_path = "data_7feb.csv"

df = pd.read_csv(data_path, header=0)

df_unique = df['condition_id'].unique()

numbers = []
for i in range(36):
    numbers.append(i)

print(numbers)

print(len(df_unique))

missing_conditions = [c for c in numbers if c not in df_unique]

print(missing_conditions)
'''