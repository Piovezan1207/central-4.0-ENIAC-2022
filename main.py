import os
import json
import time
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
load_dotenv()

from project.program_class.stations_class.generic_station import generic_station
from project.program_class.stations_class.station1 import station1
from project.program_class.stations_class.station7 import station7
from project.program_class.mqtt_class.mqttClient import mqttClient

if __name__ == "__main__":
    cliente = mqttClient(connect=True)


# order = {
#     "order_type"  : "assemble",
#     "properties" :
#         [{
#         "color"  : "black",
#         "amount" : "1",
#         "id" : "0",
#         }]
# }


# "{\"order_type\":\"assemble\",\"properties\":[{\"color\":\"black\",\"amount\":\"1\",\"id\":\"0\"}]}"
