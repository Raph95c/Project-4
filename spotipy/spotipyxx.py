# =---------------------=
# | Importing Depencies |
# =---------------------=
import os
import requests
import spotipy
import pandas as pd
import numpy as np
from pprint import pprint
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import scipy.spatial

#need to be running on python 3.11 for these
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util


path = Path() / "Data" / "tenyear_cleaned_for_kmeans.csv"
tracks_df = pd.read_csv(path)
column_names = tracks_df.columns
index = tracks_df.index

#creates playlist and adds tracks to it
def create_playlist():
    scope = ["playlist-modify-public", "playlist-modify-private"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    playlist = sp.user_playlist_create(user="ndao99", name="Recommended Songs", public=False, description="This is a test")

    playlist_id = playlist['id']
    add_track(playlist_id)

#adds tracks to playlist
def add_track(playlist):
    scope = ["playlist-modify-public", "playlist-modify-private"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    sp.playlist_add_items(playlist_id=playlist)

#gets the id of a track, given its name
def get_song_id(song_name):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
    track_name, artist = song_name.split(" by ")
    track_search = sp.search(q=f"Artist:{artist} track: {track_name}", type="track", limit=3)
    track_id = track_search['tracks']['items'][0]['id']
    search_result_song_name = track_search['tracks']['items'][0]['name']
    print(f"searching for songs like: {search_result_song_name} by {artist}")

    return track_id;

#accepts the track_id and returns our target features
def get_track_features(track_id):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
    feature_search = sp.audio_features(tracks=track_id)
    acousticness = feature_search[0]['acousticness']
    danceability = feature_search[0]['danceability']
    duration_ms = feature_search[0]['duration_ms']
    energy = feature_search[0]['energy']
    instrumentalness = feature_search[0]['instrumentalness']
    liveness = feature_search[0]['liveness']
    loudness = feature_search[0]['loudness']
    speechiness = feature_search[0]['speechiness']
    tempo = feature_search[0]['tempo']
    valence = feature_search[0]['valence']
    features = {"id": track_id, "acousticness":acousticness, "danceability":danceability, "duration_ms":duration_ms
                ,"energy":energy, "instrumentalness":instrumentalness, "liveness":liveness, "loudness":loudness
                , "speechiness":speechiness, "tempo":tempo, "valence":valence}
    
    return features;

#adding the features of the new song to the df to prep it for KMeans algorithm
def add_song_to_df(song_features, tracks_df):
    song_features_df = pd.DataFrame(song_features, index=[0])
    new_df = pd.concat([song_features_df, tracks_df])
    new_df = new_df.set_index(['id'])
    
    return new_df;

#runs kmeans with user song in it
def run_kmeans(tracks_df_w_new_song):
    column_names = tracks_df_w_new_song.columns
    index = tracks_df_w_new_song.index
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(tracks_df_w_new_song)
    tracks_df_scaled = pd.DataFrame(scaled_data, columns=column_names, index=index)

    k_model = KMeans(n_clusters=4, random_state=1)
    predictions = k_model.fit_predict(tracks_df_scaled)
    tracks_df_predictions = tracks_df_scaled.copy()
    tracks_df_predictions["ClusterGroup"] = predictions

    return tracks_df_predictions;

#recommends songs based on closest datapoints, but doesn't take into account for the clustergroup they're in 
def recommended_songs_id(predictions, song_feature1, song_feature2, track_list):
    feature1 = predictions['danceability']
    feature2 = predictions['energy']
    data_points = np.column_stack([feature1, feature2])
    ckdtree = scipy.spatial.cKDTree(data_points)
    song_recommendations = ckdtree.query([song_feature1, song_feature2],k=5)[1]

    song_ids = track_list.iloc[song_recommendations,:].index.to_list()

    return song_ids;

#gets track_name, artist, and album name with a list of track_ids 
def get_song_info(song_id_list):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
    
    for id in song_id_list:
        track = sp.track(id)
        song_name = track["name"]
        song_artist = track["artists"][0]["name"]
        song_album = track["album"]["name"]
        print(f"{song_name} by {song_artist}")

# def get_genres(track_id):
#     genres_list = []
#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
#     search = sp.track(track_id)
#     artist_id = search['album']['artists'][0]['id']
    
#     artist_search = sp.artist(artist_id)
#     genres = artist_search['genres']
#     print(genres)


# -------
#| Main |
# ------
def main():
    #setting environment variables for spotipy
    os.environ['SPOTIPY_CLIENT_ID'] = "d8c9d086b1714bbaad9b9d1448817add"
    os.environ['SPOTIPY_CLIENT_SECRET'] = "e6b7f13670bc4fec9b1b591acaa3eb8b"
    os.environ['SPOTIPY_REDIRECT_URI'] = "https://localhost:8888/callback"

    #requests an authorization token and saves it as a variable: the SpotifyOAuth accepts token automatically.
    response = requests.post(url="https://accounts.spotify.com/api/token"
                             ,data="grant_type=client_credentials&client_id=d8c9d086b1714bbaad9b9d1448817add&client_secret=e6b7f13670bc4fec9b1b591acaa3eb8b"
                             ,headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    response_json = response.json()
    access_token = response_json['access_token']

    song_name = input("What song do u like? (song by artist)")
    track_id = get_song_id(song_name)
    track_features = get_track_features(track_id)
    song_feature1, song_feature2 = track_features['danceability'], track_features['energy']

    df_with_user_song = add_song_to_df(track_features, tracks_df)
    predictions_df = run_kmeans(df_with_user_song)
    song_ids = recommended_songs_id(predictions_df, song_feature1, song_feature2, df_with_user_song)
    # recommended_songs = get_song_info(song_ids)

    print(song_ids)
    # print(recommended_songs)



if __name__ == "__main__":
    main()

