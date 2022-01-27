import time
try:
    from generic_station import generic_station
except:
    from project._class.generic_station import generic_station

class station7(generic_station):

    def __init__(self,clpNumber  , ip , port = 502) -> None:
        super().__init__(clpNumber, ip , port)

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



