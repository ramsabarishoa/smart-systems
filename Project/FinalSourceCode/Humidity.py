#Import relevant library modules
import Adafruit_DHT
import paho.mqtt.publish as publish

#Publish teh humidity values to teh parser file
while True: 
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 8) 
    print(humidity)
    publish.single("Humidity",humidity, hostname="test.mosquitto.org",)
