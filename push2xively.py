#!/usr/bin/python
""" 
This program reads off a jeelink on /dev/ttyUSB0 
which is sending data like "2580 7183 16132".
We divide that by 100 to get humidity, temperature in celsius, and temperature in fahrenheit
and then send it to Xively 
"""

import serial # Load pyserial, for the jeelink
import xively # Load the xively library
import time # So we can wait

# Insert your API key and feed ID from Xively in the line below
APIkey = "YOUR_API_KEY"
feedID = FEED_ID_OF_DEVICE # an integer

# Open the serial port at 57600
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=3)

def main():
    # Define our streams
    streamnames = "humidity","tempC","tempF"
    # Set up a feed object
    feed = xively_setup(APIkey,feedID)
    # Make some streams
    streams = makestreams(feed,streamnames)
    while True:
        # Push those streams
        updatesensors(feed,streams)
        # Take a short nap, don't want to overwhelm anyone
        time.sleep(30)

def xively_setup(API_key,feed_ID):
    """ Takes an API key, found on your device's website, returns a feed object """
    api = xively.XivelyAPIClient(API_key)
    feed = api.feeds.get(feed_ID)
    return feed

def readsensors():
    """ 
    Split our data into an array, 
    "2580 7183 16132" becomes [2580, 7183, 1613]
    Make sure it isn't the first line ("Reading sensors...")
    """
    data = ser.readline().split()
    return [round(datum/100.00, -2) for datum in map(int,data)] if len(data) == 3 else None

def makestreams(feed,streams):
    stream_objects = []
    for stream in streams:
        if not checkstream(feed,stream):
            stream_objects.append(feed.datastreams.create(id=stream))
        else:
            stream_objects.append(feed.datastreams.get(stream))
    return stream_objects

def checkstream(feed,stream):
    return stream in str([i for i in feed.datastreams.list()])

def updatesensors(feed,streams):
    data = []
    # Update the data based on the serial port output
    while not data:
        data = readsensors()
    # Loop over the streams, set each one's current value to the data from readsensors,
    # then update the value (divided by 100-- that's how we're doing floats)
    for stream in xrange(len(streams)):
	    streams[stream].current_value = data[stream]
            streams[stream].update(fields=['current_value'])
    return 0

if __name__ == "__main__":
    main()
