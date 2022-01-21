#Classe que define os pedidos feitos para a central
class order:

    status = ""

    def __init__(self, type, properties = []) -> None:
        self.type = type
        self.properties = properties
    
    def start_order(self):
        if self.type == "assemble":
            pass
        elif self.type == "storage":
            pass
        else:
            #error
            pass

    def status_order(self):
        pass