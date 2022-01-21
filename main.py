import os
import json
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
load_dotenv()

from project._class.generic_station import generic_station
from project._class.station1 import station1
from project._class.station7 import station7



order = {
    "order_type"  : "assemble",
    "properties" :
        [{
        "color"  : "black",
        "amount" : "1",
        "id" : "0",
        }]
}

station3_.input()

print(station3_.status)