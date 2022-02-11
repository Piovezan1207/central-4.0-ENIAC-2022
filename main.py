from project.program_class.mqtt_class.mqttClient import mqttClient
import json 
if __name__ == "__main__":
    cliente = mqttClient(connect=True)

    
    # cliente = mqttClient()
    # message = json.dumps({
    #             "type" : "assemble",
    #             "properties" : {
    #                 "id" : "10",
    #                 "color" : "BLACK"
    #             },
    #         })

    # val = cliente.checkJsonStructure(message)
    # print(json.dumps(val))

