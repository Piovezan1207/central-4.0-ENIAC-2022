
try:
    from process import process
except:
    from project._class.process import process


#Classe que define os pedidos feitos para a central
class order:

    status = ""

    def __init__(self, type, properties = None) -> None:
        self.type = type
        self.properties = properties
        self.start_order()
    
    def start_order(self):
        if self.type == "assemble":
            process.direction(self.type)
            process.assemblyColor(self.properties)
        elif self.type == "storage":
            process.direction(self.type)
            pass
        else:
            print("Tipo desconhecido")
            #error
            pass

    def status_order(self):
        pass