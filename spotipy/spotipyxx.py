import os
import sys
import webbrowser
import json
import requests
import spotipy

#need to be running on python 3.11 for these
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

# My User ID: 36b6fa134ea44809 
#string: ndao99

#setting environment variables for spotipy
os.environ['SPOTIPY_CLIENT_ID'] = "d8c9d086b1714bbaad9b9d1448817add"
os.environ['SPOTIPY_CLIENT_SECRET'] = "f33e37aaf4704ba7941ab2f034ce253a"
os.environ['SPOTIPY_REDIRECT_URI'] = "https://localhost:8888/callback"

#parameters for a post request
url = "https://accounts.spotify.com/api/token"
data = "grant_type=client_credentials&client_id=d8c9d086b1714bbaad9b9d1448817add&client_secret=f33e37aaf4704ba7941ab2f034ce253a"
headers = {"Content-Type": "application/x-www-form-urlencoded"}

#requests an authorization token and saves it as a variable: the SpotifyOAuth accepts token automatically.

response = requests.post(url, data=data, headers=headers)
response_json = response.json()
access_token = response_json['access_token']

#adds tracks to playlist
def add_track(playlist, track_list):
    scope = ["playlist-modify-public", "playlist-modify-private"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    sp.playlist_add_items(playlist_id=playlist)

#creates playlist and adds tracks to it
def create_playlist():
    scope = ["playlist-modify-public", "playlist-modify-private"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    playlist = sp.user_playlist_create(user="ndao99", name="Recommended Songs", public=False, description="This is a test")

    playlist_id = playlist['id']
    add_track(playlist_id)

#prints out users top 50 tracks
def user_top_tracks():
    scope = "user-top-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    ranges = ['short_term', 'medium_term', 'long_term']

    for sp_range in ranges:
        print("range:", sp_range)
        results = sp.current_user_top_tracks(time_range=sp_range, limit=50)
        for i, item in enumerate(results['items']):
            print(i, item['name'], '//', item['artists'][0]['name'])
        print()


#testing a search
sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
track_name = "Love Again" 
artist = "Daniel Ceasar"
track_id = sp.search(q=f"Artist:{artist} track: {track_name}", type="track")
print(track_id)

