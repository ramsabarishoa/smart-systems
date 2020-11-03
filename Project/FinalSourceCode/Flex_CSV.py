# MQTT Client connection for flex values
import paho.mqtt.client as mqtt
import time
import csv
import sys

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("flex_values")
csvfile = "flex.csv" 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
   # print(msg.topic+" "+str(msg.payload))  
    a = str(msg.payload.decode('utf-8'))
    timeC = time.strftime("%H")+':' +time.strftime("%M")+':'+time.strftime("%S")
    data = [a,timeC]
    with open(csvfile, "a")as output:
       writer = csv.writer(output, delimiter=",", lineterminator = '\n')
       writer.writerow(data)
       time.sleep(2) # update script every 60 second

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org", 1883)

client.loop_forever()
