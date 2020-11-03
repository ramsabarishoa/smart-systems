import paho.mqtt.client as mqtt
from datetime import datetime
import pandas as pd

filename = b'/home/pi/SL_Smart_Cities_IOT/Employee_data_1.csv'
my_time = []
ear_list = []
data_1 = {}


def on_connect(client, userdata, flags, rc):
    print("Collecting EAR Values "+str(rc))
    client.subscribe("EAR_Values")
    
    
def on_message(client, userdata, msg):
    EAR = msg.payload.decode()
   # print(EAR)
    ear_list.append(EAR)
    #print(ear_list)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    my_time.append(current_time)
    #print("***********:")
    data_1 = {'EAR_Values' : ear_list,'time' : my_time}
    #print(data_1)
    df= pd.DataFrame(data_1)
    df.to_csv('DATA_EAR.csv', encoding='utf-8',index = False)
    #print("----------------")
            
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("test.mosquitto.org", 1883)
client.loop_forever()
