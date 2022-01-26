from os import stat
import time
import sys
from threading import Thread

try:
    from process import process, stations
except:
    from project._class.process import process


class VerifyFinishProcessThread(Thread):

    stopFlag = False

    def __init__(self , temp=5) -> None:
        process.confirmProcess()#Roda uma vez o processo, antes de começar a thread
        Thread.__init__(self)
        self.daemon = True
        self.start()
        self.temp = temp

    def run(self):
        while True:
            if self.stopFlag: break
            if process.confirmProcess()[0]:
                sys.stdout.write("Uma peça foi finalizada - OK\n")
                sys.stdout.flush()
            else:
                sys.stdout.write("Nenhuma peça finalizada\n")
                sys.stdout.flush()
                time.sleep(self.temp)

    def stopThread(self):
        self.stopFlag = True



class statusProcessThread(Thread):

    stopFlag = False

    def __init__(self , temp=2) -> None:
        Thread.__init__(self)
        self.daemon = True
        self.start()
        self.temp = temp

    def run(self):
        while True:
            if self.stopFlag: break
            status = process.allStatus()
            print(status)
            time.sleep(self.temp)


x = VerifyFinishProcessThread()
y = statusProcessThread()
# x.stopThread()
# x.join()

while True:
    pass
