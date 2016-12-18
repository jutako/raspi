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
#--------------------------------------

# TODO:
# * print to log and save log to cloud
# * save pictures to cloud

#import smbus
import time
import datetime
import os
import sys
import urllib            # URL functions
import urllib2           # URL functions
import random #for testing
#import grovepi #for Grove sensors
import Adafruit_DHT #for DHT11 and DHT22 sensors
import RPi.GPIO as GPIO #for PIR pin read
from picamera import PiCamera #for camera 



################# Default Constants #################
# These can be changed if required
OUTPATH = '/home/pi/data/mokinhenki'
OUTPATH_FIG = os.path.join(OUTPATH, 'figs')
LOGFILE = os.path.join(OUTPATH, 'log_mokinhenki.txt')

AUTOSHUTDOWN  = 1    # Set to 1 to shutdown on switch
THINGSPEAKKEY = 'WUKJPVAXWTTYQTFM' #channel: ""
THINGSPEAKURL = 'https://api.thingspeak.com/update'

PIN_PIR = 12 #PIR detector data GPIO pin

DHT_SENSOR = 22 #DHT 11 sensor submodel
PIN_DHT22 = 16 #DHT sensor data GPIO pin
TEMPHUM_INTERVAL_SEC = 30 #how often measurement values are read and sent to thingspeak
#####################################################



"""
def switchCallback(channel):

    global AUTOSHUTDOWN

    # Called if switch is pressed
    if AUTOSHUTDOWN==1:
        os.system('/sbin/shutdown -h now')
        sys.exit(0)
"""

def sendData(url, key, temp, hum):
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

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_PIR, GPIO.IN)

    camera = PiCamera()
    camera.rotation = 180
    camera.resolution =  (1024, 576)
    day_pic_taken = False

    #camera.start_preview()
    #sleep(20)
    #camera.stop_preview()

    # initialize
    last_temphum_ts = time.time()
    hum2 = 0
    temp2 = -100

    while True:

        # Take picture based on PIR
        if (GPIO.input(PIN_PIR)):
            #print("Taking a picture...")
            #camera.start_preview()
            
            time.sleep(0.2) #wait for the object to move fully into frame
            
            ts = time.time()
            tstr = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
            fname = os.path.join(OUTPATH_FIG, "pirimage_%s.jpg" % (tstr))
            
            camera.capture(fname)
            time.sleep(3) #sleep until PIR is ready again
            #camera.stop_preview()


        # Take picture based on time of day
        curts = time.localtime()
        if (curts[3]==12) & (curts[4]==0) & (day_pic_taken != True):
            ts = time.time()
            tstr = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
            fname = os.path.join(OUTPATH_FIG, "dayimage_%s.jpg" % (tstr))
            camera.capture(fname)
            day_pic_taken = True

        if (curts[3]==12) & (curts[4]==1):
            day_pic_taken = False #reset flag
        
        
        # Log temperature and humidity
        if (time.time() - last_temphum_ts) > TEMPHUM_INTERVAL_SEC:
            
            #[temp, hum] = grovepi.dht(4, 1) #D4 input, the white version          
            
            # Try to grab a sensor reading.  Use the read_retry method which will retry up
            # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
            hum2_old = hum2
            temp2_old = temp2
            hum2, temp2 = Adafruit_DHT.read_retry(DHT_SENSOR, PIN_DHT22)
                
            # Note that sometimes you won't get a reading and
            # the results will be null (because Linux can't
            # guarantee the timing of calls to read the sensor).
            # If this happens try again!
            if hum2 is None or temp2 is None:
                hum2 = hum2_old
                temp2 = temp2_old
            
            if all(x is not None for x in [temp2, hum2]) & (-40 < temp2) & (temp2 < 50) & (0 < hum2) & (hum2 < 100):
                            print("temp = %.02f C humidity =%.02f%%"%(temp2, hum2))
                            sendData(THINGSPEAKURL, THINGSPEAKKEY, temp2, hum2)
                            sys.stdout.flush()
                            last_temphum_ts = time.time()


   
	
        time.sleep(0.5) #for the while loop


if __name__=="__main__":
    main()




