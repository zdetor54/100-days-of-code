from bs4 import BeautifulSoup
import requests

URL = 'https://www.billboard.com/charts/hot-100/'


year = input("What is the date (YYYY-MM-DD) you wanna use for your playlist:")

# year = '2000-01-01'

response = requests.get(url=f"{URL}{year}/")
soup = BeautifulSoup(markup=response.text, features="html.parser")
songs = [x.find(name='h3').getText().strip() for x in soup.findAll(class_='o-chart-results-list-row-container')]

print(songs)

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

CLIENT_ID = '82478238db19484393fb988e436cd84b'
CLIENT_SECRET = '1a5e7e504f8a42ea937a1d28fb371a31'
REDIRECT_URI = 'http://example.com'
scope = "playlist-modify-private"


# Initialize the Spotipy client with OAuth credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope))

# Get the current user's profile
user_profile = sp.current_user()
user_id = user_profile['id']
# print("User ID:", user_profile['id'])
# print("Display Name:", user_profile['display_name'])


type_ = 'track'
limit_ = 1
song_uri = []

for song in songs:
    song_title = song.lower()
    q_ = f'{song_title}%20year:{year[:4]}'
    print(song_title)
    sp_result = sp.search(q=q_, type=type_, limit=limit_)
    try:
        song_uri.append(sp_result['tracks']['items'][0]['uri'])
        print(sp_result['tracks']['items'][0]['external_urls'])
    except IndexError:
        print('Song not found')

# Create the playlist


playlist = sp.user_playlist_create(user=user_id, name =f'Billboard Playlist {year}', public=False)  # Set 'public' to False for a private playlist
playlist_id = playlist['id']

sp.playlist_add_items(playlist_id= playlist_id, items= song_uri, position=None)
