#Import relevant library modules
import os
import paho.mqtt.client as mqtt 
import sys
import time
import RPi.GPIO as GPIO

#Initiatlise GPIO port settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setwarnings(False)

#Initialising variable step
step = False

#Writing the problem file into the variable out 
out = """
(define (problem Health)
(:domain Employee)
(:objects 
r1 - user 
l1 - motor)
(:init 
(stop l1)
;hum
(= (hum_threshold) 29)
"""

#Connecting to the MQTT subscribe of Humidity script to recieve the Humidity value
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Humidity") 

#On Recieving the humidity value open a Problem pddl file and write the recieved value  
def on_message(client, userdata, msg):
    f = open("/home/pi/SourceCode/PDDL_FF_Planner/planner_humidity/HumidityProblem.pddl","w")
    myCmd_1 = 'chmod -R 777 /home/pi/SourceCode/PDDL_FF_Planner/planner_humidity/HumidityProblem.pddl'
    a = os.system(myCmd_1)
    f.writelines(out)
    h = str(msg.payload.decode('utf-8'))
    h_1 = float(h)
    f.writelines("(= (hum r1) {} )\n".format(h_1))
    f.writelines(')\n')
    f.writelines("(:goal (and (run-motor))\n")
    f.writelines(')\n')
    f.writelines(')')
    f.close()
#Run the FF planner file by feeding the domain and the problem file 
    myCmd = '/home/pi/SourceCode/PDDL_FF_Planner/planner_humidity/ff -o /home/pi/SourceCode/PDDL_FF_Planner/planner_humidity/Finaldomain_humidity.pddl -f /home/pi/SourceCode/PDDL_FF_Planner/planner_humidity/HumidityProblem.pddl > /home/pi/SourceCode/PDDL_FF_Planner/planner_humidity/output_humidity.txt'
    os.system(myCmd)

#Open an Output file and check for the action plan
    with open("/home/pi/SourceCode/PDDL_FF_Planner/planner_humidity/output_humidity.txt","r") as file_d:
        for line in file_d:
            action = 'step'
            if not action in line:
                GPIO.output(16, False)
            else:
                GPIO.output(16, True)
                time.sleep(2)
                print("Humidifier is switched on",h_1)
                GPIO.output(16, False)

#MQTT client connection with Humidity python Script
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org", 1883)

client.loop_forever()

