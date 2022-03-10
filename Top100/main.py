import os
from typing import List, Any

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

ID = os.environ['USERNAME']
secret = os.environ['KEY']
date = input("What date do you want to listen to? (YYYY-MM-DD):")


response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
text = response.text
soup = BeautifulSoup(text, "html.parser")
songs = soup.findAll(name="h3", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
titles = []
for song in songs:
    titles.append(song.getText().strip())

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=ID,
                                               client_secret=secret,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               ))

user_id = sp.current_user()["id"]
# print(user_id)
song_uris = []
year = date.split("-")[0]
for song in titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist_id = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, collaborative=False, description="Top 100 Songs from my birthday, 10/22/1994")
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id["id"], tracks=song_uris, position=None)
