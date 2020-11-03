import Adafruit_DHT
import time
 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 23
csvFile = open ( "dht11values.csv" , "a" ) 
while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        #print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
        csvFile. write ( '{0: 0.1f} * C; {1: 0.1f}%' . format ( temperature, humidity ))
        csvFile. write ( '\ n' )
    else:
        print("Sensor failure. Check wiring.");
try :
        while True : 
                readDht11Values ()
                time. sleep ( 2 )
except KeyboardInterrupt:
        csvFile. close ()
        passport
