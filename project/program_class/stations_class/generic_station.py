from time import time
try:
    from stations_superclass import stations_superclass
except:
    from project.program_class.stations_class.stations_superclass import stations_superclass
    
class generic_station(stations_superclass):

    status = ""

    def __init__(self,clpNumber , ip , temp = 5 , port = 502, ) -> None:
        super().__init__(clpNumber , ip , temp , port)

    def defaultInit(self):
        self.connctionTest()
        return self.readBits(0, 8)

    def startStation(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit()
        self.status = "#{}S00".format(self.clpNumber) #"Iniciando a estação."
        if  not result[self.bit_start_start] and not result[self.bit_stop_stop]:
            self.pulseBit(self.bit_start_start) 
            return True , self.status
        elif (result[self.bit_stop_stop]):
            self.pulseBit(self.bit_reset_proccess) 
            self.pulseBit(self.bit_start_start) 
            self.status = "#{}S01".format(self.clpNumber) #"A estação estava parada, foi resetada e então iniciada."
            return True , self.status
        elif (result[self.bit_start_start]):
            self.status = "#{}S02".format(self.clpNumber)#"A estação já está iniciada."
            return True , self.status

    def stopStation(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit()
        self.status = "#{}S03".format(self.clpNumber)#"Parando a estação."
        if (not result[self.bit_stop_stop]):
            self.pulseBit(self.bit_stop_stop) #Parar a estação
            return True , self.status
        else:
            self.status = "#{}S04".format(self.clpNumber)#"A estação já está parada"
            return True , self.status
    
    def resetStation(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit()
        self.status = "#{}S05".format(self.clpNumber)#"Reiniciando a estação"
        if not result[self.bit_stop_stop]:
            self.pulseBit(self.bit_stop_stop)
            self.pulseBit(self.bit_reset_proccess)
            return True , self.status
        else:
            self.pulseBit(self.bit_reset_proccess)
            return True , self.status

    def input(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit()
        self.status = "#{}S06".format(self.clpNumber)#"Estação em modo entrada."

        if(not result[self.bit_inputMode_inputMode]):
            self.writeBits(self.bit_outputMode_outputMode, False)
            self.writeBits(self.bit_inputMode_inputMode, True)
            return True , self.status
        else:
            self.writeBits(self.bit_outputMode_outputMode, False)
            self.status = "#{}S07".format(self.clpNumber)#"A estação já está em modo entrada."
            return True , self.status

    def output(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit()
        self.status = "#{}S08".format(self.clpNumber)#"Estação em modo saída."

        if(not result[self.bit_outputMode_outputMode]):
            self.writeBits(self.bit_inputMode_inputMode, False)
            self.writeBits(self.bit_outputMode_outputMode, True)
            return True , self.status
        else:
            self.writeBits(self.bit_inputMode_inputMode, False)
            self.status = "#{}S09".format(self.clpNumber)#"A estação já está em modo saída."
            return True , self.status

