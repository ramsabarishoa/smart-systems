
    
#Update from the Script above with modification of writing the data to a CSV.file:
# Importeer Adafruit DHT bibliotheek.
#time.strftime("%I:%M:%S")
import Adafruit_DHT
import time
import csv
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from datetime import datetime
csvfile = "humid.csv"
while True: 
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 8) 
    if humidity is not None and temperature is not None:
      humidity = round(humidity,2)
      temperature = round(temperature,2)
      #print ("Temperature = {0:0.1f}*C  Humidity = {1:0.1f}%".format(temperature, humidity))
    else:
      print ('can not connect to the sensor!')
    timeC = time.strftime("%H")+':' +time.strftime("%M")+':'+time.strftime("%S")
    data = [humidity,timeC]
    with open(csvfile, "a")as output:
        writer = csv.writer(output, delimiter=",", lineterminator = '\n')
        writer.writerow(data)
        time.sleep(2) # update script every 60 second
