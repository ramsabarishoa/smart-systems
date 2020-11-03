import paho.mqtt.client as mqtt # MQTT Client
from datetime import datetime
import time
import csv
import sys

# Establishing MQTT client connection
def on_connect(client, userdata, flags, rc):
    print("Collecting EAR Values "+str(rc))
    client.subscribe("EAR_Values") #Subscribe to EAR_values topic
csvfile = "ear.csv" 
def on_message(client, userdata, msg): 
    EAR = msg.payload.decode() #message payload
    timeC = time.strftime("%H")+':' +time.strftime("%M")+':'+time.strftime("%S")
    data = [EAR,timeC] #data consisting of ear values and time
    with open(csvfile, "a")as output: #open the csv file in append mode
        writer = csv.writer(output, delimiter=",", lineterminator = '\n') #Data is written in a row column format
        writer.writerow(data)
        time.sleep(2) # update the script 

            
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org", 1883)
client.loop_forever()
