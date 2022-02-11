import time
import sys

try:
    from generic_station import generic_station
except:
    from project.program_class.stations_class.generic_station import generic_station

class station5(generic_station):

    def __init__(self,clpNumber  , ip , port = 502, temp = 5) -> None:
        super().__init__(clpNumber, ip , port)
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
                        if self.order_list[0].properties.upper() == color:
                            self.order_list[0].status = ""

                    sys.stdout.write("\nUma teve sua montagem finalizada, e está na estação 5!\nA cor da peça é: {}\n".format(color))
                    sys.stdout.flush()
                    self.threadPublishMQTT("teste" , "\nUma teve sua montagem finalizada, e está na estação 5!\nA cor da peça é: {}\n".format(color))
                else:
                    time.sleep(self.temp)
            else:
                self.isRunning = False



