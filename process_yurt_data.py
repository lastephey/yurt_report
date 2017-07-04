#! python

# yurt_report project, written 2017 by LS
# the plotting parts of this script taken from https://matplotlib.org/examples/pylab_examples/date_demo_convert.html
# this script designed to download the twitter data in json format, parse it, and process it in a basic way (more exciting analysis coming soon!)

import json
import matplotlib.pyplot as plt
from matplotlib.pyplot import hist
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, date2num, num2date
import numpy as np
from numpy import arange
import time
import datetime
from yurt_download import download_yurt_tweets

#set which plots we want
plot_history=0

#download the most recent data
#download_yurt_tweets()

#number of tweets to analyze
#288 tweets per day at one tweet every 5 min
ndays=10
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
        
#now need to extract timestamps
#timestamp always starts at the 18th character in both cases
#timestamp always ends at the 44th character in both cases
time_data_dt=[]	
for i in range(0,len(analysis_array)):
    j=analysis_array[i]
    text_temp=text_data[j]	
    #this converts to datetime objects
    time_data_dt.append((datetime.datetime.strptime(text_temp[18:44], "%Y-%m-%d %H:%M:%S.%f")))
    
#do same thing again but only to get timestamps when cat is present
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
   
if plot_history == 1:    
    fig, ax = plt.subplots()
    ax.plot_date(time_data_dt, cat_status)
    ax.xaxis.set_major_locator(DayLocator())
    ax.xaxis.set_minor_locator(HourLocator(arange(0, 25, 6)))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax.fmt_xdata = DateFormatter('%Y-%m-%d %H:%M:%S')
    fig.autofmt_xdate()
    plt.title("Historical cat occupancy in yurt")
    plt.ylabel("Cat status")
    plt.xlabel("Date")
    fig.savefig('historical_cat_yurt_status.png')
    

#try a histogram to see which days are most popular
end = datetime.date(2017,7,4) 
start = datetime.date(2017,6,28) 
one_day = datetime.timedelta(days = 1)  

week = [] 
for i in range((end-start).days+1):  
    week.append(start + (i)*one_day)

numweek = date2num(week)

b=plt.figure(2)
plt.hist(cat_present_dt, bins = numweek, ec="k")
plt.gcf().autofmt_xdate()
plt.title("Cat present tweets per day")
plt.ylabel("Number of cat present tweets")
plt.xlabel("Date")
b.savefig('yurt_tweets_per_day.png')

#now plot histogram of which times are most popular
c=plt.figure(3)
plt.hist(cat_present_hour,bins=24)
plt.xlabel("Time (hour)")
plt.ylabel("Number of cat present tweets")
plt.title("Popular times to be in yurt")
c.savefig('popular_yurt_times.png')


#only call this at the end
plt.show()
#must call to keep all plots open
input()
	
	
	
	
