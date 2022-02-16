import RPi.GPIO as GPIO
import time
class Atom(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26,GPIO.OUT)
        GPIO.output(26, GPIO.LOW)
        self.isOn = False

    def increasehum(self, newhum, current):
        if current >= newhum:
            if self.isOn:
                self.isOn = False
                GPIO.output(26,GPIO.LOW)
        else:
            if not self.isOn:
                self.isOn = True
                GPIO.output(26, GPIO.HIGH)



