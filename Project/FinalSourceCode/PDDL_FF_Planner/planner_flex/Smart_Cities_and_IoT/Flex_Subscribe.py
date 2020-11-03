import paho.mqtt.client as mqtt
import pandas as pd
from datetime import datetime

filename = b'/home/pi/SL_Smart_Cities_IOT/Employee_data.csv'
flex_list = []
my_time = []
data = {}

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("flex_values")

def on_message(client, userdata, msg):
    flex = msg.payload.decode('utf-8')
    flex_list.append(flex)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    my_time.append(current_time)
    data = {'Flex_Values' : flex_list, 'TimeStamp_flex' : my_time}
    df= pd.DataFrame(data)
    df.to_csv('DATA_FLEX.csv', encoding='utf-8',index = False)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org", 1883)

client.loop_forever()

