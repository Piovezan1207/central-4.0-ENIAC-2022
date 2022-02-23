from asyncio.windows_events import NULL
import time
import json

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
        self.status = None
        self.startOrderTime  = str(time.ctime())
        self.finishOrdertTime  = ""
        self.orderId = properties["id"]
    
        if type == "assemble": properties["color"] = properties["color"].upper() #Só existirá essa propriedade caso seja do tipo assembly
        
        if startOrder : return self.startOrder()
        


    def startOrder(self):
        # print(self.properties["color"])
        #Tipo "assemble" -> Montagem de alguma peça
        if self.type == "assemble":
            respDirection = process.direction(self.type)
            respColor = process.assemblyColor(self.properties["color"])
            self.status = (respDirection[0] and respColor[0]) #O status só será True, se os dois valores forem True
            respJson = self.makeRespJson("{} , {}".format(respDirection[2] , respColor[2]))#Cria a json de resposta para a central administradora
            mqttPublish.publishMQTT("teste" , respJson) #Caso uma das duas respostas seja false, publicar informando que esse pedido nãio foi aceito
       
       #Tipo "storage" -> armazenamento de peças
        elif self.type == "storage":
            respDirection = process.direction(self.type)
            self.status = respDirection[0] 
            respJson = self.makeRespJson(respDirection[2])#Cria a json de resposta para a central administradora
            mqttPublish.publishMQTT("teste" , respJson) #Caso uma das duas respostas seja false, publicar informando que esse pedido nãio foi aceito
            pass
       
       #Caso o type não seja conhecido, ele execulta esse else, porem, isso é uma redundancia, visto que
            #o json de pedido já é verificada logo na sua chegada, na classe mqttClient
        else:
            print("Tipo desconhecido")
            json_resp = {
                "type" : "error",
                "properties" : {
                    "status" : "structureError",
                    "description" : "Tipo desconhecido."
                }
            }
            mqttPublish.publishMQTT("teste" , json.dumps(json_resp)) #Sinalizar que esse pedido teve algum erro

    def statusOrder(self):
        pass

    #Cria a json de resposta para os pedidos. Essa pode responder indicando que houve algum erro no pedido
        #o que vai sinalizar a central administradora que o pedido deve ser feito novamente futuramente.
    def makeRespJson(self, statusCode):
        #Json de resposta para a central ADM
        json_resp = {
        "tye" : "orderResponse",
        "properties" : {
            "status" : self.status,   #Status (bool) - True caso o pedido tenha sido passado para a planta / False caso tenha tido algum erro ee o pedido nao foi passado para a planta
            "statusCode" : statusCode, #Ultimo status vindo da classe procces (pode indicar a causa do erro e um feedback do sucesso)
            "orderId" : self.orderId  #Id do pedido
        }
        }
        return json.dumps(json_resp)
