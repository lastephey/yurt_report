#! python

# yurt_report project, written 2017 by LS
# the plotting parts of this script taken from https://matplotlib.org/examples/pylab_examples/date_demo_convert.html
# this script designed to download the twitter data in json format, parse it, and process it in a basic way (more exciting analysis coming soon!)

import json
import matplotlib.pyplot as plt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
import numpy as np
from numpy import arange
import time
import datetime
from yurt_download import download_yurt_tweets

#download the most recent data
download_yurt_tweets()

#number of tweets to analyze
#288 tweets per day at one tweet every 5 min
ndays=5
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
for i in range(0,ntweets):
    if "There" in text_data[i]:
        cat_status.append(1)
        analysis_array.append(i)
    elif "Sorry" in text_data[i]:
        cat_status.append(0)
        analysis_array.append(i)
    else:
        continue
        
#now need to extract timestamps
#timestamp always starts at the 18th character in both cases
#timestamp always ends at the 44th character in both cases
time_data=[]
time_data_s=[]	
for i in range(0,len(analysis_array)):
    j=analysis_array[i]
    text_temp=text_data[j]	
    #this array is timestamp strings
    time_data.append(text_temp[18:44])
    #this converts the timestamp string to seconds
    time_data_s.append((datetime.datetime.strptime(text_temp[18:44], "%Y-%m-%d %H:%M:%S.%f")))
	
# ok now plot
fig, ax = plt.subplots()
ax.plot_date(time_data_s, cat_status)
ax.xaxis.set_major_locator(DayLocator())
ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
fig.autofmt_xdate()
plt.title("Historical cat occupancy in yurt")
plt.ylabel("Cat status")
plt.xlabel("Date")
fig.savefig('historical_cat_yurt_status.png')
plt.show()

	
	
	
	

	
	
	
	
	
	
	
	
