
try:
    from process import process
except:
    from project.program_class.process import process


#Classe que define os pedidos feitos para a central
class order:

    

    def __init__(self, type, clientMqtt, properties = None) -> None:
        self.type = type
        self.properties = properties
        self.clientMqtt = clientMqtt
        self.status = ""
        self.startOrderTime  = ""
        self.finishOrdertTime  = ""
        self.orderId = properties["id"]
        self.start_order()
    
    def start_order(self):
        if self.type == "assemble":
            respDirection = process.direction(self.type)
            respColor = process.assemblyColor(self.properties["color"])
            # print(respDirection[0][0])
            self.status = respDirection[0] , respColor[0]
            self.clientMqtt.publish("teste" , str(respDirection[0][0]))
        elif self.type == "storage":
            respDirection = process.direction(self.type)
            # print(respDirection[0])
            self.status = respDirection[0]
            self.clientMqtt.publish("teste" , str(respDirection[0][0]))
            pass
        else:
            print("Tipo desconhecido")
            self.clientMqtt.publish("teste" , "error")
            #error
            pass

    def status_order(self):
        pass