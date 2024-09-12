import pandas as pd
import spotipy
import spotipy.oauth2
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Authentication Spotipy API 
sp = spotipy.Spotify(
    auth_manager=spotipy.oauth2.SpotifyOAuth(
        scope="playlist-modify-private playlist-modify-public",
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        show_dialog=True,
        cache_path="token.txt"
    )
)
# Create a new playlist
def make_playlist(user_id, year):
    create_playlist = sp.user_playlist_create(
        user=user_id,  # Parameter should be 'user'
        name=f"Viral Song Indonesia{year}", # Name for Playlist
        description=f"Enjoy Listening", #Description for Playlist
        public=True  # <- should be boolean
    )
    return create_playlist
def get_URI_song(song_name): #Function for get  URI song
    response = sp.search(q=f"track:{song_name}", type="track", limit=1) #.searh() <-- This methods for get data URI
    track = response['tracks']['items']
    if track: #If track is not none return track
        song_track = track[0]['uri']
        return song_track
    else: #If track is none Retrun None
        print(f'Track of {song_name} not Find, Add manauly song in spotify app')
        return None
def add_song_playlist(track_songs, playlist_id): #This Funsiton for add song to playlist
    add_song = sp.playlist_add_items( #sp.playlist_add_items() This function for add Song to Playlist Spotify
        playlist_id = playlist_id, 
        items = track_songs, 
        position=None
    )
    return add_song

# Get User ID
user_id = sp.current_user()['id']
# Read CSV File/ Data
song_data = pd.read_csv('data_music_viral.csv')
# Get year from song
years = song_data["Tahun"].drop_duplicates()
for year in years: # Using Pandas Function for Filtering Years
    playlist = make_playlist(user_id, year) 
    songs_by_year = song_data.loc[song_data['Tahun'] == year, 'Judul Lagu'].tolist() #select using methods Pandas .loc for get specific data, and .tolist() using for add selected to "song_by_year" this methods can automatcly make variable to list python
    URI_songs = [uri for song_name in songs_by_year if ((uri := get_URI_song(song_name)) is not None)] # If Output == None, Not add uri to list
    playlist_id = playlist['id']
    add_song_to_playlist = add_song_playlist(URI_songs, playlist_id)
    print(f"Viral Song In {year}, finish create")

print(user_id)
