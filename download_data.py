#! python

# yurt_report project, written 2017 by LS
# pieces of this function were taken from https://nocodewebscraping.com/twitter-json-examples/
# this program should save the last 3000 or so tweets and put them into a file with today's date for future processing

import tweepy
from tweepy import OAuthHandler
import json
import time

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

#initialize a list to hold all the tweepy Tweets
alltweets = []    

#make initial request for most recent tweets (200 is the maximum allowed count)
new_tweets = api.user_timeline(count=200)

#first save most recent tweets
alltweets.extend(new_tweets)

#save the id of the oldest tweet less one
oldest = alltweets[-1].id - 1

#then check for older tweets, keep going until none are left (or we hit our limit)
while len(new_tweets) > 0:
    
    #all subsiquent requests use the max_id param to prevent duplicates
    new_tweets = api.user_timeline(count=200,max_id=oldest)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    

alltweets_json=[]
for i in range(0,len(alltweets)):	
    status=alltweets[i]	 		
    #append in json format		
    alltweets_json.append(json.dumps(status._json))
    
    
#print how many tweets we got
print("Downloading %s tweets" % len(alltweets_json))	

today=time.strftime("%x")
#remove slashes
today_ns= today.replace("/", "")

print(today_ns)

savestring='saved_tweets_%s.json' %today_ns

print(savestring)

#write tweet objects to file
with open(savestring, 'w', encoding="utf-8") as outfile:
    for line in alltweets_json:
        outfile.write("%s\n" % line)

#close the file
print("Done")
outfile.close()