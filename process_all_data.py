#! python

# yurt_report project, written 2017 by LS
# use this after running download_data.py, which currently has to be run manually and will save the most recent 3k tweets
# will use all availble data for analysis

import glob
import json
import matplotlib.pyplot as plt
from matplotlib.pyplot import hist
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, date2num, num2date
import numpy as np
from numpy import arange
import time
import datetime
import os


#find all saved tweets in current directory
tweet_files=glob.glob('saved_tweets_*.json')
print(tweet_files)

data = []
text_data=[]
for i in range(0,len(tweet_files)):
    fileopen=tweet_files[i]
    print(fileopen)
    with open(fileopen) as f:
        for line in f:
            data.append(json.loads(line))

    for i in range(0,len(data)):	
        text_data.append(data[i]["text"])
  
#test file looks okay  

      
text_data_unique=[]  
#probably a lot of duplicates here, need to remove them
for line in text_data:
  if line not in text_data_unique:
    text_data_unique.append(line)
    
#see what we got, save text_data to a file
testfile = open('test.txt', 'w', encoding="utf-8")
for item in text_data_unique:
    testfile.write("%s\n" % item)       
 
print("Number of unique tweets: %s" % len(text_data_unique))    

#now we need to parse the data and pull out the parts to use!
#need timestamp and yurt status
#first just create plot of timestamp vs yurt status (0 or 1)
#need to sort which tweets we can actually use for analysis (exclude images and other tweets)
analysis_array=[]
cat_status=[]
yes_list=["There","Force"]
no_list=["Sorry","Force"]
cat_present=[]
for i in range(0,len(text_data_unique)):
    #need to exclude old data which doesn't have the right structure
    if all(x in text_data_unique[i] for x in yes_list):
        cat_status.append(1)
        cat_present.append(i)
    elif all(x in text_data_unique[i] for x in no_list):
        cat_status.append(0)
    else:
        continue
        
occupancy_rate=100*np.mean(cat_status)  
print("Yurt occupancy rate is %s percent" %occupancy_rate) 
        
#get timestamps when cat is present
cat_present_dt=[]	
cat_present_list=[]
cat_present_hour=[]
cat_present_day=[]
for i in range(0,len(cat_present)):
    j=cat_present[i]
    text_temp=text_data_unique[j]     
    #this writes a list
    cat_present_list.append(text_temp[18:44])
    #this converts to datetime objects
    cat_present_dt.append((datetime.datetime.strptime(text_temp[18:44], "%Y-%m-%d %H:%M:%S.%f")))    
    #also keep track of which hours cats are present, this is equally ugly
    cat_present_hour.append(int(text_temp[29:31]))
    cat_present_day.append((datetime.datetime.strptime(text_temp[18:28], "%Y-%m-%d")))

#print(cat_present_dt)    
    
#try plotting number of tweets vs cat occupancy
a=plt.figure(1)
plt.plot(cat_status)
plt.xlabel('Tweet number')
plt.ylabel('Yurt occupancy')
plt.title('Historical yurt occupancy')
#plt.savefig("test.png")    

#try plotting date vs cat occupancy
b=plt.figure(2)
plt.hist(cat_present_dt)
plt.xlabel('Date')
plt.ylabel('Number of cat present tweets')
plt.title('Historical yurt occupancy')
#plt.savefig("test.png")    
       
#now plot histogram of which times are most popular
c=plt.figure(3)
ax1=plt.subplot()
plt.hist(cat_present_hour,bins=24,width=1)
plt.xlabel("Time (hour)")
plt.ylabel("Number of cat present tweets")
plt.title("Popular times to be in yurt")
ax1.set_xlim([0,24])
#c.savefig('popular_yurt_times.png')
plt.show()
    
#try finding average duration of stay

#try comparing peak yurt times to sunrise

#average occupancy rate per day



