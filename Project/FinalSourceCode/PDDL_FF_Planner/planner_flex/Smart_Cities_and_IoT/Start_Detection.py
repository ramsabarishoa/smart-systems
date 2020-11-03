#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import paho.mqtt.publish as publish
import subprocess
from subprocess import run
import os

Flex_Path = "/home/pi/SL_Smart_Cities_IOT/Flex_Subscribe.py"
TH_Path = "/home/pi/SL_Smart_Cities_IOT/Temperature_and_Humdity_Detection.py"
os.chmod(Flex_Path, 0o777)
os.chmod(TH_Path, 0o777)

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN) #PIR
GPIO.setup(17, GPIO.OUT) #LED

count = 0

try:
    time.sleep(2) # to stabilize sensor
    while True:
        if GPIO.input(25):
            GPIO.output(17, True)
            count = count + 1
            time.sleep(5)
            GPIO.output(17, False)
            print("Motion Detected...")
            time.sleep(2) #to avoid multiple detection
        time.sleep(0.1) #loop delay, should be less than detection delay
        if count == 2:
            print(count)
            print("______________________________________", "Checking for Drowsiness", "______________________________________", sep="\n")
            publish.single("Person Detected", "Start monitoring drowsiness factor", hostname="test.mosquitto.org")
            subprocess.Popen(['python','Drowsiness_Subscribe.py'])
            print("______________________________________", "Checking for Posture", "______________________________________", sep="\n")
            subprocess.Popen(['python', 'Flex_Subscribe.py'])
            print("______________________________________", "Checking for Temperature and Humidity", "______________________________________", sep="\n")
            subprocess.Popen(['python', 'Temperature_and_Humdity_Detection.py'])
except:
    GPIO.cleanup()
