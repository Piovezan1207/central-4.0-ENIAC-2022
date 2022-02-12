from time import time
try:
    from stations_superclass import stations_superclass
except:
    from project.program_class.stations_class.stations_superclass import stations_superclass

#Classe que define a estações de forma genérica
class generic_station(stations_superclass):

    status = ""

    def __init__(self,clpNumber , ip , temp = 5 , port = 502, useOrderList = False) -> None:
        #Stations superclass
        super().__init__(clpNumber , ip , temp , port, useOrderList)

    #Método para fazer a inicialização padrão dos outros métodos, pois, caso alguma estação precise
    #   fazer algum tipo de verificação diferenciada, terá uma classe e inicialização própria.
    #                       parametros
    # null

    #                       retorna
    # [] -> List : Lista de 1 byte lidos no MODBUS dessa estação
    def defaultInit(self):
        self.connctionTest() #Faz um teste de conexão
        return self.readBits(0, 8) #Efetua a leitura do primeiro byte do MODBUS, que contém informações
                                   #    úteis para verificar se os métodos a baixo podem cumprir seus propósitos.   

    #Método para iniciar a estação
    #                       parametros
    # _defaultInit -> bool = False : flag utilizada quando a estação tiver uma inicialização diferenciada
    #   desses métodos. Quando for True, a lista de leitura de BITS deve ser passada no parametro _result 
    # _result  -> list = [] : Lista de leitura dos BITS feita no momento da inicialização personalizada

    #                       retorna
    #  [0] / True   -> bool : Caso a inicialização seja feito com sucesso 
    #  [0] / False  -> bool : Caso a inicialização não seja concluida
    #  [1] / status -> list : Status resultantes dos comandos feitos nesse método
    def startStation(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit() #Verifica qual inicialização será utilizada
        self.status = "#{}S00".format(self.clpNumber) #Status S00 - A estação foi iniciada com sucesso
        if  not result[self.bit_start_start] and not result[self.bit_stop_stop]: #VErifica se a estação já não está iniciada ou se está parada
            self.pulseBit(self.bit_start_start) #Inicia a estação com um pulso no BIT de start
            return True , self.status #retorna o sucesso
        elif (result[self.bit_stop_stop]): #Caso a estação esteja parada
            self.pulseBit(self.bit_reset_proccess)  #Será reinicicada
            self.pulseBit(self.bit_start_start)     #Será será iniciada
            self.status = "#{}S01".format(self.clpNumber) #Status S01 - A estação estava parada, foi reiniciada e iniciada.
            return True , self.status #Retorna o sucesso
        elif (result[self.bit_start_start]): #Caso a estação já esteja iniciada
            self.status = "#{}S02".format(self.clpNumber)#Status S02 -	A estação já estava iniciada.
            return True , self.status
    
    #Método para parar a estação
    #                       parametros
    # _defaultInit -> bool = False : flag utilizada quando a estação tiver uma inicialização diferenciada
    #   desses métodos. Quando for True, a lista de leitura de BITS deve ser passada no parametro _result 
    # _result  -> list = [] : Lista de leitura dos BITS feita no momento da inicialização personalizada

    #                       retorna
    #  [0] / True   -> bool : Caso a parada seja feito com sucesso 
    #  [0] / False  -> bool : Caso a parada não seja concluida
    #  [1] / status -> list : Status resultantes dos comandos feitos nesse método
    def stopStation(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit() #Verifica qual inicialização será utilizada
        self.status = "#{}S03".format(self.clpNumber)#Status S03 - A estação foi parada.
        if (not result[self.bit_stop_stop]): #Caso a estação já não esteja parada
            self.pulseBit(self.bit_stop_stop) #Parar a estação
            return True , self.status #Retorna o sucesso
        else: #Caso a estação já esteja parada
            self.status = "#{}S04".format(self.clpNumber)#S04 - A estação já estava parada.
            return True , self.status #Retorna o sucesso
    
    #Método para reiniciar a estação
    #                       parametros
    # _defaultInit -> bool = False : flag utilizada quando a estação tiver uma inicialização diferenciada
    #   desses métodos. Quando for True, a lista de leitura de BITS deve ser passada no parametro _result 
    # _result  -> list = [] : Lista de leitura dos BITS feita no momento da inicialização personalizada

    #                       retorna
    #  [0] / True   -> bool : Caso a reinicialização seja feito com sucesso 
    #  [0] / False  -> bool : Caso a reinicialização não seja concluida
    #  [1] / status -> list : Status resultantes dos comandos feitos nesse método
    def resetStation(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit() #Verifica qual inicialização será utilizada
        self.status = "#{}S05".format(self.clpNumber)#Status S05 - A estação foi reiniciada.
        if not result[self.bit_stop_stop]: #Caso a estação não esteja parada
            self.pulseBit(self.bit_stop_stop) #Para a estação
            self.pulseBit(self.bit_reset_proccess) #Reinicia a estação
            return True , self.status #Retorna o sucesso
        else: #CAso a estação já esteja parada
            self.pulseBit(self.bit_reset_proccess) #Reinicia a estção
            return True , self.status #Retorna o sucesso

    #Método para definir essa estação como modo entrada (só funcionará para algumas)
    #                       parametros
    # _defaultInit -> bool = False : flag utilizada quando a estação tiver uma inicialização diferenciada
    #   desses métodos. Quando for True, a lista de leitura de BITS deve ser passada no parametro _result 
    # _result  -> list = [] : Lista de leitura dos BITS feita no momento da inicialização personalizada

    #                       retorna
    #  [0] / True   -> bool : Caso a estação fique em modo entrada com sucesso
    #  [0] / False  -> bool : Caso haja algum problema para que a estação fique em modo entrada
    #  [1] / status -> list : Status resultantes dos comandos feitos nesse método
    def input(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit() #Verifica qual inicialização será utilizada
        self.status = "#{}S06".format(self.clpNumber)#Status S06 - Estação colocada em modo entrada.

        if(not result[self.bit_inputMode_inputMode]): #Caso a estação não esteja em modo entrada
            self.writeBits(self.bit_outputMode_outputMode, False) #Retira o modo saída (por garantia)
            self.writeBits(self.bit_inputMode_inputMode, True) #Coloca a estação em modo entrada
            return True , self.status #Retorna o sucesso
        else: #Caso a estação já esteja em modo entrada
            self.writeBits(self.bit_outputMode_outputMode, False) #Retira o modo saida (por garantia)
            self.status = "#{}S07".format(self.clpNumber)#Status S07 - Estação já está em modo entrada.
            return True , self.status #Retorna o sucesso

    #Método para definir essa estação como modo saída (só funcionará para algumas)
    #                       parametros
    # _defaultInit -> bool = False : flag utilizada quando a estação tiver uma inicialização diferenciada
    #   desses métodos. Quando for True, a lista de leitura de BITS deve ser passada no parametro _result 
    # _result  -> list = [] : Lista de leitura dos BITS feita no momento da inicialização personalizada

    #                       retorna
    #  [0] / True   -> bool : Caso a estação fique em modo saída com sucesso
    #  [0] / False  -> bool : Caso haja algum problema para que a estação fique em modo saída
    #  [1] / status -> list : Status resultantes dos comandos feitos nesse método
    def output(self, _defaultInit = False, _result = []):
        result = _result if _defaultInit else  self.defaultInit() #Verifica qual inicialização será utilizada
        self.status = "#{}S08".format(self.clpNumber)#Status S08 - Estação colocada em modo saída.

        if(not result[self.bit_outputMode_outputMode]): #Caso a estação não esteja em modo saída
            self.writeBits(self.bit_inputMode_inputMode, False) #retira do modo entrada (por garantia)
            self.writeBits(self.bit_outputMode_outputMode, True) #Coloca em modo saída
            return True , self.status #Retorna o sucesso
        else:
            self.writeBits(self.bit_inputMode_inputMode, False) #Retira do modo entrada (por garantia)
            self.status = "#{}S09".format(self.clpNumber)#Status S09 - Estação já estava em modod saída.
            return True , self.status

