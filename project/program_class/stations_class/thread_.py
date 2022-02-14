# from os import stat
# import time
# import sys
from threading import Thread

try:
    from ...program_class.mqtt_class.mqttPublish import mqttPublish
except:
    from project.program_class.mqtt_class.mqttPublish import mqttPublish

class thread_(Thread):

    stopFlag = False
    pauseThread = False
    isRunning = False

    def __init__(self , temp, clpNumber) -> None:
        Thread.__init__(self)
        self.daemon = True
        self.temp = temp
        self.clpNumber = clpNumber

    def stopThread_(self):
        self.stopFlag = True
        self.isRunning = False
        status = "#{}S14".format(self.clpNumber)
        return status

    def pauseThread_(self):
        self.pauseThread = True
        status = "#{}S15".format(self.clpNumber)
        return status

    def playThread_(self):
        self.pauseThread = False
        status = "#{}S13".format(self.clpNumber)
        return status
        
    def isRunning_(self):
        return self.isRunning

    def threadPublishMQTT(self, topic, payload):
        id = "ThreadStation{}".format(self.clpNumber)
        mqttPublish.publishMQTT(topic, payload, id)
