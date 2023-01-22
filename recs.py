import re, operator
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from joblib import load

file_tracks = pd.read_csv('./tracks.csv')

top = []
for row in np.array(file_tracks):
    if row[2] > 50: top.append(row) # only add songs who have rating > 50

popular_tracks = pd.DataFrame(populars, columns=['id', 'name', 'rating', 'duration_ms', 'explicit', 'artists',
    'id_artists', 'release_date', 'dance', 'energy', 'key',
    'volume', 'mode', 'wordy', 'guitar', 'instrument',
    'energy', 'genre', 'tempo', 'time_signature'])

model = KMeans(n_clusters=2).fit(tracks[['dance', 'vibe', 'volume', 'genre']])
tracks['cluster_no'] = model.labels_

def element(arr, str_arr):
    for elem in arr:
        if elem in str_arr:
            return True
    return False

# Data to panda
def data(raw_data):
    user_data = []
    feature_names = ['id', 'dance', 'energy', 'volume',
                    'tempo', 'guitar', 'genre', 'wordy',
                    'instrument', 'fav']

    for playlist_id, tracks in raw_data:
        for track in tracks:
            user_data.append([
                track['id'], track['dance'], track['energy'],
                track['volume'], track['tempo'], track['guitar'],
                track['genre'], track['wordy'], track['instrument'], 1
            ])

    return pd.DataFrame(user_data, columns=feature_names)


# Garbage logic applied here:
#   Clusterized whole popular_tracks dataframe into 3 clusters (based on energy: high, medium, low) along with liked_tracks
#   Obtained the most prominent cluster number
#   get songs with the obtained cluster number
def make_predictions(raw_data):
    global popular_tracks, model

    fav_songs = data(raw_data)
    prediction_factors = ['dance', 'energy', 'volume', 'genre']

    liked_cluster = round(model.predict(fav_songs[prediction_factors]).mean())

    # Get most listened artists
    fav_artists = {}
    for row in np.array(popular_tracks[['artists', 'cluster_no']]):
        if row[1] != liked_cluster:
            continue

        artists = row[0].replace('[', '').replace(']', '').replace("'", "").replace("\"", "")
        if ',' in artists:
            artist_arr = artists.split(', ')
        else: artist_arr = [artists]
        
        for artist in artist_arr:
            fav_artist[artist] = fav_artist.get(artist, 0) + 1

    fav_artist = dict([i for i in sorted(fav_artist.items(), key=operator.itemgetter(1), reverse=True) if i[1] > 2])

    recommended = []
    for row in np.array(popular_tracks[['name', 'artists', 'id', 'cluster_no']]):
        if row[-1] == liked_cluster and element(fav_artist.keys(), row[1]):
            recommended.append([row[0], row[2]])
    
    return recommended
