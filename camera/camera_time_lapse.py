from picamera import PiCamera
from time import sleep
import time
import datetime

camera = PiCamera()
camera.rotation = 180
camera.resolution =  (1024, 576)
camera.exposure_mode = 'night'

#camera.start_preview()
#sleep(20)
#camera.stop_preview()

while True:
    camera.start_preview()

    sleep(2)

    ts = time.time()
    tstr = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
    fname = "/home/pi/figs/image_%s.jpg" % (tstr)

    camera.capture(fname)
    camera.stop_preview()
    print('Took picture at %s. going to sleep for 30 secs...' % (tstr))
    sleep(30)
