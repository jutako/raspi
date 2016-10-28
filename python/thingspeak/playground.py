


temp = 10
hum = 20
key = 'VEHKJKJXTZBYLMVC'

import urllib
values = {'api_key' : key, 'field1' : temp, 'field2' : hum}

postdata = urllib.urlencode(values)
