#! python

from twython import Twython

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

#now that we have loaded the twitter info, need to decide how to handle force sensor signal
#let's assume we have a value called force_signal
force_signal=8

#let's assume we have set a threshold value for the force sensor
force_threshold=10

if force_signal > force_threshold:
	cat_status=1
	message="There is a cat in the yurt! (test)"
elif force_signal <= force_threshold:
	cat_status=0
	message="Sorry, the cats are somewhere else (test)"

#message = "Hello world!"
twitter.update_status(status=message)
print("Tweeted: %s" % message)