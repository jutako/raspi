#!/usr/bin/python

import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import datetime

PIN = 12


GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)

camera = PiCamera()
camera.rotation = 180
camera.resolution =  (1024, 576)

#camera.start_preview()
#sleep(20)
#camera.stop_preview()


while True:
    time.sleep(0.5)
    #print("waiting...")
    if (GPIO.input(PIN)):
        print("Taking a picture...")
        #camera.start_preview()
        
        time.sleep(0.2)
        
        ts = time.time()
        tstr = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
        fname = "/home/pi/figs/image_%s.jpg" % (tstr)
        
        camera.capture(fname)
        time.sleep(3)
        #camera.stop_preview()

    else:
        print("PIN down...")

    
