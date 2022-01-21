from time import time
try:
    from stations_superclass import stations_superclass
except:
    from project._class.stations_superclass import stations_superclass
    
class generic_station(stations_superclass):

    status = ""

    def __init__(self,clpNumber , ip , port = 502) -> None:
        super().__init__(clpNumber , ip , port)

    def defaultInit(self):
        self.connctionTest()
        return self.readBits(0, 8)

    def start(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit()
        self.status = "Iniciando a estação."
        if  not result[self.bit_start_start] and not result[self.bit_stop_stop]:
            self.pulseBit(self.bit_start_start) 
            return True
        elif (result[self.bit_stop_stop]):
            self.pulseBit(self.bit_reset_proccess) 
            self.pulseBit(self.bit_start_start) 
            self.status = "A estação estava parada, foi resetada e então iniciada."
            return True
        elif (result[self.bit_start_start]):
            self.status = "A estação já está iniciada."
            return True

    def stop(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit()
        self.status = "Parando a estação."
        if (not result[self.bit_stop_stop]):
            self.pulseBit(self.bit_stop_stop) #Parar a estação
            return True
        else:
            self.status = "A estação já está parada"
            return True
    
    def reset(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit()
        self.status = "Reiniciando a estação"
        if not result[self.bit_stop_stop]:
            self.pulseBit(self.bit_stop_stop)
            self.pulseBit(self.bit_reset_proccess)
            return True
        else:
            self.pulseBit(self.bit_reset_proccess)
            return True

    def input(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit()
        self.status = "Estação em modo entrada."

        if(not result[self.bit_inputMode_inputMode]):
            self.writeBits(self.bit_outputMode_outputMode, False)
            self.writeBits(self.bit_inputMode_inputMode, True)
            return True
        else:
            self.writeBits(self.bit_outputMode_outputMode, False)
            self.status = "A estação já está em modo entrada."
            return True
    
    def output(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit()
        self.status = "Estação em modo saída."

        if(not result[self.bit_outputMode_outputMode]):
            self.writeBits(self.bit_inputMode_inputMode, False)
            self.writeBits(self.bit_outputMode_outputMode, True)
            return True
        else:
            self.writeBits(self.bit_inputMode_inputMode, False)
            self.status = "A estação já está em modo saída."
            return True

