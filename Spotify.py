import time
import os
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
#%config InlineBackend.figure_format ='retina'  ##this is just for high resolution 
import seaborn as sns
import random
from functools import reduce
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import oauth2
import csv 

# The authorization required by the spotify API
cid = ''
secret = ''
redirect_uri=""
username = ''

#Authorization and sp to call the APIs
scope = 'user-top-read playlist-modify-private playlist-modify-public'
token = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret, redirect_uri=redirect_uri)
#Ensuring Authorization was successful
if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)



playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f&nd=1&dlsi=6ce05bd2564c4195" #provided by the spotify app
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

for track in sp.playlist_tracks(playlist_URI)["items"]: #looping through the tracks in the playlist_link
    #URI
    track_uri = track["track"]["uri"]
    
    #Track name
    track_name = track["track"]["name"]
    
    #Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)
    
    #Name, popularity, genre
    artist_name = track["track"]["artists"][0]["name"]
    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]
    # print(artist_genres)
    #Album
    album = track["track"]["album"]["name"]
    
    #Popularity of the track
    track_pop = track["track"]["popularity"]

    df= pd.DataFrame(columns= [track_name,  artist_name, artist_pop,  artist_genres])
    data = [track_name, artist_name, artist_pop, artist_genres]
    print(data)
    
# references: https://github.com/lognorman20/spotify_recommender/blob/main/data_engineering.ipynb
#references: https://towardsdatascience.com/spotify-sentiment-analysis-8d48b0a492f2
   


