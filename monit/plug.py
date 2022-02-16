import time
from PyP100 import PyP100
class Plug(object):
    def __init__(self):
        self.p100 = PyP100.P100('192.168.0.101', 'email', 'passwd')
        self.p100.handshake()
        self.p100.login()
        self.p100.turnOff()
        self.isOn = False

    def raiseTemp(self, newtemp, current):
        if current >= newtemp:
            if self.isOn:
                self.isOn = False
                try:
                    self.p100.turnOff()
                except:
                    self.p100.turnOff()
        else:
            if not self.isOn:
                self.isOn = True
                try:
                    self.p100.turnOn()
                except:
                    self.p100.turnOn()
