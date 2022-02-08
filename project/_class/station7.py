import time
import sys

try:
    from generic_station import generic_station
except:
    from project._class.generic_station import generic_station

class station7(generic_station):

    def __init__(self,clpNumber  , ip , temp = 2 , port = 502) -> None:
        super().__init__(clpNumber, ip , temp , port)
        self.temp = temp

    def outputStartWithColor(self, color):
        B1 = False
        B2 = False

        if color.upper() == "BLACK":
            B1 = True
            B2 = False
        elif color.upper() == "RED":
            B1 = False
            B2 = False
        elif color.upper() == "SILVER":
            B1 = False
            B2 = True 

        self.writeBits(6, B1)
        self.writeBits(7, B2)
        self.writeBits(8, False)
        
        time.sleep(0.1)
        self.pulseBit(9)

        self.status = "#{}S0D".format(self.clpNumber)

        return True , self.status

    def readColorsStorage(self):
        if self.readBits(10 , 1)[0]:
            B = self.readBits(6 , 3)
            self.pulseBit(10)
            return True , B
        else:
            return False , False

    def run(self):
        while True:
            resp = self.readColorsStorage()
            if self.stopFlag: break

            if resp[0]:
                color = ""
                if resp[1][0] and not resp[1][1]:
                    color = "BLACK"
                elif not resp[1][0] and not resp[1][1]:
                    color = "RED"
                elif not resp[1][0] and  resp[1][1]:
                    color = "SILVER"
                sys.stdout.write("\nUma peça deu entrada na estação 7!\nA cor da peça é: {}\n".format(color))
                sys.stdout.flush()
            else:
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(self.temp)







teste = station7(7, "192.168.2.70")
teste.input()
# teste.outputStartWithColor("BLACk")