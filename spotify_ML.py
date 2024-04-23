
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from functools import reduce
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import oauth2



# Huda's Credentials
cid = 'b8e80eff330e45fabd50a76166723f3d'
secret = '1780e668755b404f9f0c1b16f83a0113'
redirect_uri = "http://localhost:8888/callback"
username = '313vt7klumo3nsclaxmdi7sqxipy'

# Load your preprocessed data


#  Authorization and sp to call the APIs
scope = 'user-top-read playlist-modify-private playlist-modify-public'
token = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret, redirect_uri=redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)

playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f&nd=1&dlsi=6ce05bd2564c4195"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"][:20]]

df = pd.read_csv('playlist_song_analysis.csv')
track_data = []

# Iterating through each track in the playlist
for track in sp.playlist_tracks(playlist_URI)["items"][:20]:
    # Store track information in a dictionary
    track_info = {

        "Artist": track["track"]["artists"][0]["name"],
        "Track": str(track["track"]["name"]),
        "ratings": track["track"]["popularity"] / 100  # Normalize popularity scale to 0-1
    }
    # Append the dictionary to the list of track data
    track_data.append(track_info)

# Convert the list of dictionaries to a DataFrame
new_df = pd.DataFrame(track_data)


# Assuming you already have your DataFrame 'df' with the relevant data


features = df[['Popularity', 'Sentiment']]  # features necessary for k-clustering

# Scaling the fetaures
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# K-means Clustering

k = 6  # Ecjosing 3 clusters

# Initializing  and fit the K-means model
kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(scaled_features)

# Add cluster labels to the DataFrame
df['Cluster'] = kmeans.labels_
# print(df)
# # # 4. Model Evaluation: Elbow method to determine the optimal number of clusters
inertia_values = []
k_values = range(1, 10)

for k in k_values:
    kmeans_model = KMeans(n_clusters=k, random_state=42)
    kmeans_model.fit(scaled_features)
    inertia_values.append(kmeans_model.inertia_)

#Plotting the Elbow Method to see best value of k 
plt.figure()
plt.plot(k_values, inertia_values, marker='o')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia (Within-cluster sum of squares)')
plt.title('Elbow Method for Optimal Number of Clusters')
plt.show()


# # Adding  a column for the cluster assignment to the DataFrame
df['Cluster'] = kmeans.labels_  # Replace `kmeans` with your clustering model

# # Plot the clusters
plt.figure(figsize=(10, 6))
for cluster in df['Cluster'].unique():
    # getting cluster from df
    cluster_data = df[df['Cluster'] == cluster]
    
    # Scatter plot of the cluster data
    plt.scatter(cluster_data["Sentiment"], cluster_data["Popularity"], label=f'Cluster {cluster}', alpha=0.7)
    
# Add labels and title
plt.xlabel("Sentiment")
plt.ylabel("Popularity")
plt.title('Clustering of Songs by Sentiment and Popularity')
plt.legend()
plt.show()



# Just to see the songs by their cluster
for cluster in range(k):
    cluster_df = df[df['Cluster'] == cluster]
    print(f"Cluster {cluster} contains {len(cluster_df)} songs")
    print(cluster_df[['Track', 'Artist']].head())



