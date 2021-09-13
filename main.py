from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from pprint import pprint
import sys
date = input("Please enter the desired date in YYYY-MM-DD formad:\n")
sp_url = "https://accounts.spotify.com/authorize"
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, "html.parser")
song_names = soup.find_all(name="span", class_= "chart-element__information__song")
song_list = []
for name in song_names:
    song_list.append(name.getText())

client_id= os.environ.get("CLIENTID")
secret= os.environ.get("SECRET")
user_id= os.environ.get("USERID")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private", redirect_uri= "http://myapp.com/callback/", client_id=client_id, client_secret=secret,show_dialog=True, cache_path="token.txt"))
playlist = sp.user_playlist_create(user=user_id, name= f"Top 100 songs of {date}", public=False)
song_uri = []
for name in song_list:
    song_uri.append(sp.search(q=name,limit=1, type="track")["tracks"]["items"][0]["uri"])

real_uri = []
for ind in song_uri:
    spl = ind.split(":")
    real_uri.append(spl[len(spl)-1])

playlist_id = playlist["id"]

try:
    sp.playlist_add_items(playlist_id= playlist_id, items= song_uri)
except:
    pass
