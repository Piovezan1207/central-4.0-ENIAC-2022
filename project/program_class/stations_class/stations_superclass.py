from pymodbus.client.sync import ModbusTcpClient
import os
import time
from dotenv import load_dotenv

try:
    import errors
    from thread_ import thread_
except:
    from project.program_class.error_class import errors
    from project.program_class.stations_class.thread_ import thread_

load_dotenv()

# Stations superclass
class stations_superclass(thread_):

    #Os BITs a seguir são padronizados nos códigos dos CLPs e tem funções parecidas, porém em modo entrada e saída
    #                                                               >>ENTRADA<<              >>SAÍDA<<
    bit_start_start=int(os.getenv("bit_start_start"))                    #Inicia a estação        Verifica se a estação está iniciada
    bit_stop_stop=int(os.getenv("bit_stop_stop"))                        #Para a estação          Verifica se a estação não está parada
    bit_reset_proccess=int(os.getenv("bit_reset_proccess"))              #Reinicia a estação      Verifica se a estação não está em processo
    bit_inputMode_inputMode=int(os.getenv("bit_inputMode_inputMode"))    #Seta o modo de entrada  Verifica se a estação está em modo de entrada
    bit_outputMode_outputMode=int(os.getenv("bit_outputMode_outputMode"))#Seta o modo de saída    Verifica se a estação está em modo de saída
    bit_test_test=int(os.getenv("bit_test_test"))                        #Teste de conexão        Teste de conexão - resposta da estação

    def __init__(self, clpNumber, ip , temp , port = 502  ) -> None:
        super().__init__( temp, clpNumber )
        self.daemon = True
        self.ip = ip
        self.port = port
        self.clpNumber = clpNumber
        self.modbusClient = ModbusTcpClient(ip, port)
    
    def readBits(self, startBit, numBits):
        return  self.modbusClient.read_discrete_inputs(startBit,numBits).bits

    def writeBits(self, bitAddress, bitValue):
        self.modbusClient.write_coils(bitAddress, [bitValue]*1)
        return True
    
    def pulseBit(self, bitAddress):
        self.writeBits(bitAddress, True)
        # time.sleep(0.1)
        self.writeBits(bitAddress, False)
        # time.sleep(0.1)
    
    def connctionTest(self):
        initialValue = self.readBits(self.bit_test_test, 1)[0]
        self.writeBits(self.bit_test_test, True)
        finalValue = self.readBits(self.bit_test_test, 1)[0]
        self.writeBits(self.bit_test_test, False)
        if(not initialValue  and finalValue):
            return True
        else:
            self.status = "#{}E01".format(self.clpNumber)
            raise project.program_class.error_class.errors.connection_error(self.clpNumber , self.ip, self.bit_test_test)
            return False


