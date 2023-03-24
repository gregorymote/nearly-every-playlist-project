import os

#Spotify
CLIENT_ID = os.getenv('PLAYLIST_CLIENT_ID', 'my-spotify-client-id')
CLIENT_SECRET = os.getenv('PLAYLIST_CLIENT_SECRET', 'my-spotify-client-secret')
REDIRECT_URI = 'http://localhost:8000/auth/'
USERNAME = '<my-spotify-username>'
TRACK = '6hTcuIQa0sxrrByu9wTD7s' #Tack ID for Born to Run - Search for Track ID @ https://developer.spotify.com/console/get-search-item/?q=Born%20to%20Run&type=track


#Twitter
CONSUMER_KEY = os.getenv('PLAYLIST_TWITTER_CONSUMER_KEY', 'my-twitter-consumer-key')
CONSUMER_SECRET = os.getenv('PLAYLIST_TWITTER_CONSUMER_SECRET', 'my-twitter-consumer-secret')
BEARER =  os.getenv('PLAYLIST_TWITTER_BEARER', 'my-twitter-bearer')
ACCESS_TOKEN = os.getenv('PLAYLIST_TWITTER_ACCESS_TOKEN', 'my-twitter-access-token')
ACCESS_SECRET =  os.getenv('PLAYLIST_TWITTER_ACCESS_SECRET', 'my-twitter-access-secret')
