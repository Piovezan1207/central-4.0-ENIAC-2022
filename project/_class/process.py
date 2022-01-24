from msilib.schema import Directory
import datetime
import os
try:
    from stations_superclass import stations_superclass
    from generic_station import generic_station
    from station1 import station1
    from station7 import station7
except:
    from project._class.stations_superclass import stations_superclass
    from project._class.generic_station import generic_station
    from project._class.station1 import station1
    from project._class.station7 import station7
    

stations = {
    1 : station1(1, "192.168.2.10"), 
    2 : generic_station(2, "192.168.2.20"), 
    3 : generic_station(3, "192.168.2.30"), 
    5 : generic_station(5, "192.168.2.50"), 
    6 : generic_station(6, "192.168.2.60"), 
    7 : station7(7, "192.168.2.70"), 
}


class process:


    def __init__(self) -> None:
        pass

    @staticmethod
    def status(station):
        temp_bits = station.readBits(0, 6)

        started = "T" if temp_bits[0] else "F" 
        stop = "T" if temp_bits[1] else "F" 
        process_ = "T" if temp_bits[2] else "F" 

        if temp_bits[3] : direction = "I"   
        elif temp_bits[4] : direction = "O"
        else: direction = "F"    

        return "#{}{}{}{}{}".format(station.clpNumber,started,stop,process_,direction)        
    
    @staticmethod
    def process():
        stationsInProcess = []
        status = []
        for num in stations:
            tempStatus = process.status(stations[num])
            status.append(tempStatus)
            if tempStatus[4] == "T":
                stationsInProcess.append(tempStatus)

        if stationsInProcess == []:
            return True, status
        else:
            return False, status , stationsInProcess 

    @staticmethod
    def defineDirection(var):
        var = var[1]

       #Analisa as unicas estações que precisam de direção
        if var[2][5] == var[4][5] and var[4][5] == var[5][5]:
            pass
        else: return False

        return "storage" if var[2][5] == "I" else "assemble"


    @staticmethod
    def direction_(flow):
        messages_list = []
        process_ =  process.process()
        actualDirection = process.defineDirection(process_)
        
        if actualDirection == flow:
            if actualDirection == "storage":
                stations[1].start()
            
            status = "#XS10" if actualDirection == "storage" else "#XS11"
            messages_list.append(status)
            return True , messages_list
        
        if not process_[0] :
            print(process_[1])
            status = "#XE08"
            messages_list.append(status)
            return False , messages_list  #"Alguma estação está em processo, aguarde para fazer um novo chamado"
        
        print(process_[1])
        print (actualDirection)
        
        if flow == "storage":
            messages_list.append(stations[5].stop()[1])
            stations_to_command = [1,2,3,6,7]
            for num in stations_to_command:
                messages_list.append(stations[num].start()[1])
                messages_list.append(stations[num].input()[1])
            status = "#XS0E"
            messages_list.append(status)
            return True, messages_list# "Processo em modo de armazenamento."
        elif flow == "assemble":
            messages_list.append(stations[1].stop()[1])
            messages_list.append(stations[2].stop()[1])
            stations_to_command = [3,5,6,7]
            for num in stations_to_command:
                messages_list.append(stations[num].start()[1])
                messages_list.append(stations[num].output()[1])
            status = "#XS0E"
            messages_list.append(status)
            return True, messages_list # "Processo em modo de montagem."
        else:
            status = "#XE05"
            messages_list.append(status)
            return False , messages_list #"Tipo de processo desconhecido."
    
    @staticmethod
    def assemblyColor(color):
        messages_list = []
        process_ =  process.process()
        actualDirection = process.defineDirection(process_)

        if actualDirection == "assemble":
            acceptColors = ["BLACK" , "RED" , "SILVER"]
            if color.upper() in acceptColors:
                stations[7].outputStartWithColor(color)
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

    @staticmethod
    def direction(flow):
        path = "{}\{}".format(os.getcwd(), "logs.txt")
        logs = open(path , 'r')
        conteudo = logs.readlines()
        
        resp = process.direction_(flow)
        for i in resp[1]:
            conteudo.append("{} : {}\n".format(datetime.datetime.now() , i))
        conteudo.append("---------------------------\n")
        logs = open(path , 'w')
        logs.writelines(conteudo)
        logs.close()
        return resp



# process.direction("assemble")
process.direction("storage")
# stations[7].reset()
# process.assemblyColor("black")
