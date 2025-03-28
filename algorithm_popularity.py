# Properties to consider: item_type, year, genres, runtime, actors, rating, rating_votecount
import pandas as pd
from itertools import zip_longest

# FUNCTION THAT GENERATES THE TOP-18 ITEMS FOR EVERY PROVIDED COMBINATION
def generate_carousel_items_popularity(combinations, df_raw):
    def generate_popularity_scores(df_raw):
        min_score = df_raw['rating_votecount'].min()
        max_score = df_raw['rating_votecount'].max()
        popularity_scores = []
        for _ ,row in df_raw.iterrows():
            lower_bound = 1
            upper_bound = 10

            normalized_score = lower_bound + ((row['rating_votecount'] - min_score) * (upper_bound - lower_bound)) / (max_score - min_score)
            popularity_score = (row['rating'] + normalized_score) / 2
            popularity_scores.append(popularity_score)
        return popularity_scores

    popularity_scores = generate_popularity_scores(df_raw)
    # STORE INDIVIDUAL ITEM SCORES IN A DATAFRAME, SORT THEM DESCENDINGLY AND REMOVE ITEMS THAT THE USER ALREADY LIKED
    df_item_scores = pd.DataFrame({'imdb_id': df_raw['imdb_id'], 'title': df_raw['title'], 'item_type': df_raw['item_type'], 'genres': df_raw['genres'], 'score': popularity_scores})
    df_items = df_item_scores.sort_values(by='score', ascending=False)

    # FUNCTION THAT GETS THE TOP N ITEMS FOR A COMBINATION AND RETURNS THEM AS A DATAFRAME
    def get_top_items(df, item_type, genre, excluded_ids, top_n=18):
        filtered = df[
            (df['item_type'] == item_type) &
            (df['genres'].str.contains(genre, case=False, na=False)) &
            (~df['imdb_id'].isin(excluded_ids))
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
                'season_count': str(item['season_count']),
            })

        # APPEND THE FULL CAROUSEL OBJECT TO THE LIST OF CAROUSEL OBJECTS
        carousel_objects.append({
            'item_type': item_type,
            'genre': genre,
            'items': carousel_items
        })

    return carousel_objects

# FUNCTION THAT GENERATES A LIST THAT CONTAINS OBJECTS REPRESENTING EACH INDIVIDUAL ITEM, ORDERED DESCENDINGLY BY SIMILARITY SCORE.
def generate_similarity_database_popularity(df_raw):
    def generate_popularity_scores(df_raw):
        min_score = df_raw['rating_votecount'].min()
        max_score = df_raw['rating_votecount'].max()
        popularity_scores = []
        for _ ,row in df_raw.iterrows():
            lower_bound = 1
            upper_bound = 10

            normalized_score = lower_bound + ((row['rating_votecount'] - min_score) * (upper_bound - lower_bound)) / (max_score - min_score)
            popularity_score = (row['rating'] + normalized_score) / 2
            popularity_scores.append(popularity_score)
        return popularity_scores
    
    item_scores = generate_popularity_scores(df_raw)

    # STORE SCORES IN A DATAFRAME AND SORT DESCENDINGLY BASED ON VALUE, THEN TAKE OUT ITEMS THAT THE USER ALREADY LIKED
    df_items = pd.DataFrame({
        'imdb_id': df_raw['imdb_id'],
        'score': item_scores
    }).sort_values(by='score', ascending=False)

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
def generate_carousel_data_popularity(df_raw): 
    # PREPARE DATAFRAME
    df_filtered = df_raw[['imdb_id', 'title', 'item_type', 'year', 'genres', 'runtime', 'actors', 'rating', 'rating_votecount']].copy()

    # USE THE LIKED ITEMTYPE-GENRE COMBINATIONS TO COMPUTE SIMILARITY SCORES FOR ALL COMBINATIONS
    # --- TO DO ---
    # - ADD WEIGHTS TO THE SIMILARITY SCORE?

    def generate_popularity_scores(df_combinations, min_score, max_score):
        popularity_scores = []
        for _, row in df_combinations.iterrows():
            lower_bound = 1
            upper_bound = 10
            normalized_score = lower_bound + ((row['avg_rating_votecount'] - min_score) * (upper_bound - lower_bound)) / (max_score - min_score)
            popularity_score = (row['avg_rating'] + normalized_score) / 2
            popularity_scores.append(popularity_score)
        return popularity_scores

    combination_rows = []

    for index, row in df_filtered.iterrows():
        item_type = row['item_type']
        genres = row['genres'].split(",")

        # RANDOMLY ASSIGN EITHER 1 OR 0 AS A SIMILARITY SCORE
        for genre in genres:
                combination_rows.append({
                    'imdb_id': row['imdb_id'],
                    'item_type': item_type,
                    'genre': genre.strip(),
                    'rating': row['rating'],
                    'rating_votecount': row['rating_votecount']
                })
    df_combinations = pd.DataFrame(combination_rows)

    df_combinations = df_combinations.groupby(['item_type', 'genre']).agg(
        avg_rating=('rating', 'mean'),
        avg_rating_votecount=('rating_votecount', 'mean')
    ).reset_index()

    min_score = df_combinations['avg_rating_votecount'].min()
    max_score = df_combinations['avg_rating_votecount'].max()

    popularity_scores = generate_popularity_scores(df_combinations, min_score, max_score)
    df_combinations['popularity_score'] = popularity_scores

    # STORE THE SIMILARITY SCORES IN A DATAFRAME AND GENERATE THE TOTAL SCORE FOR ALL COMBINATIONS
    # --- TO DO ---
    # - FIGURE OUT IF IT'S AN ISSUE THAT THESE SCORES ARE NOT NORMALISED (I.E. GENRE-ITEMTYPE COMBINATIONS THAT OCCUR MORE NATURALLY HAVE A HIGHER SCORE)    
    recommended_combinations = df_combinations.sort_values(by='popularity_score', ascending=False)

    # GENERATE TOP 6 COMBINATIONS FOR MOVIES, SERIES, AND BOTH
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
    def generate_carousel_objects(combinations_df, df_raw):
        combinations = []
        # GENERATE LIST OF COMBINATIONS TO FEED TO THE generate_carousel_items FUNCTION
        for _, row in combinations_df.iterrows():
            item_type = row['item_type']
            genre = row['genre']
            combinations.append({
                'item_type': item_type,
                'genre': genre
            })
        
        carousel_objects = generate_carousel_items_popularity(combinations, df_raw)
        return carousel_objects

    # GENERATE CAROUSEL OBJECTS FOR MOVIES, SERIES, AND BOTH (ALL)
    carousel_objects_all = generate_carousel_objects(df_all, df_raw)
    carousel_objects_movies = generate_carousel_objects(df_movies, df_raw)
    carousel_objects_series = generate_carousel_objects(df_series, df_raw)

    return {
         'home_carousels': carousel_objects_all,
         'movie_carousels': carousel_objects_movies,
         'series_carousels': carousel_objects_series
    }