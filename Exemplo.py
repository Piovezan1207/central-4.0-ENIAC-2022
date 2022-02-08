from pymodbus.client.sync import ModbusTcpClient,ModbusUdpClient
import time

client7 = ModbusTcpClient('192.168.2.70',port=502) #estação 7
client6 = ModbusTcpClient('192.168.2.60',port=502) #estação 7
client3 = ModbusTcpClient('192.168.2.30',port=502) #estação 7

x = 32

if x == 0: #Resetar a estação 7 e fazer home
    client7.write_coils(0,[True]*1) #Seta o bit de home
    time.sleep(1)
    client7.write_coils(0,[False]*1) #Reseta o bit de home
    time.sleep(1)

if x == 1:
    #Define sentido de entrada
    # client6.write_coils(1,[False]*1) #Desabilita modo de saida (por garantia pois já deveria estar desabilitado)
    # time.sleep(0.2)
    # client6.write_coils(2,[True]*1)
    # time.sleep(0.2)
    # client6.write_coils(2,[False]*1)
    # time.sleep(0.2)

    #N lembro para q serve
    # client6.write_coils(3,[True]*1)
    # time.sleep(0.2)
    # client6.write_coils(3,[False]*1)

    #Reseta o bit do reset da estação
    client6.write_coils(0,[False]*1)
    #Define sentido de saida
    client7.write_coils(2,[False]*1)  #Desabilita modo de entrada (por garantia pois já deveria estar desabilitado)
    time.sleep(0.2)
    client6.write_coils(1,[True]*1)
    time.sleep(0.2)
    client7.write_coils(1,[False]*1) 

    #Bits dad cores
    client7.write_coils(3,[False]*1)
    client7.write_coils(4,[True]*1)
    client7.write_coils(5,[False]*1)
    
    #Define saída
    # client7.write_coils(2,[True]*1)
    
    #Iniciar processo
    time.sleep(1)
    client7.write_coils(6,[True]*1)
    time.sleep(0.3)
    client7.write_coils(6,[False]*1)
    
    #estação 6
if x == 2:
    #Para tudo
    client6.write_coils(2,[True]*1)
    time.sleep(0.2)
    client6.write_coils(2,[False]*1)
    time.sleep(0.2)
    #Reseta tudo
    client6.write_coils(3,[True]*1)
    time.sleep(0.2)
    client6.write_coils(3,[False]*1)

    #Define como entrada de peças
    # client6.write_coils(1,[False]*1)
    # client6.write_coils(0,[True]*1)

    #Define como saída de peças
    client6.write_coils(0,[False]*1)
    client6.write_coils(1,[True]*1)

### ESTAÇÃO 3

if x == 3: #Modo entrada de peças da estação 3
    client3.write_coils(4,[True]*1) #Seta moto entrada
    client3.write_coils(5,[False]*1) #Reseta modo saida

if x == 4:#modo saída de peças da estação 3
    client3.write_coils(5,[True]*1) #reseta modo entrada
    client3.write_coils(4,[False]*1) #Seta modo saida

if x == 5:#Teste de comunicação
    resultado = client3.read_discrete_inputs(23,1) #Lê o BIT de confirmação (deve estar em False)
    print(resultado.bits[0]) 
    client3.write_coils(6,[True]*1) #manda um pulso para verificar a resposta
    time.sleep(0.1)
    client3.write_coils(6,[False]*1)
    resultado = client3.read_discrete_inputs(23,1) #Lê o BIT de confirmação (deve estar em True)
    print(resultado.bits[0])

c1 = {
      "vermelho" : False,
      "preto" : True,  
      "prata" : False,
      }
c2 = {
      "vermelho" : False,
      "preto" : False,  
      "prata" : True,
      }

def estacao3(tipo):
    if tipo == "entrada":
        client3.write_coils(4,[True]*1) #Seta moto entrada
        client3.write_coils(5,[False]*1) #Reseta modo saida
    elif tipo == "saida":
        client3.write_coils(5,[True]*1) #reseta modo entrada
        client3.write_coils(4,[False]*1) #Seta modo saida
    else:
        print("Erro na string do tipo")


def estacao6(tipo):

    client6.write_coils(2,[True]*1)
    time.sleep(0.2)
    client6.write_coils(2,[False]*1)
    time.sleep(0.2)
    #Reseta tudo
    client6.write_coils(3,[True]*1)
    time.sleep(0.2)
    client6.write_coils(3,[False]*1)

    if tipo == "entrada":
        client6.write_coils(1,[False]*1)
        client6.write_coils(0,[True]*1)
    elif tipo == "saida":
        client6.write_coils(0,[False]*1)
        client6.write_coils(1,[True]*1)
    else:
        print("Erro na string do tipo")



def estacao7(tipo , cor):
    if tipo == "entrada":
        #Define sentido de saida
        client7.write_coils(4,[False]*1)  #Desabilita modo de saida (por garantia pois já deveria estar desabilitado)
        client7.write_coils(3,[True]*1)
        time.sleep(0.1)
        client7.write_coils(3,[False]*1) 
    
        #Iniciar processo
        # time.sleep(1)
        # client7.write_coils(6,[True]*1)
        # time.sleep(0.3)
        # client7.write_coils(6,[False]*1)

    elif tipo == "saida":
       
        print(cor)
        if cor == "preto":
            c1 = True
            c2 = False
        elif cor == "prata":
            c1 = False
            c2 = True
        elif cor == "vermelho":
            c1 = False
            c2 = False

        #Bits dad cores
        client7.write_coils(6,[c1]*1)
        client7.write_coils(7,[c2]*1)
        client7.write_coils(8,[False]*1)

         #Define sentido de saida
        client7.write_coils(3,[False]*1)  #Desabilita modo de entrada (por garantia pois já deveria estar desabilitado)
        client7.write_coils(4,[True]*1)
        time.sleep(0.1)
        client7.write_coils(4,[False]*1) 
        
        #Iniciar processo
        time.sleep(1)
        client7.write_coils(9,[True]*1)
        time.sleep(0.3)
        client7.write_coils(9,[False]*1)

    elif tipo == "reset":
        client7.write_coils(2,[True]*1) #Seta o bit de home
        time.sleep(0.1)
        client7.write_coils(2,[False]*1) #Reseta o bit de home
        time.sleep(0.1)

    elif tipo == "stop":
        client7.write_coils(2,[True]*1) #Seta o bit de home
        time.sleep(0.1)
        client7.write_coils(2,[False]*1) #Reseta o bit de home
        time.sleep(0.1)

    elif tipo == "start":
        client7.write_coils(0,[True]*1) #Seta o bit de home
        time.sleep(0.1)
        client7.write_coils(0,[False]*1) #Reseta o bit de home
        time.sleep(0.1)
    else:
        print("Erro na string do tipo")

# tipo = "entrada"

# estacao3(tipo)
# estacao6(tipo)
# estacao7(tipo , "vermelho")


client2 = ModbusTcpClient('192.168.2.20',port=502) #estação 7


client2.write_coils(2,[True]*1) #Seta o bit de home
# time.sleep(0.1)
# client2.write_coils(2,[False]*1) #Reseta o bit de home
# time.sleep(0.1)