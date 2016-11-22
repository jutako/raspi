
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import time
import datetime

PIN = 5


GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)
camera = PiCamera()

#camera.start_preview()
#sleep(20)
#camera.stop_preview()


while True:
    #print("waiting...")
    if (GPIO.input(PIN)):
        print("Taking a picture...")
        camera.start_preview()
        
        sleep(2)
        
        ts = time.time()
        tstr = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
        fname = "/home/pi/figs/image_%s.jpg" % (tstr)
        
        camera.capture(fname)
        camera.stop_preview()
