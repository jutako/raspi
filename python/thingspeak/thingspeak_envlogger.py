#!/usr/bin/python

# Modified from:

#--------------------------------------
#    ___  ___  _ ____
#   / _ \/ _ \(_) __/__  __ __
#  / , _/ ___/ /\ \/ _ \/ // /
# /_/|_/_/  /_/___/ .__/\_, /
#                /_/   /___/
#
#           Temperature Logger
#  Read data from a BMP180 sensor and
#  send to Thingspeak.com account.
#
# Author : Matt Hawkins
# Date   : 20/06/2015
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

#import smbus
import time
import os
import sys
import urllib            # URL functions
import urllib2           # URL functions
import random #for testing
import grovepi #for Grove sensors

################# Default Constants #################
# These can be changed if required
AUTOSHUTDOWN  = 1    # Set to 1 to shutdown on switch
THINGSPEAKKEY = 'VEHKJKJXTZBYLMVC'
THINGSPEAKURL = 'https://api.thingspeak.com/update'
LOGFILE = '/home/pi/log/thingspeak_envlogger.txt'
#####################################################

"""
def switchCallback(channel):

    global AUTOSHUTDOWN

    # Called if switch is pressed
    if AUTOSHUTDOWN==1:
        os.system('/sbin/shutdown -h now')
        sys.exit(0)
"""

def sendData(url,key,temp,hum):
    """
    Send event to internet site
    """
    
    global LOGFILE

    values = {'api_key' : key, 'field1' : temp, 'field2' : hum}

    postdata = urllib.urlencode(values)
    req = urllib2.Request(url, postdata)

    log = time.strftime("%d-%m-%Y,%H:%M:%S") + ","
    log = log + "{:.1f}C".format(temp) + ","
    log = log + "{:.2f}%".format(hum) + ","

    try:
        # Send data to Thingspeak
        response = urllib2.urlopen(req, None, 5)
        html_string = response.read()
        response.close()
        log = log + 'Update ' + html_string

    except urllib2.HTTPError, e:
        log = log + 'Server could not fulfill the request. Error code: ' + str(e.code)
        
        """
        Traceback (most recent call last):
		  File "thingspeak_test.py", line 146, in <module>
			main()
		  File "thingspeak_test.py", line 131, in main
			sendData(THINGSPEAKURL,THINGSPEAKKEY,temp,hum)
		  File "thingspeak_test.py", line 73, in sendData
			log = log + 'Server could not fulfill the request. Error code: ' + e.code
		TypeError: cannot concatenate 'str' and 'int' objects
        """
        
    except urllib2.URLError, e:
        log = log + 'Failed to reach server. Reason: ' + str(e.reason)
        """
        TODO: Find a way to avoid this: 
        
        Traceback (most recent call last):
		File "thingspeak_envlogger.py", line 153, in <module>
		main()
		File "thingspeak_envlogger.py", line 137, in main
		sendData(THINGSPEAKURL,THINGSPEAKKEY,temp,hum)
		File "thingspeak_envlogger.py", line 76, in sendData
		log = log + 'Failed to reach server. Reason: ' + e.reason
		TypeError: cannot concatenate 'str' and 'gaierror' objects
		"""
        
    except:
        log = log + 'Unknown error'

    print log
    
    with open(LOGFILE, 'a') as file:
		file.write(log + '\n')

def main():

    global THINGSPEAKKEY
    global THINGSPEAKURL

    while True:
        
        [temp, hum] = grovepi.dht(4, 1) #D4 input, the white version  
        print("temp = %.02f C humidity =%.02f%%"%(temp, hum))        
        
        if (-40 < temp) & (temp < 50) & (0 < hum) & (hum < 100):
			sendData(THINGSPEAKURL,THINGSPEAKKEY,temp,hum)
			sys.stdout.flush()
		
        time.sleep(60)


if __name__=="__main__":
    main()
