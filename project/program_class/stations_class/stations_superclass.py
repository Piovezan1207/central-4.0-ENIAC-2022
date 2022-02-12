from pymodbus.client.sync import ModbusTcpClient
import os
import time
from dotenv import load_dotenv

try:
    from ... import errors
    from thread_ import thread_
except:
    from project.program_class.error_class import errors
    from project.program_class.stations_class.thread_ import thread_

try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

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

    

    def __init__(self, clpNumber, ip , temp , port = 502, useOrderList = False  ) -> None:
        super().__init__( temp, clpNumber )
        self.daemon = True
        self.ip = ip #ip referente ao CLP utilizado
        self.port = port #Porta utilizada pelo MODBUS
        self.clpNumber = clpNumber #Número da estação do CLP
        self.modbusClient = ModbusTcpClient(ip, port) #Instanciando um client modbus para esse CLP
        if useOrderList:#Caso seja necessária a utilização de lista de pedidos 
            self.order_list = [] #Lista de pedidos que podem ser feitos, onde essa estação é uma referencia
            self.loadOrderList() #Método para carregar a lista com os objetos de pedidos

    #Método para fazer a leitura de BITs do CLP, utiliando MODBUS
    #                       parametros
    # startBit -> int : Número do BIT em que a leitura no MODBUS deve ser iniciada 
    # numBits  -> int : Número de BOTs que devem ser lidos a partir do start bit

    #                       retorna
    # [] -> List : Lista de valores lidos no MODBUS, que serão booleanos
    def readBits(self, startBit, numBits):
        return  self.modbusClient.read_discrete_inputs(startBit,numBits).bits

    #Método para escrever em BITs do CLP, utilizando MODBUS
    #                       parametros
    # bitAddress -> int : Endereço do BIT a ser setado / resetado
    # bitValue   -> int : Valor em booleano a ser atribuido a esse endereço

    #                       retorna
    # True -> bool
    def writeBits(self, bitAddress, bitValue):
        self.modbusClient.write_coils(bitAddress, [bitValue]*1)
        return True
    
    #Método para dar um pulso em um BIT do CLP, utilizando MODBUS
    #                       parametros
    # bitAddress -> int : Endereço do BIT a receber o pulso

    #                       retorna
    # True -> bool
    def pulseBit(self, bitAddress):
        self.writeBits(bitAddress, True)
        self.writeBits(bitAddress, False)
        return True
    
    #Método para fazer um teste simples de resposta do CLP, com o objetico de verificar se o código
    #   colocado no controlador está correto, visto que, apenas a nova versão irá responder corretamente 
    #   a esse método de teste.
    
    #                       parametros
    # null

    #                       retorna
    # True -> bool : Caso o CLP passe no teste
    # Exception -> Exception : Caso o CLP não passe no teste, uma exceção será lançada e deve ser tradada
    #                               de forma a avisar a central desse CLP fora do padrão.
    def connctionTest(self):
        initialValue = self.readBits(self.bit_test_test, 1)[0] #Leitura do BIT de resoista (Deve estar em FALSE)
        self.writeBits(self.bit_test_test, True)               #Seta o  BIT de sinal para o CLP
        finalValue = self.readBits(self.bit_test_test, 1)[0]   #Leitura do BIT de resposta (Deve estar em True)
        self.writeBits(self.bit_test_test, False)              #Reseta o BIT de sianl paara o CLP
        if(not initialValue  and finalValue):   #Verifica se os valores lidos foram os esperados
            return True
        else:
            self.status = "#{}E01".format(self.clpNumber) #Cria o status que sinaliza esse erro
            raise errors.connection_error(self.clpNumber , self.ip, self.bit_test_test) #Lança a exceção
            return False

    #Método para salvar a lista de objetos referentes a ordens de serviços no qual esse CLP
    #   é responsável por finalizar

    #                       parametros
    # null

    #                       retorna
    # True -> bool 
    def saveOrderList(self):
        filename = "orderListStation{}.pkl".format(self.clpNumber)
        with open(filename, 'wb') as outp:  
            pickle.dump(self.order_list, outp, pickle.HIGHEST_PROTOCOL)
        return True

    #Método para carregar a lista de objetos referentes a ordens de serviços no qual esse CLP
    #   é responsável por finalizar

    #                       parametros
    # null

    #                       retorna
    # True -> bool 
    def loadOrderList(self):
        filename = "orderListStation{}.pkl".format(self.clpNumber)
        try:
            with open(filename, 'rb') as inp:
                self.order_list = pickle.load(inp)
            for i in  self.order_list:
                print("Iniciando ... Ordem estação {}".format(self.clpNumber) , i.type)
        except:
            with open(filename, 'wb'): pass
