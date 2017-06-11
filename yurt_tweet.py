#! python

from twython import Twython
import time

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

#just do this continuously
counter=0
while True:
	counter=counter+1
	#call read_force_sensor program (read_force_sensor.py)
	#should return value called force_signal
	read_force_sensor.get_force_signal()
	#test_force.test_value()

	#let's assume we have a value called force_signal
	force_signal=8

	#let's assume we have set a threshold value for the force sensor
	force_threshold=10
	
	if force_signal > force_threshold:
		cat_status=1
		message="There is a cat in the yurt! (test)"
	elif force_signal <= force_threshold:
		cat_status=0
		message="(test %s)" % counter

	twitter.update_status(status=message)
	print("Tweeted: %s" % message)

	# check every 30 s
	time.sleep(30)