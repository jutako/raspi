#!/usr/bin/python

import RPi.GPIO as GPIO
import time

PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)

while True:
    time.sleep(0.5)
    if (GPIO.input(PIN)):
        print("PIN up...")   
    else:
        print("PIN down...")

    
