from threading import Thread
import time

class myClassA(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        
    def run(self):
        while True:
            time.sleep(1)
            print ('A')



x = myClassA()
time.sleep(10)
x.start()
while True:
    print("teste")
    time.sleep(2)