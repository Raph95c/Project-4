# =---------------------=
# | Importing Depencies |
# =---------------------=
import os
import sys
import webbrowser
import json
import requests
import spotipy
from pprint import pprint

#need to be running on python 3.11 for these
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util

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

#right now this gets name, artist, and album for list of songs
def get_song_info(song_id_list):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

    for id in song_id_list:
        track = sp.track(id)
        song_name = track["name"]
        song_artist = track["artists"][0]["name"]
        song_album = track["album"]["name"]
        print(f"{song_name} by {song_artist}")

#prints out users top 10 tracks
def user_top_tracks():
    scope = "user-top-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    ranges = ['short_term', 'medium_term', 'long_term']

    for sp_range in ranges:
        print("range:", sp_range)
        results = sp.current_user_top_tracks(time_range=sp_range, limit=10)

        for i, item in enumerate(results['items']):
            print(i, item['name'], '//', item['artists'][0]['name'])
        print()


#song list from track clustering
song_list = ['7MdZQXUBijQxcBkYz4G1Z5',
 '0zhzkkSXFj60Y5fzb2j9hU',
 '7v52k3ozNqjKGlFPWDiudw',
 '6ZGqVXaJmhbYAK2DF8mWRR',
 '3V0nnQhqvbE3JmiDdnzQFQ']

def main():
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
    get_song_info(song_list)


if __name__ == "__main__":
    main()