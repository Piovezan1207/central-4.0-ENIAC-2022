from concurrent.futures import thread
import datetime
import os
import time

try:
    from generic_station import generic_station
    from station1 import station1
    from station5 import station5
    from station7 import station7
    from thread_ import thread_

except:
    from project._class.generic_station import generic_station
    from project._class.station1 import station1
    from project._class.station5 import station5
    from project._class.station7 import station7
    from project._class.thread_ import thread_
    
#Estações da planta
stations = {
    1 : station1(1, "192.168.2.10"), 
    2 : generic_station(2, "192.168.2.20"), 
    3 : generic_station(3, "192.168.2.30"), 
    5 : station5(5, "192.168.2.50"), 
    6 : generic_station(6, "192.168.2.60"), 
    7 : station7(7, "192.168.2.70"), 
}


#Classe com todos os atributos do processo como um todo
class process(thread_):

    ThreadsStorage = []
    ThreadsAssemble = []
    stopFlag = False

    def __init__(self) -> None:
        super().__init__(self)
        self.daemon = True
        pass

    # @staticmethod
    #Verifica o status de uma estação escolhida, gerando um código que indicará a sua situação.
    #                                       Legenda
    # #   - Inicio do código
    # X   - Número da respectiva estação
    # T/F - Estação iniciada
    # T/F - Estação parada
    # T/F - Estção em processo
    # I/O/F - Estação em modo entrada (I), saída(O) ou sem direção (F)
    def status(self, station):
        temp_bits = station.readBits(0, 6)

        started = "T" if temp_bits[0] else "F" 
        stop = "T" if temp_bits[1] else "F" 
        process_ = "T" if temp_bits[2] else "F" 

        if temp_bits[3] : direction = "I"   
        elif temp_bits[4] : direction = "O"
        else: direction = "F"    

        return "#{}{}{}{}{}".format(station.clpNumber,started,stop,process_,direction)        
    
    # @staticmethod
    #Verifica se alguma estação está em processo, e gera uma lista de status básico de todas as estações
    #                           retorna
    # 0 - True : Se a planta estiver livre e sem processos / False :  Se houver uma estação em processo
    # 1 - []   : Retorna a lista do status de todas as estações
    # 2 - []   : Retorna a lista de status apenas das estações em processo
    def process(self):
        stationsInProcess = []
        status = []
        for num in stations:
            tempStatus = self.status(stations[num])
            status.append(tempStatus)
            if tempStatus[4] == "T":
                stationsInProcess.append(tempStatus)

        if stationsInProcess == []:
            return True, status
        else:
            return False, status , stationsInProcess 
    
    # @staticmethod
    #Verifica qual a direção atual que a planta está operando
    #                   retorna
    # False      : Caso não tenha uma direção definida (Acontece se a estações não estiverem sincronizadas)
    # "storage"  : Caso a estação esteja no modo armazenamento (storage)
    # "assemble" : Caso a estação esteja no modo de montagem (assemble) 
    def defineDirection(self, var):
        var = var[1]

       #Analisa as unicas estações que precisam de direção
        if var[2][5] == var[4][5] and var[4][5] == var[5][5]:
            pass
        else: return False

        return "storage" if var[2][5] == "I" else "assemble"


    # @staticmethod
    #Define uma direção para a planta atuar (Esse método deve ser chamado através do método direction()!)
    #                       retorna
    # 0 : bool : 
    #            True - Caso a planta já esteja no sentido desejado
    #                   Caso a planta entre no modo desejado
    #
    #            False - Caso alguma estação já esteja em processo 
    #                    Comando desconhecido
    #
    # 1 : []   : Lista de menssagen para a confecção do log (Através dela é possível saber tudo que aconteceu no processo)
    def direction_(self, flow):
        messages_list = []
        process_ =  self.process()
        actualDirection =self.defineDirection(process_)
        
        messages_list.append("Actual direction: {}".format(actualDirection))
        messages_list.append("Command: direction - {}".format(flow))
        messages_list.append("Stations status: {}".format(process_[1]))

        if actualDirection == flow:
            if actualDirection == "storage":
                stations[1].startStation()
                if self.ThreadsStorage == []:
                    self.ThreadsStorage.append(stations[7].start())#Roda a thread da estação 7 que verifica a entrada de peças
            else:
                if self.ThreadsStorage == []:
                    self.ThreadsStorage.append(stations[5].start())#Roda a thread da estação 5 que verifica a saída de peças
            status = "#XS10" if actualDirection == "storage" else "#XS11"
            messages_list.append(status)
            return True , messages_list
        
        if not process_[0] :
            print(process_[1])
            status = "#XE08"
            messages_list.append(status)
            return False , messages_list  #"Alguma estação está em processo, aguarde para fazer um novo chamado"
        
        print(process_[1])
        # print (actualDirection)
        
        if flow == "storage":
            if self.ThreadsAssemble != []: 
                status = self.killThread(process.ThreadsAssemble, "5")
                messages_list.append(status)
            messages_list.append(stations[5].stopStation()[1])
            stations_to_command = [1,2,3,6,7]
            for num in stations_to_command:
                messages_list.append(stations[num].startStation()[1])
                messages_list.append(stations[num].input()[1])
            status = "#XS0E"
            messages_list.append(status)
            self.ThreadsStorage.append(stations[7].start())#Roda a thread da estação 7 que verifica a entrada de peças
            status = "#7S13"
            messages_list.append(status)
            return True, messages_list# "Processo em modo de armazenamento."

        elif flow == "assemble":
            if self.ThreadsAssemble != []: 
                status = self.killThread(process.ThreadsAssemble , "7")
                messages_list.append(status)
            messages_list.append(stations[1].stopStation()[1])
            messages_list.append(stations[2].stopStation()[1])
            stations_to_command = [3,5,6,7]
            for num in stations_to_command:
                messages_list.append(stations[num].startStation()[1])
                messages_list.append(stations[num].output()[1])
            status = "#XS0E"
            messages_list.append(status)
            self.ThreadsStorage.append(stations[5].start())#Roda a thread da estação 5 que verifica a saída de peças
            status = "#5S13"
            messages_list.append(status)
            return True, messages_list # "Processo em modo de montagem."

        else:
            status = "#XE05"
            messages_list.append(status)
            return False , messages_list #"Tipo de processo desconhecido."
    
    # @staticmethod
    #Inicia a montagem de uma cor espessífica
    #               retorna 
    # 0 : bool : 
    #            True - Pedido de montagem feito com sucesso
    #            
    #            False - Cor escolhida não existe
    #                    A planta não está em modo montagem (assemble)
    #
    # 1 : []   : Lista de menssagen para a confecção do log (Através dela é possível saber tudo que aconteceu no processo)
    def assemblyColor_(self, color):
        messages_list = []
        process_ =  self.process()
        actualDirection = self.defineDirection(process_)

        messages_list.append("Command: assemblyColor - {}".format(color))
        messages_list.append("Stations status: {}".format(process_[1]))

        if actualDirection == "assemble":
            acceptColors = ["BLACK" , "RED" , "SILVER"]
            if color.upper() in acceptColors:
                stations[7].outputStartWithColor(color)
                status = "#XS0D"
                messages_list.append(status)
                if self.ThreadsStorage == []:
                    self.ThreadsStorage.append(stations[5].start())
                return True , messages_list
            else:
                print("Erro na cor escolhida, verifique a string e tente novamente.\nCores aceitas : {}".format(acceptColors))
                status = "#XE06"
                messages_list.append(status)
                return False , messages_list    
        else:
            print("Para efetuar a montagem de uma peça, o processo deve estar em modo montagem (assemble).")
            status = "#XE07"
            messages_list.append(status)
            return False , messages_list

    # @staticmethod
    #Define a direção e cria o log
    def direction(self, flow):
        resp = self.direction_(flow)
        self.makeLog(resp[1])
        return resp
    
    # @staticmethod
    #Faz o pedido da cor e cria o log
    def assemblyColor(self ,color):
        resp = self.assemblyColor_(color)
        self.makeLog(resp[1])
        return resp
    
    # @staticmethod
    #Cria o log em um arquivo TXT
    def makeLog(self, info):
        path = "{}\{}".format(os.getcwd(), "logs.txt")
        logs = open(path , 'r')
        conteudo = logs.readlines()
        for i in info:
            conteudo.append("{} : {}\n".format(datetime.datetime.now() , i))
        conteudo.append("---------------------------\n")
        logs = open(path , 'w')
        logs.writelines(conteudo)
        logs.close()

    # @staticmethod
    #Retorna todos os status que essa classe criou, para ser enviado para a API
    def allStatus(self):
        status = []
        process_ = self.process()
        status.append(process_)
        actualDirection = self.defineDirection(process_)
        status.append(actualDirection)
        return status

    # @staticmethod
    #Sanaliza quando uma peça entrou na estação 7 e a sua cor está disponível para ser capturada no MODBUS
    def readColorsStorage(self):
        return stations[7].readColorsStorage()
    
    # @staticmethod
    #Finaliza todas as threads relativas ao modo entrada ou saída
    def killThread(self, listThreadToKill , num = "X"):
        for threadKill  in listThreadToKill:
            threadKill.stopThread()
            threadKill.join()
        status = "#{}S14".format(num)
        return status

    def run(self):
        while True:
            if self.stopFlag: break
            status = self.allStatus()
            print(status)
            time.sleep(self.temp)

if __name__ == "__main__":

    teste = process()
    teste.direction("assemble")
    # stations[1].stopStation()
    # self.direction("storage")
    teste.assemblyColor("black")
    # time.sleep(15)
    # self.assemblyColor("red")
    # time.sleep(15)
    # self.assemblyColor("silver")
    # time.sleep(15)
    while True:
        pass