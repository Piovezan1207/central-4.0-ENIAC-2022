try:
    from generic_station import generic_station
except:
    from project._class.generic_station import generic_station

class station1(generic_station):

    def __init__(self,clpNumber  , ip , port = 502) -> None:
        super().__init__(clpNumber, ip , port)

    def startStation(self):
        self.connctionTest()
        result = self.readBits(0, 8)

        if result[6]:
            self.status = "#{}E09".format(self.clpNumber)#"A estação está sem peças disponíveis no magazine."
            return False , self.status
        else:
            return super().startStation(True, result)
