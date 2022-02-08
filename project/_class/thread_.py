from os import stat
import time
import sys
from threading import Thread

class thread_(Thread):

    stopFlag = False

    def __init__(self , temp) -> None:
        Thread.__init__(self)
        self.daemon = True
        self.temp = temp

    def stopThread(self):
        self.stopFlag = True

