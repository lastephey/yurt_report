#! python

# yurt_report project, written 2017 by LS
# pieces of this function were taken from https://nocodewebscraping.com/twitter-json-examples/
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
	
	#initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
	
    #print alltweets here
    #print(alltweets)
    
    #keep grabbing tweets until there are no tweets left to grab


    while len(new_tweets) > 0:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(count=200,max_id=oldest)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
		
    counter=0	
    alltweets_json=[]
    for i in range(0,len(alltweets)):	
        status=alltweets[counter]	 		
        #append in json format		
        alltweets_json.append(json.dumps(status._json))
        counter += 1	
		
    #print how many tweets we got
    print("Downloading %s tweets" % len(alltweets_json))	
	
    #print raw alltweets list
    #print(alltweets_json)
  	
    #write tweet objects to file
    with open('saved_yurt_tweets.json', 'w') as outfile:
        for line in alltweets_json:
            outfile.write("%s\n" % line)
    
    #close the file
    print("Done")
    outfile.close()