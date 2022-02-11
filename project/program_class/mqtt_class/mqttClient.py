import paho.mqtt.client as mqtt

import os
from dotenv import load_dotenv
import json

try:
    from ..order import order
    from ..process import process
    from ..process import stations
except:
    from project.program_class.order import order
    from project.program_class.process import process
    from project.program_class.process import stations

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

    assemble_oder_list = []
    storage_oder_list = []

    def __init__(self, broker = os.getenv("BOKER") , 
                       port = int(os.getenv("PORTABROKER")), 
                       username = os.getenv("USERNAME_"), 
                       password = os.getenv("PASSWORD"), 
                       topic = os.getenv("TOPICO"), 
                       keepAliveBroker = 60,
                       connect = False,) -> None:

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic
        self.keepAliveBroker = keepAliveBroker
        self.processClass = process()
        self.processClass.playThread_()

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
        message = msg.payload
        
        check = self.checkJsonStructure(message)

        if not check[0]: 
            client.publish("teste" , json.dumps(check[1])) 
            return

        client.publish("teste" , "ok")
        jsonCommands =  check[1]


        if jsonCommands["type"] == "assemble":
           
            properties = jsonCommands["properties"]
            #A lista de pedidos de montagens estará no objeto da estação 5, visto que uma thread dessa estação
            #   irá finalizar esses pedidos
            stations[5].order_list.append(order("assemble" , client , properties))
            for i in  stations[5].order_list:
                print("Ordem estação 5 " , i.type)

        elif jsonCommands["type"] == "storage":
            #A lista de pedidos de armazenamento estará no objeto da estação 7, visto que uma thread dessa estação
                #   irá finalizar esses pedidos
            stations[7].order_list.append(order("storage" , client))
            for i in  stations[7].order_list:
                    print("Ordem estação 7 " , i.type)
        else:
            print("Tipo desconhecido...")


    def checkJsonStructure(self, message):

        jsonErrorResp = {
                "type" : "error",
                "properties" : {
                    "status" : "structureError",
                    "description" : ""
                },
            }

        try:    jsonCommands = json.loads(message)
        except:
            jsonErrorResp["properties"]["description"] = "Erro no formato da estrutura da JSON." 
            return False, jsonErrorResp
        
        if "type" not in jsonCommands or "properties" not in jsonCommands: 
            jsonErrorResp["properties"]["description"] = "O parâmetro type ou properties não foi passado." 
            return False, jsonErrorResp

        typesList = ["storage" , "assemble"]
        parameterList = {
            typesList[0] : [["id" , self.checkIdParameter ] ],
            typesList[1] : [["id" , self.checkIdParameter ] , ["color" , self.checkcolorParameter]],
            }

        if jsonCommands["type"] not in typesList:
            jsonErrorResp["properties"]["description"] = "O valor de type é invalido." 
            return False, jsonErrorResp


        for parameter in parameterList:
            if parameter == jsonCommands["type"]:
                 for specificParameter in parameterList[parameter]:

                     if specificParameter[0] not in jsonCommands["properties"]: 
                         jsonErrorResp["properties"]["description"] = "O parâmetro passado no properties é inválido." 
                         return False, jsonErrorResp
                     else:
                         if not  specificParameter[1](jsonCommands["properties"][specificParameter[0]]):
                            jsonErrorResp["properties"]["description"] = "O valor do parâmetro {} é inválido.".format(specificParameter[0]) 
                            return False, jsonErrorResp
        
        return True, jsonCommands
                 

    def checkIdParameter(self, id):
        try:
            int(id)
            return True
        except:
            return False

    def checkcolorParameter(self, color):
        listColors = ["BLACK" , "SILVER" , "RED"]
        if color.upper() in listColors: return True
        else: return False


