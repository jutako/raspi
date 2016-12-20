from picamera import PiCamera
from time import sleep
import time
import datetime

camera = PiCamera()
camera.rotation = 180

#camera.start_preview()
#sleep(30)
#camera.stop_preview()



### still images
camera.start_preview()

sleep(2)

ts = time.time()
tstr = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
fname = "/home/pi/figs/image_%s.jpg" % (tstr)

camera.capture(fname)
camera.stop_preview()
