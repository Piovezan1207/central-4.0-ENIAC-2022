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
