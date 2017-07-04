#! python

# yurt_report project, written 2017 by LS
# this script designed to download the twitter data in json format, parse it, and process it in a basic way (more exciting analysis coming soon!)

import json

from yurt_download import download_yurt_tweets

#just test that the basic functionality works first
#download_yurt_tweets()

#now reassemble the data line by line, the same way we wrote teh file
data = []
with open('saved_yurt_tweets.json') as f:
    for line in f:
        data.append(json.loads(line))

text_data=[]		
for i in range(0,len(data)):	
    text_data.append(data[i]["text"])
	
print(text_data)