import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
import json

try:
    from order import order
except:
    from project._class.order import order

load_dotenv()


class mqttClient:

    connection_list = {
     "0" :   "Connection successful",
     "1" :  "Connection refused – incorrect protocol version",
     "2" :  "Connection refused – invalid client identifier",
     "3" :  "Connection refused – server unavailable",
     "4" :  "Connection refused – bad username or password",
     "5" :  "Connection refused – not authorised",
     "6" :  "255: Currently unused."
    }

    oder_list = []

    def __init__(self, broker = os.getenv("BOKER") , 
                       port = int(os.getenv("PORTABROKER")), 
                       username = os.getenv("USERNAME_"), 
                       password = os.getenv("PASSWORD"), 
                       topic = os.getenv("TOPICO"), 
                       keepAliveBroker = 60,
                       connect = False) -> None:

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic
        self.keepAliveBroker = keepAliveBroker

        if connect: self.connect()

    def connect(self):
        self.client.username_pw_set(username=self.username, password=self.password)
        self.client.connect(self.broker, self.port, self.keepAliveBroker)
        self.client.loop_forever()
   
    def on_connect(self, client, userdata, flags, rc):
        status_code = str(rc)
        print("[STATUS] {} - {}".format(status_code , self.connection_list[status_code]))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        mensagem = msg.payload
        try:
            jsonCommands = json.loads(mensagem)
        except:
            print("Erro na json recebida")
            return
        print(jsonCommands)

        if "type" in jsonCommands:
            if jsonCommands["type"] == "assemble":
                if "color" in jsonCommands:
                    color = jsonCommands["color"]
                    self.oder_list.append(order("assemble" , color))
            elif jsonCommands["type"] == "storage":
                self.oder_list.append(order("storage"))
            else:
                print("Tipo desconhecido...")
        else:
            print("False algo aqui...")
        print(self.oder_list)
    