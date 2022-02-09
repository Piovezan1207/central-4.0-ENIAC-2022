import paho.mqtt.publish as publish  
import os
from dotenv import load_dotenv
load_dotenv()

class mqttPublish:
    def __init__(self) -> None:
        pass

    @staticmethod
    def publishMQTT(topic, payload, id=""):

        auth = {"username" : os.getenv("USERNAME_"), "password":os.getenv("PASSWORD")}

        publish.single(
            topic , 
            str(payload), 
        hostname=os.getenv("BOKER"), 
        port=int(os.getenv("PORTABROKER")),
        auth=auth,
        client_id=id,
        )