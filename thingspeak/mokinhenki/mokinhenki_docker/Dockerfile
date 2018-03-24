FROM resin/raspberrypi3-python:2.7
#remember to load an image that is for raspberry pi and arm!

COPY requirements.txt /app/
COPY mokinhenki.py /app/
COPY google_app_token /app/
COPY dbx_accesstoken_mokinhenki /app/
COPY Adafruit_Python_DHT /app/Adafruit_Python_DHT/

WORKDIR /app

#RUN pip install numpy
# RUN pip install Adafruit_Python_DHT # does not work
#RUN pip install RPi.GPIO
#RUN pip install picamera
#RUN pip install dropbox

RUN pip install -r requirements.txt

# RUN apt install build-essential python-dev python-openssl
RUN cd Adafruit_Python_DHT && python setup.py install

ENTRYPOINT ["python"]

CMD ["mokinhenki.py"]
