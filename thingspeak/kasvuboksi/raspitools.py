#!/usr/bin/python
# -*- coding: utf-8 -*-

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
# * make log machine readable
# * make a more verbose human readable log as well
# * save pictures and log to cloud

#import smbus
import time
import datetime
import os
import sys
import glob #to get lists of files etc.
import urllib            # URL functions
import urllib2           # URL functions
import random #for testing
import numpy as np #for simple computations such as median

# Modules for building email
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib #for sending email

#import grovepi #for Grove sensors
import Adafruit_DHT #for DHT11 and DHT22 sensors
import RPi.GPIO as GPIO #for PIR pin read
from picamera import PiCamera #for camera 



################# Default Constants #################
# These can be changed if required
#OUTPATH = '/home/pi/data/mokinhenki'
#OUTPATH_FIG = os.path.join(OUTPATH, 'figs')
#LOGFILE = os.path.join(OUTPATH, 'log_mokinhenki.txt')

#from_email = 'jussitapiokorpela@gmail.com' #seems to make no difference what this is...
#to_email = ['jussikorpela@hotmail.com']
#app_token_file = '/home/pi/private/google_app_token'

#TEMP_ALARM_TH = -20
#HUM_ALARM_TH = 100

#AUTOSHUTDOWN  = 1    # Set to 1 to shutdown on switch
#THINGSPEAKKEY = 'WUKJPVAXWTTYQTFM' #channel: ""
#THINGSPEAKURL = 'https://api.thingspeak.com/update'



"""
def switchCallback(channel):

    global AUTOSHUTDOWN

    # Called if switch is pressed
    if AUTOSHUTDOWN==1:
        os.system('/sbin/shutdown -h now')
        sys.exit(0)
"""

# value_dict = {'field1' : temp, 'field2' : hum}
def sendData(url, api_key, value_dict):
    """
    Send event to internet site
    """

    value_dict['api_key'] = api_key
    postdata = urllib.urlencode(value_dict)
    req = urllib2.Request(url, postdata)

    log = time.strftime("%d-%m-%Y,%H:%M:%S")

    try:
        # Send data to Thingspeak
        response = urllib2.urlopen(req, None, 5)
        html_string = response.read()
        response.close()
        log = log + ' update ' + html_string
        
    except:
        log = log + 'sendData error. Reason: ' + sys.exc_info()[0]

    return log


""" Create a multipart MIME message that can hold both text and images. """
def createMultipartEMail(from_email, to_email, subjectline, message):
    msg = MIMEMultipart()
    msg['Subject'] = subjectline
    msg['From'] = from_email
    msg['To'] = ",".join(to_email)
    #msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(message))
    return msg


""" Sends email using smtp.gmail.com. Authentication needs an App token since I use two-factor authentication. 
    App token needs to be provided, since I do not dare to hard code it into this public code."""
def sendGMail(msg, google_app_token):
    status = [None] * 2
    log = time.strftime("%d-%m-%Y,%H:%M:%S") 
    global LOGFILE

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        status[0] = server.login('jussitapiokorpela@gmail.com', google_app_token)
        status[1] = server.sendmail(msg['from'], msg['to'], msg.as_string())
        server.quit()
        log = log + 'Send mail notification.'
    
    except:
        log = log + 'sendData error. Reason: ' + sys.exc_info()[0]

    print log
    with open(LOGFILE, 'a') as file:
	    file.write(log + '\n')

    return status


"""
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
    hum = 0
    temp = -100
    last_temphum_email_ts = time.time()
    hum_hist = [HUM_ALARM_TH - 1] * 5
    temp_hist = [TEMP_ALARM_TH + 1] * 5

    # Load google app token from file
    fp = open(app_token_file, 'r')
    app_token = fp.readline()
    app_token = app_token[0:-1] #remove \n
    fp.close()

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

            # Create email
            msg = createMultipartEMail(from_email, to_email,
                    'Mokinhenki tiedottaa: liiketunnistin lauennut',
                    'Liiketunnistimeni laukesi. Ohessa kuva.')
            
            # Attach image
            fp = open(fname, 'rb')
            img = MIMEImage(fp.read())
            fp.close()
            msg.attach(img)

            # Send using gmail
            status = sendGMail(msg, app_token)

            #time.sleep(3) #sleep until PIR is ready again
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
            hum_old = hum
            temp_old = temp
            hum, temp = Adafruit_DHT.read_retry(DHT_SENSOR, PIN_DHT22)
                
            # Note that sometimes you won't get a reading and
            # the results will be null (because Linux can't
            # guarantee the timing of calls to read the sensor).
            # If this happens try again!
            if hum is None or temp is None:
                hum = hum_old
                temp = temp_old
            
            if all(x is not None for x in [temp, hum]) & (-40 < temp) & (temp < 50) & (0 < hum) & (hum < 100):
                            print("temp = %.02f C humidity =%.02f%%"%(temp, hum))
                            sendData(THINGSPEAKURL, THINGSPEAKKEY, temp, hum)
                            sys.stdout.flush()

                            # update history records: pop last element and add new to position 0
                            temp_hist.pop()
                            temp_hist.insert(0, temp)
                            hum_hist.pop()
                            hum_hist.insert(0, hum)

                            # send email warning
                            if ((np.median(temp_hist) < TEMP_ALARM_TH) | (np.median(hum_hist) > HUM_ALARM_TH)) & ((time.time() - last_temphum_email_ts) > TEMPHUM_ALARM_INTERVAL_SEC):
                                msg = createMultipartEMail(from_email, to_email,
                                'Mokinhenki tiedottaa: liian kylmaa tai kosteaa',
                                'Majassani on liian kylmaa tai kosteaa. Lampotila on %2.1f astetta ja suht. kosteus %2.1f prosenttia. Tee jotain.' % (temp, hum) )
                                status = sendGMail(msg, app_token)
                                last_temphum_email_ts = time.time()

                            last_temphum_ts = time.time()


        time.sleep(0.5) #for the while loop


if __name__=="__main__":
    main()
"""



