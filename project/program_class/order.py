import time

try:
    from process import process
    from mqtt_class.mqttPublish import mqttPublish
except:
    from project.program_class.mqtt_class.mqttPublish import mqttPublish
    from project.program_class.process import process

#Classe que define os pedidos feitos para a central
class order:


    def __init__(self, type, clientMqtt, properties = None, startOrder = True) -> None:
        self.type = type
        self.properties = properties
        self.status = ""
        self.properties["color"] = properties["color"].upper()
        self.startOrderTime  = str(time.ctime())
        self.finishOrdertTime  = ""
        self.orderId = properties["id"]
        if startOrder : return self.start_order()
    
    def start_order(self):
        if self.type == "assemble":
            respDirection = process.direction(self.type)
            respColor = process.assemblyColor(self.properties["color"])
            self.status = respDirection[0] , respColor[0]
            mqttPublish.publishMQTT("teste" , str(respDirection[0][0]))
        elif self.type == "storage":
            respDirection = process.direction(self.type)
            self.status = respDirection[0]
            mqttPublish.publishMQTT("teste" , str(respDirection[0][0]))
            pass
        else:
            print("Tipo desconhecido")
            mqttPublish.publishMQTT("teste" , "error")
            #error
            pass

    def status_order(self):
        pass