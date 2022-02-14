import time
import sys
import json

try:
    from generic_station import generic_station
except:
    from project.program_class.stations_class.generic_station import generic_station

class station5(generic_station):

    def __init__(self,clpNumber  , ip , temp = 5 , port = 502, useOrderList = False) -> None:
        super().__init__(clpNumber, ip , temp, port , useOrderList)
        self.temp = temp
        self.pauseThread = True
        self.start()

    def confirmProcess(self):
        if self.readBits(10 , 1)[0]:
            B = self.readBits(6 , 3)
            self.pulseBit(10)
            return True , B
        else:
            return False , False

    def run(self):
        while True:
            if self.stopFlag: break

            if not self.pauseThread:
                self.isRunning = True
                resp = self.confirmProcess()

                if resp[0]:
                    color = ""
                    if resp[1][0] and not resp[1][1]:
                        color = "BLACK"
                    elif not resp[1][0] and not resp[1][1]:
                        color = "RED"
                    elif not resp[1][0] and  resp[1][1]:
                        color = "SILVER"

                    if self.order_list != []:
                        if self.order_list[0].properties["color"].upper() == color:
                            self.order_list[0].status = ""

                    # sys.stdout.write("\nUma teve sua montagem finalizada, e está na estação 5!\nA cor da peça é: {}\n".format(color))
                    # sys.stdout.flush()

                    message = json.dumps({
                        "type" : "finishedAssembly",
                        "properties" : {
                            "id" : self.order_list[0].orderId,
                            "color" : color,
                            "startDateTime" : self.order_list[0].startOrderTime,
                            "finishDateTime" : str(time.ctime())
                        },
                    })

                    self.threadPublishMQTT("teste" , message)

                    self.order_list.pop(0)
                    self.saveOrderList()
                    for i in  self.order_list:
                        print("Ordem estação 5 " , i.orderId)

                    # self.threadPublishMQTT("teste" , "\nUma teve sua montagem finalizada, e está na estação 5!\nA cor da peça é: {}\n".format(color))
                else:
                    # print("cachaça")
                    time.sleep(self.temp)
            else:
                self.isRunning = False



