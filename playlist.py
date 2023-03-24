from spotipy.client import Spotify
import spotipy.oauth2 as oauth2 
from random_word import RandomWords
import tweepy
from settings import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, USERNAME, TRACK, ACCESS_SECRET, ACCESS_TOKEN, CONSUMER_KEY, CONSUMER_SECRET, BEARER
import requests
import datetime
import os

def check_token(token_info, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, username=USERNAME):
    sp_oauth = oauth2.SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret, 
        redirect_uri=redirect_uri,
        username=username
    )

    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


def has_track(playlist_id, spotify):
    offset = 0
    tracks = [1]
    while len(tracks) > 0:
        try:
            tracks = spotify.playlist_tracks(playlist_id, offset=offset)['items']
        except Exception as e:
            print(e)
            return False
        for track in tracks:
            if track['track'] and track['track']['href'] and 'track' in track['track']['href']:
                track_id = track['track']['href'].split('tracks/')
                if track_id[1] == TRACK:
                    return True
        offset += 100
    return False


def find_playlist(token_info, word=None, offset=0):

    playlists = {}
    limit = 50
    r = RandomWords()

    while True:
        if not word:
            word = r.get_random_word()
        search = {'playlists':{'next':True}} 
        if word:
            print("Searching Playlists w/ word: ", word)
            while search['playlists']['next'] != 'null' and offset < 1000:
                token_info = check_token(token_info)
                spotify = Spotify(auth=token_info['access_token'])
                search = spotify.search(q=word, limit=limit, offset=offset, type='playlist')
                index = 0
                for playlist in search['playlists']['items']:
                    if playlist['id'] not in playlists:
                        playlists[playlist['id']] = playlist['name']
                        if has_track(playlist['id'], spotify):
                            return {
                                'object': playlist,
                                'offset': offset,
                                'index' : index + 1,
                                'word': word
                                }
                    index+=1
                offset+=limit
        word= None
        offset = 0


if __name__ == "__main__":

    print("BOTIFY: Running Playlist Search - " + str(datetime.datetime.now()))

    client = tweepy.Client(
        bearer_token=BEARER,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN, 
        access_token_secret=ACCESS_SECRET
        )
    print("client established")

    user_tweets ={}
    for response in tweepy.Paginator(client.get_users_tweets, id='1487864170171228161', tweet_fields='entities', max_results=100): 
        if response.data:
            for tweet in response.data:
                user_tweets[tweet.entities['urls'][0]['expanded_url']] = tweet.id
    
    sp_oauth = oauth2.SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET, 
        redirect_uri=REDIRECT_URI,
        username=USERNAME
    )
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        token_info = sp_oauth.get_access_token()
    print("token established")
    
    unique = False
    offset = 0
    index = 0
    word=None
    playlist = find_playlist(token_info=token_info, word=word, offset=offset + index)
    while not unique:
        playlist = find_playlist(token_info=token_info, word=word, offset=offset + index)
        url = playlist["object"]["external_urls"]["spotify"]
        unique = url not in user_tweets
        if not unique:
            offset = playlist["offset"]
            index = playlist["index"]
            word = playlist["word"]
    response = client.create_tweet(text=url)
    print("BOTIFY: ", response) 