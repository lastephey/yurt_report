#! python

from twython import Twython
import time
import os
import RPi.GPIO as GPIO


from auth import (
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
)

import read_force_sensor
#import test_force

twitter = Twython(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
)

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

#just do this continuously
counter=0

while True:
        counter=counter+1

        # read the analog pin
        trim_pot = read_force_sensor.readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

        set_volume = trim_pot / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
        set_volume = round(set_volume)          # round out decimal value
        set_volume = int(set_volume)            # cast volume as integer

        # change variable names
        force_signal=set_volume

        # print('Force=%s' %force_signal)
 

        #let's set a threshold value for the force sensor
        force_threshold=50
	
        if force_signal > force_threshold:
                cat_status=1
                message="force sensor above threshold (test %s)" %counter
           
        elif force_signal <= force_threshold:
                cat_status=0
                message="force sensor below threshold (test %s)" % counter
               

        twitter.update_status(status=message)
        print("Tweeted: %s" % message)

	# check every 60 s
        time.sleep(60)
