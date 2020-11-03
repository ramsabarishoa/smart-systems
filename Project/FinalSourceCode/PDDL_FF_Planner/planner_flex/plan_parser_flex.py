#Import relevant Library files
import os
import socket
import paho.mqtt.client as mqtt 
import sys
import time
import RPi.GPIO as GPIO

#Initialisation of GPIO port settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setwarnings(False)

#Initialise user and step variable
user = False
step = False

#Socket connection is to recieve user presence flag
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.8', 8080))
from_server = client.recv(4096)
client.close()
print("After connecting to socket",from_server)

#Writing the problem file into the variable out
out = """
(define (problem Health)
(:domain Employee)
(:objects 
r1 - user 
l1 - led)
(:init 
(off l1)
;pos
(= (pos_threshold) 100)
"""

#If user is present then start process
if from_server == "User Present":
    user = True
    # Connecting with the publisher from flex script fro teh bend values
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("flex_values") 
    #On Recieving the flex values write values to the prpoblem file
    def on_message(client, userdata, msg):
        f = open("/home/pi/SourceCode/PDDL_FF_Planner/planner_flex/Flexproblem.pddl",'w')
        myCmd_1 = 'chmod -R 777 /home/pi/SourceCode/PDDL_FF_Planner/planner_flex/Flexproblem.pddl'
        os.system(myCmd_1)
        f.writelines(out)
        flex_payload = str(msg.payload.decode('utf-8'))
        float_flex_payload = float(flex_payload)
        flex = int(float_flex_payload)
        f.writelines("(= (pos r1) {} )\n".format(flex))
        f.writelines(')\n')
        f.writelines("(:goal (and (on-led))\n")
        f.writelines(')\n')
        f.writelines(')')
        f.close()
	#Run the FF planner file by feeding the domain and the problem file
        myCmd = '/home/pi/SourceCode/PDDL_FF_Planner/planner_flex/ff -o /home/pi/SourceCode/PDDL_FF_Planner/planner_flex/Finaldomain_Flex.pddl -f /home/pi/SourceCode/PDDL_FF_Planner/planner_flex/Flexproblem.pddl > /home/pi/SourceCode/PDDL_FF_Planner/planner_flex/output_flex.txt'
        a = os.system(myCmd)
	#Open an Output file and check for the action plan
        with open("/home/pi/SourceCode/PDDL_FF_Planner/planner_flex/output_flex.txt","r") as file_d:
            for line in file_d:
                action = 'step'
                if not action in line:
                    #print("Person is sitting straight")
                    GPIO.output(6, False)
                else:
                    GPIO.output(6, True)
                    time.sleep(2)
                    print("Bend Detected - Please Correct your posture : Forward Angle",flex)
                    GPIO.output(6, False)
   
    #MQTT client connection with Humidity python Script
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("test.mosquitto.org", 1883)

    client.loop_forever()


