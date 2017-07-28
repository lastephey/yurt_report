#! python

# yurt_report project, written 2017 by LS
# parts based heavily on code provided by adafruit, written by limor fried
# master program which calls read_force_sensor.py, which reads the value and reports back
# then, based on a threshold, decides whether a cat is present or not
# performs this check every 5 mins, updates twitter account @yurt_report


import time
import os
import RPi.GPIO as GPIO
import datetime
import tweepy
from tweepy import OAuthHandler


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

import read_force_sensor

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k trim pot connected to adc #0
potentiometer_adc = 0;

while True:

        # read the analog pin
        trim_pot = read_force_sensor.readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

        set_volume = trim_pot / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
        set_volume = round(set_volume)          # round out decimal value
        set_volume = int(set_volume)            # cast volume as integer

        # change variable names
        force_signal=set_volume 

        #let's set a threshold value for the force sensor
		#with basket, now reads about 35 percent empty
		#should read over 40 percent with cat
        force_threshold=40

        # get system time for timestamp on tweet to avoid duplicates
        now=datetime.datetime.now()
	
        if force_signal > force_threshold:
                cat_status=1
                message="There is a cat :) %s Force sensor at %s percent" %(now,force_signal) 
           
        elif force_signal <= force_threshold:
                cat_status=0
                message="Sorry, no cats :( %s Force sensor at %s percent" %(now,force_signal) 
        
        #have encountered errors several times now (the 503 error), need to make yurt_report robust to these		
        try:
             api.update_status(status=message)
             print("Tweeted: %s" % message)
        #try to improve our error handling     
        #make sure we use tweepy, not twython!
        except api.TweepError as e:
             print("We encountered a general error")
             print(e)
        except api.RateLimitError as e:
             print("We encountered a rate limit error")
             print(e)
  
		


	# check every 300 s
        time.sleep(300)
