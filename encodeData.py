import pandas as pd
from sklearn.preprocessing import StandardScaler

raw_data_path = "datasets/raw_data.csv"

new_encoded_path = "datasets/encoded_data.csv"

df_raw = pd.read_csv(raw_data_path, header=0)

df_raw.drop(columns=["tvdb_id", 'pg_rating', 'rating', 'rating_votecount', 'banner_url', 'season_count', 'drive_url', 'file_id'], inplace=True)

print(df_raw.keys())

def hot_encode_data(df, column_name, comma_separated=False):
    print(f"Hot encoding for column: {column_name}")
    if comma_separated:
        df[column_name] = df[column_name].apply(lambda x: x.split(","))
    genres_df = df[column_name].explode().str.get_dummies().groupby(level=0).sum()

    df_encoded = pd.concat([df, genres_df], axis=1)
    df_encoded.drop(column_name, axis=1, inplace=True)
    print(f"Finished hot encoding for column: {column_name}")
    return df_encoded

print("--- START ENCODING PROCESS ---\n")
# Convert categorical features to numerical representations
# Features include: item_type, genres, actors
df_preprocess_1 = hot_encode_data(df_raw, 'genres', True)
df_preprocess_2 = hot_encode_data(df_preprocess_1, 'actors', True)
df_encoded = hot_encode_data(df_preprocess_2, 'item_type')


# Standardize numerical features
scaler = StandardScaler()
df_encoded[['year', 'runtime']] = scaler.fit_transform(df_encoded[['year', 'runtime']])
print("\n--- ENCODING PROCESS FINISHED ---")



df_encoded.to_csv(new_encoded_path, index=False)
