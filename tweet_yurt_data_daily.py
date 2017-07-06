#! python

# yurt_report project, written 2017 by LS
# script to download the past day's tweets, analyze them, plot them, and automatically post the plot to twitter!


import json
import matplotlib.pyplot as plt
from matplotlib.pyplot import hist
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, date2num, num2date
import numpy as np
from numpy import arange
import time
import datetime
from yurt_download import download_yurt_tweets
from twython import Twython
import os

#load twitter data
from auth import (
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
)

#keep checking to see what time it is every 60 s
#at some time every day, generate the last 24 hour report
report_time='22:08:00';
FMT='%H:%M:%S'
print(flush=True)
while True:
    #need to flush out print buffer, apparently
    print(flush=True)
    #cut off microseonds, we don't need them
    now_time=str(datetime.datetime.now().time())[:8]
    print("Current time is %s" %now_time)
    deltat=datetime.datetime.strptime(report_time,FMT)-datetime.datetime.strptime(now_time,FMT)
    deltat_ms=divmod(deltat.days * 86400 + deltat.seconds, 60)
    deltat_min=deltat_ms[0]
    time.sleep(50)
    if -1 <= deltat_min <= 0: #which should happen around the report time (hopefully)
        print("It's report time! Here we go...")
        #then start the downloading, analyzing, and plotting process
        #download the most recent data
        download_yurt_tweets()

        #number of tweets to analyze
        #288 tweets per day at one tweet every 5 min
        ndays=1
        tweets_per_day=288
        ntweets=ndays*tweets_per_day

        #now reassemble the data line by line, the same way we wrote the file
        data = []
        with open('saved_yurt_tweets.json') as f:
            for line in f:
                data.append(json.loads(line))

        text_data=[]
        for i in range(0,len(data)):	
            text_data.append(data[i]["text"])

        #now we need to parse the data and pull out the parts to use!
        #need timestamp and yurt status
        #first just create plot of timestamp vs yurt status (0 or 1)
        #need to sort which tweets we can actually use for analysis (exclude images and other tweets)
        analysis_array=[]
        cat_status=[]
        cat_present=[]
        for i in range(0,ntweets):
            if "There" in text_data[i]:
                cat_status.append(1)
                analysis_array.append(i)
                cat_present.append(i)
            elif "Sorry" in text_data[i]:
                cat_status.append(0)
                analysis_array.append(i)
            else:
                continue
                
        #get timestamps when cat is present
        cat_present_dt=[]	
        cat_present_list=[]
        cat_present_hour=[]
        for i in range(0,len(cat_present)):
            j=cat_present[i]
            text_temp=text_data[j]	
            #this writes a list
            cat_present_list.append(text_temp[18:44])
            #this converts to datetime objects
            cat_present_dt.append((datetime.datetime.strptime(text_temp[18:44], "%Y-%m-%d %H:%M:%S.%f")))    
            #also keep track of which hours cats are present, this is equally ugly
            cat_present_hour.append(int(text_temp[29:31]))
           
        #now plot histogram of which times are most popular
        c=plt.figure(1)
        plt.hist(cat_present_hour,bins=24)
        plt.xlabel("Time (hour)")
        plt.ylabel("Number of cat present tweets")
        plt.title("Past 24 hours yurt occupancy")
        c.savefig('popular_yurt_times_daily.png')
        
        #okay, now that we've generated the data, post it to twitter!
        twitter = Twython(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
        )
        
        # get system time for timestamp on tweet to avoid duplicates
        now=datetime.datetime.now()

        #and upload
        message=("Here is today's Yurt Report! %s" % now)
        tweetpic = open("popular_yurt_times_daily.png","rb")
        # Update status with our new image and status
        twitter.update_status_with_media(status=message, media=tweetpic)
        print("Tweeted: %s" % message)

        
        
            
            
            
