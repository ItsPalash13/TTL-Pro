from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import os
import pandas as pd
import numpy as np
import json

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_movies_list():
    selected_columns = ['title', 'index', 'id']
    df_subset = df.head(200)[selected_columns]  # Select only the desired columns
    list_of_dicts = df_subset.to_dict(orient='records')
    return list_of_dicts


def get_title_from_index(index):
    row = df.iloc[index]
    return row.to_dict()

def get_index_from_title(title):
	return df[df.title == title]["index"].values[0]

def get_index_from_id(id):
	return df[df.id == id]["index"].values[0]

csv_file_path = os.path.join(os.path.dirname(__file__), 'merged_csv_file1.csv')
df = pd.read_csv(csv_file_path)
features = ['keywords','cast','genres','director']
##Step 3: Create a column in DF which combines all selected features
for feature in features:
	df[feature] = df[feature].fillna('')

def combine_features(row):
    try:
        # Check if any of the features are None, if so, replace with an empty string
        keywords = row['keywords'] if isinstance(row['keywords'], str) else ''
        cast = row['cast'] if isinstance(row['cast'], str) else ''
        genres = row['genres'] if isinstance(row['genres'], str) else ''
        director = row['director'] if isinstance(row['director'], str) else ''
        
        return keywords + " " + cast + " " + genres + " " + director
    except Exception as e:
        print("Error:", e)


df["combined_features"] = df.apply(combine_features,axis=1)

#print("Combined Features:", df["combined_features"].head())

##Step 4: Create count matrix from this new combined column
cv = CountVectorizer()

count_matrix = cv.fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(count_matrix) 

def getrecom(movie_index): 
    movie_index=get_index_from_id(movie_index)
    similar_movies =  enumerate(cosine_sim[movie_index])

    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

    # Getting top 10 similar movies
    top_similar_movies = []
    for i in range(10):
        top_similar_movies.append(get_title_from_index(sorted_similar_movies[i][0]))

    return top_similar_movies
    
# Create your views here.
def members(request):
    return HttpResponse("Hello world!")

def list(request):
    r = get_movies_list()
    return JsonResponse({'data': r}) 

def popular(request):

    r = getrecom(eval(request.GET.get('movie')))
    print(type(r))
    return JsonResponse({'top': r}) 