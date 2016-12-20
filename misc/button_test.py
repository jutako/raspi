

import RPi.GPIO as GPIO
from time import sleep

PIN = 5

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN, GPIO.IN)

while True:
    if (GPIO.input(PIN)):
        print("pin True.")
    else:
        print("pin False.")
    sleep(1)
