from cos_generators import generate_similarity_database_cosine, generate_carousel_data_cosine
from random_generators import generate_similarity_database_random, generate_carousel_data_random
from popularity_generators import generate_similarity_database_popularity, generate_carousel_data_popularity
import pandas as pd

def algorithm1(df_raw):
    carousel_objects = generate_carousel_data_random(df_raw)
    item_object_list = generate_similarity_database_random(df_raw)

    return {
        'carousel_objects': carousel_objects,
        'item_object_list': item_object_list
    }

def algorithm2(df_raw):
    carousel_objects = generate_carousel_data_popularity(df_raw)
    item_object_list = generate_similarity_database_popularity(df_raw)

    return {
        'carousel_objects': carousel_objects,
        'item_object_list': item_object_list
    }

def algorithm3(liked_items, df_raw, encoded_data_path):
    df_encoded = pd.read_csv(encoded_data_path, header=0)

    carousel_objects = generate_carousel_data_cosine(liked_items, df_raw, df_encoded)
    item_object_list = generate_similarity_database_cosine(liked_items, df_raw, df_encoded)

    return {
        'carousel_objects': carousel_objects,
        'item_object_list': item_object_list
    }

