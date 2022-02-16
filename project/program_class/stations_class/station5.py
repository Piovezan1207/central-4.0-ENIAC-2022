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
        self.pauseThread = False
        self.start()

    def confirmProcess(self):
        if self.readBits(6 , 1)[0]:
            B = self.readBits(6 , 12)
            self.pulseBit(6)
            
            return True , B
        else:
            return False , False

    def binaryToInt(self, binaryList):
            val = 0
            val += int(binaryList[0]) * 1
            val += int(binaryList[1]) * 2
            val += int(binaryList[2]) * 4
            return val


    def run(self):
        while True:
            if self.stopFlag: break

            if not self.pauseThread:
                self.isRunning = True
                resp = self.confirmProcess()

                if resp[0]:

                    color = { "BLACK" : self.binaryToInt(resp[1][1:4]),
                              "SILVER" : self.binaryToInt(resp[1][4:7]),
                              "RED" : self.binaryToInt(resp[1][7:10] ),
                            }
                    
                    print(color)

                    # if self.order_list != []:
                    #     if self.order_list[0].properties["color"].upper() == color:
                    #         self.order_list[0].status = ""

                    # # sys.stdout.write("\nUma teve sua montagem finalizada, e está na estação 5!\nA cor da peça é: {}\n".format(color))
                    # # sys.stdout.flush()

                    # message = json.dumps({
                    #     "type" : "finishedAssembly",
                    #     "properties" : {
                    #         "id" : self.order_list[0].orderId,
                    #         "color" : color,
                    #         "startDateTime" : self.order_list[0].startOrderTime,
                    #         "finishDateTime" : str(time.ctime())
                    #     },
                    # })

                    # self.threadPublishMQTT("teste" , message)

                    # self.order_list.pop(0)
                    # self.saveOrderList()
                    # for i in  self.order_list:
                    #     print("Ordem estação 5 " , i.orderId)

                    # self.threadPublishMQTT("teste" , "\nUma teve sua montagem finalizada, e está na estação 5!\nA cor da peça é: {}\n".format(color))
                else:
                    time.sleep(self.temp)
            else:
                self.isRunning = False



