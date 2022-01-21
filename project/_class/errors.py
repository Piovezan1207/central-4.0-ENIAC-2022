

from shutil import ExecError

#Para gatilhar essa excessão, utilizar raise connection_error(clpNumber, clpIp)
class connection_error(Exception):
     def __init__(self, clpNumber, clpIp, testeAddress) -> None:
         message = "O CLP da estação {} não passou no teste de conexão.\nIp do CLP: {}\nBit de teste: {}\nVerifique se o CLP está com o programa correto.".format(clpNumber, clpIp, testeAddress)
         super().__init__(message)