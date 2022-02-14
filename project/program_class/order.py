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
        # self.clientMqtt = clientMqtt # ESSE CARA CAUSA PROBLEMA PARA SALVAR O OBJETO UTILIZANDO PICKLE
        self.status = ""
        self.startOrderTime  = str(time.ctime())
        self.finishOrdertTime  = ""
        self.orderId = properties["id"]
        if startOrder : self.start_order()
    
    def start_order(self):
        if self.type == "assemble":
            respDirection = process.direction(self.type)
            respColor = process.assemblyColor(self.properties["color"])
            # print(respDirection[0][0])
            self.status = respDirection[0] , respColor[0]
            mqttPublish.publishMQTT("teste" , str(respDirection[0][0]))
        elif self.type == "storage":
            respDirection = process.direction(self.type)
            # print(respDirection[0])
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