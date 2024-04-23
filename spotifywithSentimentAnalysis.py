import time
import os
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
import random
from functools import reduce
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import oauth2
from textblob import TextBlob
import lyricsgenius

# Insert your Spotify username and the credentials that you obtained from Spotify developer
cid = '5370c0ca87054f429022354f75b83c9f'
secret = '8931c1ca07414c1c961cb8660939ac92'
redirect_uri = 'http://localhost:3000/analysis'
username = 'hadasa'

# Once the Authorisation is complete, we just need to `sp` to call the APIs
scope = 'user-top-read playlist-modify-private playlist-modify-public'
token = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret, redirect_uri=redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)


# Getting features for each song
def fetch_audio_features(sp, df):
    playlist = df[['track_id', 'track_name']]
    index = 0
    audio_features = []

    # Make the API request
    while index < playlist.shape[0]:
        audio_features += sp.audio_features(playlist.iloc[index:index + 50, 0])
        index += 50

    # Create an empty list to feed in different characteristics of the tracks
    features_list = []
    # Create keys-values of empty lists inside nested dictionary for album
    for features in audio_features:
        features_list.append([features['danceability'],
                              features['acousticness'],
                              features['energy'],
                              features['tempo'],
                              features['instrumentalness'],
                              features['loudness'],
                              features['liveness'],
                              features['duration_ms'],
                              features['key'],
                              features['valence'],
                              features['speechiness'],
                              features['mode']
                              ])

    df_audio_features = pd.DataFrame(features_list, columns=['danceability', 'acousticness', 'energy', 'tempo',
                                                             'instrumentalness', 'loudness', 'liveness', 'duration_ms', 'key',
                                                             'valence', 'speechiness', 'mode'])

    # Create the final df, using the 'track_id' as an index for future reference
    df_playlist_audio_features = pd.concat([playlist, df_audio_features], axis=1)
    df_playlist_audio_features.set_index('track_name', inplace=True, drop=True)
    return df_playlist_audio_features


# Getting playlist IDs from each of Spotify's playlists
playlists = sp.user_playlists('spotify')
spotify_playlist_ids = []
while playlists:
    for i, playlist in enumerate(playlists['items']):
        spotify_playlist_ids.append(playlist['uri'][-22:])
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None


# Creating a function to get the first 50 tracks IDs from a playlist
def getTrackIDs(playlist_id):
    playlist = sp.user_playlist('spotify', playlist_id)
    ids = []  # Fix: Define ids list here
    for item in playlist['tracks']['items'][:50]:
        track = item['track']
        ids.append(track['id'])  # Changed from "id" to "track_id"
    return ids  # Fix: Return ids list


# Creating a function to get the lyrics of each song
def get_lyrics(track_artist, track_name):
    lyrics = None
    try:
        # Added by Julia
        # Using Genius API, enter key credentials
        genius = lyricsgenius.Genius('gehQ281GDHsLX_LSk6IWVn5Y-Cb2H9Moa5YNXH3SS2Ol_hLcqqoYhcX6HLIShAbRFE6P8ieauLhqEKLw9JamJQ')  # Get your Genius API Key
        song = genius.search_song(track_name, track_artist)
        if song:
            lyrics = song.lyrics
    except Exception as e:
        print("Error occurred while fetching lyrics:", str(e))
    return lyrics


# Creating a function get features of each track from track id
def getTrackFeatures(track_id):
    meta = sp.track(track_id)
    features = sp.audio_features(track_id)

    # meta
    track_id = track_id
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']

    # changes made by cheryl
    track = []
    m1 = [track_id, name, album, artist, release_date, length, popularity, danceability, acousticness, energy,
          instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
    for i in m1:
        track.append(i)
    return track


# Gathering track ids
ids = []
for x in spotify_playlist_ids[:200]:
    ids.extend(getTrackIDs(x))  # Fix: Use extend instead of append

# loop over track ids to get audio features for each track
tracks = []
for i in range(len(ids)):
    try:
        track = getTrackFeatures(ids[i])
        tracks.append(track)
    except:
        pass

# create dataset
df = pd.DataFrame(tracks, columns=['track_id', 'name', 'album', 'artist', 'release_date', 'length', 'popularity',
                                   'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness',
                                   'speechiness', 'tempo', 'time_signature'])

df.to_csv('playlist_songs.csv', index=False)

df = pd.read_csv('playlist_songs.csv')
df.head()


# Edited by Julia below

# Function to perform sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(str(text))
    return analysis.sentiment.polarity


# Adding sentiment analysis for playlist titles
df_playlist_songs = pd.read_csv('playlist_songs.csv')  # Provide path to your playlist titles CSV
df_playlist_songs['playlist_sentiment'] = df_playlist_songs['name'].apply(analyze_sentiment)

# Adding sentiment analysis for song lyrics

# Fetching lyrics for each song
lyrics = []
for i in range(df.shape[0]):
    try:
        lyric = get_lyrics(df['artist'][i], df['name'][i])
        lyrics.append(lyric)
    except:
        lyrics.append(None)

df['lyrics'] = lyrics
df['lyrics_sentiment'] = df['lyrics'].apply(analyze_sentiment)

# Displaying results
print("Playlist Titles Sentiment:")
print(df_playlist_songs[['name', 'playlist_sentiment']].head())
print("\nSong Lyrics Sentiment:")
print(df[['name', 'lyrics_sentiment']].head())

# Save the dataframes to CSV
df_playlist_songs.to_csv('playlist_titles_sentiment.csv', index=False)
df.to_csv('playlist_songs_with_lyrics_sentiment.csv', index=False)