import threading
from datetime import datetime
class Monit(object):
    def __init__(self, sen, plug, csvdata, display, fan):
        self.sen = sen
        self.plug = plug
        self.csvdata = csvdata
        self.display = display
        self.sensors_data = []
        self.fan = fan
    
    def dayTime(self, start, end, actual):
        if start <= end:
            return start <= actual <= end
        else:
            return start <= actual or actual <=end

    def threadfunction(self):
        while True:
            self.sensors_data = self.sen.getData()
            self.display.lcd_display_string("Temp.:" + str(self.sensors_data[0][1]) + " ^C" + " ruch",  1) 
            self.display.lcd_display_string("Wilg.:" + str(self.sensors_data[0][0]) + " %" + "     " + str(self.sen.motion()), 2) 

            with open('/home/pi/github/webpage/web/.txts/set.txt', 'r') as f:
                set_data = f.read().splitlines()
            
            night = datetime.strptime(set_data[4], '%H:%M:%S')
            day = datetime.strptime(set_data[3], '%H:%M:%S')
            actual = datetime.strptime(self.sensors_data[1], '%H:%M:%S')
            
            if self.dayTime(day.time(), night.time(), actual.time()):
                setTemperature = set_data[0]
            else:
                setTemperature = set_data[1]

            self.plug.raiseTemp(int(setTemperature), int(self.sensors_data[0][1]))
            self.fan.lowTemp(int(setTemperature), int(self.sensors_data[0][1]))
            self.csvdata.process(self.sensors_data[0])
            self.csvdata.motioncsv(self.sen.motion(), self.sensors_data[1])	
	
    def start(self):
        t1 = threading.Thread(target=self.threadfunction)
        t1.start()

