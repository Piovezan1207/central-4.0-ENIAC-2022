import time
import sys
import json

try:
    from generic_station import generic_station
except:
    from project.program_class.stations_class.generic_station import generic_station

class station5(generic_station):

    def __init__(self,clpNumber  , ip , temp = 5 , port = 502, useOrderList = False) -> None:
        super().__init__(clpNumber, ip , temp, port , useOrderList)
        self.temp = temp
        self.pauseThread = False
        self.start()

    def confirmProcess(self):
        if self.readBits(6 , 1)[0]:
            B = self.readBits(6 , 12)
            self.pulseBit(6)
            
            return True , B
        else:
            return False , False

    def binaryToInt(self, binaryList):
            val = 0
            val += int(binaryList[0]) * 1
            val += int(binaryList[1]) * 2
            val += int(binaryList[2]) * 4
            return val


    def run(self):
        while True:
            if self.stopFlag: break

            if not self.pauseThread:
                self.isRunning = True
                resp = self.confirmProcess()

                if resp[0]:

                    color = { "BLACK" : self.binaryToInt(resp[1][1:4]),
                              "SILVER" : self.binaryToInt(resp[1][4:7]),
                              "RED" : self.binaryToInt(resp[1][7:10] ),
                            }

                    #Verifica as peças que foram finalizadas e para quais ordens pertencem
                    for colorName in color: #Para cada cor da color{}
                        for num in range(color[colorName]):#Para cada cor, esse for rodará o número de peças processadas
                            reversedOrderList = list(reversed(self.order_list)) #Inverte a lista, para que o primeiro pedido esteja na ultima posição.
                                                                                #   Isso é feito pois a lista será rodada invertida.
                            for orderNum in range(len(reversedOrderList)-1, -1 , -1):#Para cada ordem existente na order_list[]
                                print(orderNum, reversedOrderList[orderNum].properties["color"] , reversedOrderList[orderNum].status)

                                if reversedOrderList[orderNum].status == True: #Caso o pedido tenha sido padssado para a planta com sucess

                                    if reversedOrderList[orderNum].properties["color"] == colorName: #Verifica se a cor processada bate com alguma ordem
                                        message = json.dumps({ #Caso bata, cria a JSON de finalização da order
                                                "type" : "finishedAssembly",
                                                "properties" : {
                                                    "id" : reversedOrderList[orderNum].orderId,
                                                    "color" : colorName,
                                                    "startDateTime" : reversedOrderList[orderNum].startOrderTime,
                                                    "finishDateTime" : str(time.ctime())
                                                },
                                            })
                                        print(message)
                                        self.threadPublishMQTT("teste" , message) #Envia a informação que essa ordem foi finalizada, por MQTT
                                        reversedOrderList.pop(orderNum) #Remove do Order_list
                                        self.order_list = list(reversed(reversedOrderList)) #Iverte a lista, voltando para sua ordem original e salva no order_list.
                                        self.saveOrderList() #Salva os objetos nos arquivos
                                        break #Quebra o loop de verificação dessa cor


                                #Faz a remoção de pedidos inválidos encontrados
                                elif reversedOrderList[orderNum].status == False: #Caso o pedido não tenha sido feito com sucesso a planta, o mesmo
                                                                                    #deve ser apenas ignorado e removido da lista, pois está "perdido" nela, já que não servirá para nada
                                    print("Removendo order False na finalização da 5" , reversedOrderList[orderNum].orderId)
                                    reversedOrderList.pop(orderNum) #Remove do Order_list
                                    self.order_list = list(reversed(reversedOrderList)) #Iverte a lista, voltando para sua ordem original e salva no order_list.
                                    self.saveOrderList() #Salva os objetos nos arquivos
                                    #Como não tem um break, ele continuará rodando o vetor a procura de um pedido válido

                    for i in  self.order_list:
                        print("Ordem estação 5 " , i.properties["color"])

                else:
                    print("Thread 5 - rodando")
                    # if self.order_list == []: self.pauseThread_()
                    time.sleep(self.temp)
            else:
                self.isRunning = False



