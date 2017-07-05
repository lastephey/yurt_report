#! python

# yurt_report project, written 2017 by LS
# script to test image upload

from twython import Twython
import time
import os
import datetime


from auth import (
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
)

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
tweetpic = open("C:/Yurt_report/popular_yurt_times_daily.png","rb")
# Update status with our new image and status
twitter.update_status_with_media(status=message, media=tweetpic)
print("Tweeted: %s" % message)
