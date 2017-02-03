#!/usr/bin/env python

from datetime import datetime
import requests
import time

flickerstripIp = "http://192.168.0.119"; #Adjust this to the correct IP address of your Flickerstrip

timeSlots = [5,6,6]; #This represents the number of binary digits we want to allocate to each segment hours. minutes and seconds respectively

while True:
    now = datetime.now();
    currentTime = [now.hour,now.minute,now.second]; #This array is parallel to timeSlots and holds the current time in hours, minutes, and seconds
    pixels = [];
    for i in range(len(timeSlots)):
        binarySlot = format(currentTime[i],"0"+str(timeSlots[i])+"b"); #Format the value for this slot as a binary string with the length from timeSlots

        if (i != 0): pixels += [255,0,0]; #We'll start with a green pixel to make the clock more readable except for the first slot

        for b in binarySlot: #Now we'll iterate through the binary representation character by character and output a "byte" array for the pixels
            if (b == "1"):
                pixels += [255,255,255]; # Full white for the 1s
            else:
                pixels += [0,0,0]; # Off for the 0s

    pixels += [0,0,255]; #Triple blue to terminate it
    pixels += [0,0,255];
    pixels += [0,0,255];

    binaryString = ''.join([chr(item) for item in pixels]) #Convert the pixel array into a binary string

    #POST the pixeldata to the strip, note that we're using the preview option which prevents the pattern from being saved permanently
    url = "%s/pattern/create?name=Clock&fps=1&frames=1&pixels=%d&preview" % (flickerstripIp,len(pixels));
    requests.post(url,data=binaryString);

    time.sleep(1) #Delay a second before running the loop again, this could be improved by waiting until the second rolls over
