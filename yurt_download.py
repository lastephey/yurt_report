#! python

# yurt_report project, written 2017 by LS
# this function designed to pull the tweets made by @yurt_report and save them in json format for further processing

def download_yurt_tweets():

     import tweepy
     from tweepy import OAuthHandler
     import json

     # load authentication key info
     from auth import (
             consumer_key,
             consumer_secret,
             access_token,
             access_token_secret
     )

     auth = OAuthHandler(consumer_key, consumer_secret)
     auth.set_access_token(access_token, access_token_secret)
 
     api = tweepy.API(auth)


     with open('saved_yurt_tweets.json', 'w') as outfile:
          for tweet in tweepy.Cursor(api.user_timeline).items():
               json.dump(tweet._json, outfile)
		  
     print('finsihed downloading tweets')		  
