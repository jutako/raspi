#!/usr/bin/env python
#
# GrovePi Example for using the Grove Moisture Sensor (http://www.seeedstudio.com/wiki/Grove_-_Moisture_sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#

'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''



import time
import math #for dht sensor
import grovepi #for general grovepi
import SI1145 #for I2C sunlight sensor
import raspitools as rpit #my own set of tools

THINGSPEAKKEY = '8QQ12B7Q5YSZ355T' #channel: "kasvuboksi"
THINGSPEAKURL = 'https://api.thingspeak.com/update'
LOGINTERVAL = 60 #in seconds

# Connect the Grove Moisture Sensor to analog port A0
# SIG,NC,VCC,GND
PORT_MOISTURE_1 = 0
PORT_MOISTURE_2 = 1


sunlight_i2c = SI1145.SI1145()
# Default constructor will pick a default I2C bus.
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.


# Connect the Grove Temperature & Humidity Sensor Pro to digital port D4
# This example uses the blue colored sensor.
# SIG,NC,VCC,GND
PORT_DHT = 5  # The Sensor goes on digital port
# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
DHT_TYPE = 1 # 0 -> blue colored sensor, 1 -> white colored sensor


PORT_RELAY_1 = 3
grovepi.pinMode(PORT_RELAY_1, "OUTPUT")


time_since_last_log = 0;
while True:
    try:




        # I2C sunlight sensor
        # NOTE:
        # 	The wiki suggests the following sensor values:
        # 		Min  Typ  Max  Condition
        # 		0    0    0    sensor in open air
        # 		0    20   300  sensor in dry soil
        # 		300  580  700  sensor in humid soil
        # 		700  940  950  sensor in water
            
        # 	Sensor values observer: 
        # 		Val  Condition
        # 		0    sensor in open air
        # 		18   sensor in dry soil
        # 		425  sensor in humid soil
        # 		690  sensor in water
        vis = sunlight_i2c.readVisible()
        IR = sunlight_i2c.readIR()
        UV = sunlight_i2c.readUV()
        uvIndex = UV / 100.0
        print('Vis:             ' + str(vis))
        print('IR:              ' + str(IR))
        print('UV Index:        ' + str(uvIndex))
        print('')

        # Analog moisture sensors x2
        moisture_1 = grovepi.analogRead(PORT_MOISTURE_1)
        moisture_2 = grovepi.analogRead(PORT_MOISTURE_2)
        print('Moisture at A0: ' + str(moisture_1) + '\n')
        print('Moisture at A1: ' + str(moisture_2) + '\n')


        # This example uses the blue colored sensor. 
        # The first parameter is the port, the second parameter is the type of sensor.
        [temp,humidity] = grovepi.dht(PORT_DHT, DHT_TYPE)
        # Reading dht messes up moisture readings, tried many ports. Works better if moisture is read first. Maybe sleeping time helps as well.
        if math.isnan(temp) == False and math.isnan(humidity) == False:
            print("temperature: %.02f C, humidity: %.02f%%\n" % (temp, humidity))

        # Relay
        # switch on for 5 seconds
        if temp > 23:
            grovepi.digitalWrite(PORT_RELAY_1, 1)
            relay_state = 1;
            print ("relay: on")

        else:
            # switch off for 5 seconds
            grovepi.digitalWrite(PORT_RELAY_1, 0)
            relay_state = 0;
            print ("relay: off")

        if time_since_last_log > LOGINTERVAL:
            value_dict = {'field1': temp, 'field2': humidity, 'field3': vis , 'field4':  IR, 'field5': moisture_1, 'field6': moisture_2, 'field7': relay_state, 'field8': 999}
            rpit.sendData(THINGSPEAKURL, THINGSPEAKKEY, value_dict)
            time_since_last_log = 0;

        print('#############################################')
        time.sleep(3)
        time_since_last_log = time_since_last_log + 3;

    except KeyboardInterrupt:
        break

    except:
        exctype, value = sys.exc_info()[:2]
        log = 'Loop error: ' + str(value)
        print(log)
