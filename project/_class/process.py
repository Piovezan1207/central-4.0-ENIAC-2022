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
    

class process:

    station1_ = station1(1, "192.168.2.10")
    station2_ = generic_station(2, "192.168.2.20")
    station3_ = generic_station(3, "192.168.2.30")
    station5_ = generic_station(5, "192.168.2.50")
    station6_ = generic_station(6, "192.168.2.60")
    station7_ = station7(7, "192.168.2.70")

    stations = [
        station1_,
        station2_, 
        station3_, 
        station5_, 
        station6_, 
        station7_, 
        ]

    actualDirection = ""

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
        for num in process.station:
            tempStatus = process.status(num)
            if tempStatus[4] == "T":
                stationsInProcess.append(tempStatus)

        if stationsInProcess == []:
            return True, False
        else:
            return False, stationsInProcess

    @staticmethod
    def direction(flow):
        if process.actualDirection == flow: return True
        
        process_ =  process.process()
        if process.actualDirection == "" and not process_[0]:
            return "Alguma estação está em processo, aguarde para fazer um novo chamado"
        
        if flow == "storage":
            for i in process.stations:
                pass
        elif flow == "assemble":
            pass

        else:
            pass #Algum estação já está em processo
    

print(process.status(3))