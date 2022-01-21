try:
    from generic_station import generic_station
except:
    from project._class.generic_station import generic_station

class station1(generic_station):

    def __init__(self,clpNumber  , ip , port = 502) -> None:
        super().__init__(clpNumber, ip , port)

    def start(self):
        self.connctionTest()
        self.status = "Iniciando a estação...."
        result = self.readBits(0, 8)
        if result[6]:
            self.status = "A estação está sem peças disponíveis no magazine."
            return False
        else:
            super().start(True, result)
