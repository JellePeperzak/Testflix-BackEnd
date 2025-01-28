# Properties to consider: item_type, year, genres, runtime, actors, rating, rating_votecount
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from itertools import zip_longest

# FUNCTION THAT GENERATES THE TOP-18 ITEMS FOR EVERY PROVIDED COMBINATION
def generate_carousel_items_cosine(combinations, df_raw, df_items):
    df_items = df_items.sort_values(by='score', ascending=False)

    # FUNCTION THAT GETS THE TOP N ITEMS FOR A COMBINATION AND RETURNS THEM AS A DATAFRAME
    def get_top_items(df, item_type, genre, exclude_ids, top_n=18):
        filtered = df[
            (df['item_type'] == item_type) &
            (df['genres'].str.contains(genre, case=False, na=False)) &
            (~df['imdb_id'].isin(exclude_ids))
        ]
        return filtered.head(top_n)
    
    # GO OVER EVERY PROVIDED COMBINATION AND GENERATE APPROPRIATE ITEM- AND CAROUSEL OBJECTS FOR THEM
    carousel_objects = []
    suggested_item_ids = set()

    for combination in combinations:
        item_type, genre = combination['item_type'], combination['genre']
        top_items = get_top_items(df_items, item_type, genre, suggested_item_ids, top_n=18)

        top_6_ids = top_items['imdb_id'].head(6).tolist()
        top_18_ids = top_items['imdb_id'].head(18).tolist()
        suggested_item_ids.update(top_6_ids)

        # ITERATE OVER THE LIST OF 18 IMDB_IDS TO GENERATE A LIST FOR THE CAROUSEL OBJECT
        carousel_items = []
        for imdb_id in top_18_ids:
            item = df_raw[df_raw['imdb_id'] == imdb_id].iloc[0]
            carousel_items.append({
                'imdb_id': str(item['imdb_id']),
                'tvdb_id': str(item['tvdb_id']),
                'item_type': item['item_type'],
                'title': item['title'],
                'year': str(item['year']),
                'genres': item['genres'],
                'runtime': str(item['runtime']),
                'actors': item['actors'],
                'pg_rating': item['pg_rating'],
                'season_count': str(item['season_count'])
            })

        # APPEND THE FULL CAROUSEL OBJECT TO THE LIST OF CAROUSEL OBJECTS
        carousel_objects.append({
            'item_type': item_type,
            'genre': genre,
            'items': carousel_items
        })

    return carousel_objects

# FUNCTION THAT GENERATES A LIST THAT CONTAINS OBJECTS REPRESENTING EACH INDIVIDUAL ITEM, ORDERED DESCENDINGLY BY SIMILARITY SCORE.
def generate_similarity_database_cosine(liked_items, df_raw, df_encoded):
    # EXTRACTING THE FEATURE COLUMNS (EXCLUDING IMDB_ID AND TITLE, WHICH ARE AT INDEX 0 AND 1, RESPECTIVELY)
    # AND USING IT TO CREATE A FEATURE MATRIX
    feature_columns = df_encoded.columns[2:]
    feature_matrix = csr_matrix(df_encoded[feature_columns].values)

    # GENERATE INDIVIDUAL ITEM SCORES BASED ON COSINE SIMILARITY TO LIKED FEATURES
    liked_items_features = feature_matrix[np.isin(df_encoded['imdb_id'], liked_items)]
    similarity_matrix = cosine_similarity(liked_items_features, feature_matrix)
    item_scores = np.sum(similarity_matrix, axis=0)

    # STORE SCORES IN A DATAFRAME AND SORT DESCENDINGLY BASED ON VALUE, THEN TAKE OUT ITEMS THAT THE USER ALREADY LIKED
    df_item_scores = pd.DataFrame({
        'imdb_id': df_encoded['imdb_id'],
        'score': item_scores
    }).sort_values(by='score', ascending=False)
    df_items = df_item_scores[~df_item_scores['imdb_id'].isin(liked_items)]

    # PRECOMPUTE DICTIONARIES FOR FAST LOOKUPS
    raw_data_dict = df_raw.set_index('imdb_id').to_dict('index')
    scores_dict = df_items.set_index('imdb_id')['score'].to_dict()

    # GENERATE ITEM OBJECT FOR EVERY IMDB_ID
    item_object_list = [
        {
            'imdb_id': str(imdb_id),
            'tvdb_id': str(raw_data_dict[imdb_id]['tvdb_id']),
            'item_type': raw_data_dict[imdb_id]['item_type'],
            'title': raw_data_dict[imdb_id]['title'],
            'year': str(raw_data_dict[imdb_id]['year']),
            'genres': raw_data_dict[imdb_id]['genres'],
            'runtime': str(raw_data_dict[imdb_id]['runtime']),
            'actors': raw_data_dict[imdb_id]['actors'],
            'pg_rating': raw_data_dict[imdb_id]['pg_rating'],
            'season_count': str(raw_data_dict[imdb_id]['season_count']),
            'score': float(scores_dict[imdb_id])
        }
        for imdb_id in df_items['imdb_id']
    ]

    return item_object_list

# FUNCTION THAT GENERATES AN OBJECT CONTAINING DATA FOR ALL CAROUSEL TYPES
def generate_carousel_data_cosine(preference_ids, df_raw, df_encoded): 
    default_weight = 1.0
    genre_weight = 1.2  # 1.2 seemed to be the first weight value where no genres unrelated to preference items were in the top-5 for either movies or series
    feature_weights = {
        'Action': genre_weight,
        'Adventure': genre_weight,
        'Animation': genre_weight,
        'Comedy': genre_weight,
        'Crime': genre_weight,
        'Drama': genre_weight,
        'Fantasy': genre_weight,
        'Horror': genre_weight,
        'Mystery': genre_weight,
        'Romance': genre_weight,
        'Sci-Fi': genre_weight,
        'Thriller': genre_weight
    }

    # Generate individual item scores based on cosine similarity
    feature_columns = df_encoded.columns[2:]
    weighted_features = [
        feature_weights.get(feature, default_weight)  # If feature not found, use default_weight
        for feature in feature_columns
    ]

    weighted_feature_matrix = df_encoded[feature_columns].multiply(weighted_features, axis=1).values
    features_liked_items = weighted_feature_matrix[np.isin(df_encoded['imdb_id'], preference_ids)]
    similarity_matrix = cosine_similarity(features_liked_items, weighted_feature_matrix)
    item_scores = similarity_matrix.sum(axis=0)

    # Create a dataframe that shows the score for every item, and exclude preferred items
    df_item_scores = pd.DataFrame({
        'imdb_id': df_encoded['imdb_id'], 
        'title': df_encoded['title'],
        'item_type': df_raw['item_type'], 
        'genres': df_raw['genres'], 
        'score': item_scores
    })
    df_items = df_item_scores[~df_item_scores['imdb_id'].isin(preference_ids)]

    print(len(df_items))

    combination_rows = []

    # Prepare combinations
    for index, row in df_items.iterrows():
        item_type = row['item_type']
        genres = row['genres'].split(",")

        for genre in genres:
            combination_rows.append({
                'imdb_id': row['imdb_id'],
                'item_type': item_type,
                'genre': genre.strip(),
                'score': row['score']
            })
    df_combinations = pd.DataFrame(combination_rows)

    df_combinations = df_combinations.groupby(['item_type', 'genre']).agg(
        avg_score=('score', 'mean')
    ).reset_index()

    recommended_combinations = df_combinations.sort_values(by='avg_score', ascending=False)

    df_movies = recommended_combinations[recommended_combinations['item_type'] == 'movie'].head(6)
    df_series = recommended_combinations[recommended_combinations['item_type'] == 'series'].head(6)

    # Ensure that the home-page carousels alternate between movies and series (due to this not being personalized)
    interleaved_rows = []
    for movie, series in zip_longest(df_movies.iterrows(), df_series.iterrows()):
        if movie is not None:
            interleaved_rows.append(movie[1])  # movie[1] contains the row data
        if series is not None:
            interleaved_rows.append(series[1])  # serie[1] contains the row data

    df_all = pd.DataFrame(interleaved_rows).reset_index(drop=True).head(6)

    # FUNCTION TO GENERATE THE LIST OF ITEMS FOR EVERY COMBINATION PROVIDED IN THE combinations_df VARIABLE
    def generate_carousel_objects(combinations_df, df_raw, df_scores):
        combinations = []
        # GENERATE LIST OF COMBINATIONS TO FEED TO THE generate_carousel_items FUNCTION
        for _, row in combinations_df.iterrows():
            item_type = row['item_type']
            genre = row['genre']
            combinations.append({
                'item_type': item_type,
                'genre': genre
            })
        
        carousel_objects = generate_carousel_items_cosine(combinations, df_raw, df_scores)
        return carousel_objects

    # GENERATE CAROUSEL OBJECTS FOR MOVIES, SERIES, AND BOTH (ALL)
    carousel_objects_all = generate_carousel_objects(df_all, df_raw, df_items)
    carousel_objects_movies = generate_carousel_objects(df_movies, df_raw, df_items)
    carousel_objects_series = generate_carousel_objects(df_series, df_raw, df_items)

    return {
         'home_carousels': carousel_objects_all,
         'movie_carousels': carousel_objects_movies,
         'series_carousels': carousel_objects_series
    }