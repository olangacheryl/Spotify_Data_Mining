# Spotify_Data_Mining
For our spotify.py program to run, search spotify developer on the web and create an account. Afterwards, on your creator dashboard, under settings, Spotify will provide you with the following details that you should paste in the Spotify.py file under the Authentication/Authorization section: cid, secret, redirect_uri, and username. From there, when you run our code, you will be able to get the results that we got.

disclaimer: the redirect_uri doesn't really work, it is just Spotify's way of authenticating you. Just make sure after you run your code, you are redirected to a seprate page where Spotify asks you to confirm your identity. Also, do not share the secret. 
It is also important to note that the top twenty tracks we extracted from this playlist are constantly being updated by Spotify, therefore the following tracks shown on report were taken from the week of May 3 and are subject to change resulting in different data if program is ran at a later time. 
To run our Python Programs , follow the instructions below to set up your Spotify Developer account and obtain the necessary credentials.

Here is the detailed Steps:
#1. Create a Spotify Developer Account
Go to the Spotify Developer website and create an account if you don't have one already.
Once logged in, navigate to your developer dashboard.
\n
#2. Obtain Your Spotify API Credentials
In your dashboard, create a new app (if you haven't already).
Under the app settings, you will find the following details:
Client ID (cid)
Client Secret (secret)
Redirect URI (redirect_uri)
Copy these credentials.
\n
#3. Update Your Spotify.py File
Open the spotify.py file.
Look for the Authentication/Authorization section in the script.
Replace the existing credentials with your own credentials from Step 2:
python
Copy code
\n
# Your Spotify Credentials

cid = 'YOUR_CLIENT_ID_HERE'
secret = 'YOUR_CLIENT_SECRET_HERE'
redirect_uri = 'YOUR_REDIRECT_URI_HERE'
username = 'YOUR_USERNAME_HERE'

**4. Run the Program**s
Execute the spotify.py script.
You may be redirected to a separate page where Spotify asks you to confirm your identity.
Once you authenticate, the program will proceed with the analysis.
Important Notes
Do Not Share your Client Secret or other sensitive information.
The Redirect URI is part of the authentication process and may not function as expected. Simply follow the authentication steps when prompted.
The top 20 tracks we extracted from the playlist are regularly updated by Spotify. The results shown in the report are from the week of May 3 and may change if you run the program at a different time.
