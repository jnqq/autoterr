import RPi.GPIO as GPIO
class Fan(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21,GPIO.OUT)
        GPIO.output(21, GPIO.LOW)
        self.isOn = False

    def lowTemp(self, newtemp, current):
        if current <= newtemp:
            if self.isOn:
                self.isOn = False
                GPIO.output(21,GPIO.LOW)
        else:
            if not self.isOn:
                self.isOn = True
                GPIO.output(21, GPIO.HIGH)
