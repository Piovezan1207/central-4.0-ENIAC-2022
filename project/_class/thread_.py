from os import stat
import time
import sys
from threading import Thread

class thread_(Thread):

    stopFlag = False
    pauseThread = False
    isRunning = False

    def __init__(self , temp) -> None:
        Thread.__init__(self)
        self.daemon = True
        self.temp = temp

    def stopThread(self):
        self.stopFlag = True
        self.isRunning = False

    def pauseThread(self, value):
        if value:
            self.pauseThread = True
        else:
            self.pauseThread = False
            

