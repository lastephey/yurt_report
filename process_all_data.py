#! python

# yurt_report project, written 2017 by LS
# use this after running download_data.py, which currently has to be run manually and will save the most recent 3k tweets

import glob
import json
import matplotlib.pyplot as plt
from matplotlib.pyplot import hist
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, date2num, num2date
import numpy as np
from numpy import arange
import time
import datetime


#find all saved tweets in current directory
tweet_files=glob.glob('saved_tweets_*.json')

data=[]
#for each entry in tweet_files, load the data and continue to append it to the same list
for i in range(0,len(tweet_files)):
    fileopen=tweet_files[i]
    print(fileopen)
    
    #now reassemble the data line by line, the same way we wrote the file
    with open(fileopen) as f:
        for line in f:
             data.append(json.loads(line))
        f.close()     
          
#pull out only the text data
text_data=[]
for i in range(0,len(data)):	
    text_data.append(data[i]["text"])
      
text_data_unique=[]  
#probably a lot of duplicates here, need to remove them
for i in text_data:
  if i not in text_data_unique:
    text_data_unique.append(i)

#now we need to parse the data and pull out the parts to use!
#need timestamp and yurt status
#first just create plot of timestamp vs yurt status (0 or 1)
#need to sort which tweets we can actually use for analysis (exclude images and other tweets)
analysis_array=[]
cat_status=[]
cat_present=[]
for i in range(0,len(text_data_unique)):
    #need to exclude old data which doesn't have the right structure
    if "Force" not in text_data_unique[i]:
        break
    elif "There" in text_data_unique[i]:
        cat_status.append(1)
        analysis_array.append(i)
        cat_present.append(i)
    elif "Sorry" in text_data_unique[i]:
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
    text_temp=text_data_unique[j]	
    #this writes a list
    cat_present_list.append(text_temp[18:44])
    #this converts to datetime objects
    cat_present_dt.append((datetime.datetime.strptime(text_temp[18:44], "%Y-%m-%d %H:%M:%S.%f")))    
    #also keep track of which hours cats are present, this is equally ugly
    cat_present_hour.append(int(text_temp[29:31]))
       
print(cat_present_hour)    
print(len(cat_present_hour))   

#now plot histogram of which times are most popular
if len(cat_present_hour) >= 1:
    c=plt.figure(3)
    ax1=plt.subplot()
    plt.hist(cat_present_hour,bins=24,width=1)
    plt.xlabel("Time (hour)")
    plt.ylabel("Number of cat present tweets")
    plt.title("Popular times to be in yurt")
    ax1.set_xlim([0,24])
    #c.savefig('popular_yurt_times.png')
    plt.show()
    

