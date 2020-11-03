#!/usr/bin/env python

# Import libraries
import RPi.GPIO as GPIO
import time
import paho.mqtt.publish as publish
import subprocess
import os
import socket

# Setting GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN) #PIR
GPIO.setup(17, GPIO.OUT) #LED

# Flag to check user presence
flag = 0

try:
    time.sleep(2) # to stabilize sensor
    while True:
        if GPIO.input(24):
            GPIO.output(17, True)
            flag = flag + 1
            time.sleep(5)
            GPIO.output(17, False)
            #print("Motion Detected...")
            time.sleep(2) #to avoid multiple detection
        time.sleep(0.1) #loop delay, should be less than detection delay
        if flag == 2:
            #user = True       
            print("__________________________________________User Detected______________________________________________________________")
            #Pop-up to request permission from the user
            publish.single("Person Detected", "Pop-up to request permission from the user", hostname="test.mosquitto.org",port=1883,keepalive=60)

            time.sleep(10)
	    #Trigger to an AI planner
            print("__________________________________________Start AI Planner____________________________________________________________")
            
            #Trigger Sub-process of Humidity sensing, AI parser and Flex AI parser file
	    
            subprocess.Popen(['python','/home/pi/SourceCode/PDDL_FF_Planner/planner_flex/plan_parser_flex.py'])
            subprocess.Popen(['python', 'Humidity.py'])
            subprocess.Popen(['python','/home/pi/SourceCode/PDDL_FF_Planner/planner_humidity/plan_parser_humidity.py'])

            # Start Socket Connection to the PDDL Planner by sending the user presence
            serv = socket.socket()
            serv.bind(('192.168.0.8',8080))
            serv.listen(5)
            print("Socket connection successful")
            conn,addr = serv.accept()
            conn.send(b"User Present")
            conn.close()
            print('client disconnected')
            time.sleep(10)

	    #Trigger Drowsiness script via MQTT
            print("_________________________________________Checking for Drowsiness_____________________________________________________", sep="\n")
            publish.single("Person Detected", "Start monitoring drowsiness factor", hostname="test.mosquitto.org")
            time.sleep(10)
	    #Plot Drowsiness Detection values and write to CSV
            print("_________________________________________Plotting Drowsiness Detection_______________________________________________")
            cmd_1 = 'rm -rf ear.csv'
            os.system(cmd_1)
            time.sleep(1)
            subprocess.Popen(['python3', 'Drowsiness_CSV.py'])
            time.sleep(5)
            subprocess.Popen(['python3', 'Drowsiness_Plot.py'])
	    
            #Plot posture check values and write to csv
            print("_________________________________________Plotting Bend Curve_________________________________________________________")
            cmd_2 = 'rm -rf flex.csv'
            os.system(cmd_2)
            time.sleep(1)
            subprocess.Popen(['python3', 'Flex_CSV.py'])
            subprocess.Popen(['python3', 'Flex_Plot.py'])
            
            #Plot Humidity check value and write to csv
            print("_________________________________________Plotting Changes Humidity___________________________________________________")
            cmd_3 = 'rm -rf humid.csv'
            os.system(cmd_3)
            time.sleep(1)
            subprocess.Popen(['python3', 'Humidity_CSV.py'])
            subprocess.Popen(['python3', 'Humidity_Plot.py'])
except:
    GPIO.cleanup()
