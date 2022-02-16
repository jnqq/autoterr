import threading
from datetime import datetime

def dayTime(start, end, actual):
    if start <= end:
        return start <= actual <= end
    else:
        return start <= actual or actual <=end

def monitoring(sen, plug, csvdata, display, fan, atom):
    sensors_data = []
    while True:
        sensors_data = sen.getData()
        display.lcd_display_string("Temp.:" + str(sensors_data[0][1]) + " ^C" + " ruch",  1)
        display.lcd_display_string("Wilg.:" + str(sensors_data[0][0]) + " %" + "     " + str(sen.motion()), 2)

        with open('/home/pi/github/webpage/web/.txts/set.txt', 'r') as f:
            set_data = f.read().splitlines()

        night = datetime.strptime(set_data[4], '%H:%M:%S')
        day = datetime.strptime(set_data[3], '%H:%M:%S')
        actual = datetime.strptime(sensors_data[1], '%H:%M:%S')

        if dayTime(day.time(), night.time(), actual.time()):
            setTemperature = set_data[0]
        else:
            setTemperature = set_data[1]

        plug.raiseTemp(int(setTemperature), int(sensors_data[0][1]))
        fan.lowTemp(int(setTemperature), int(sensors_data[0][1]))
        atom.increasehum(int(set_data[2]), int(sensors_data[0][0]))
        csvdata.process(sensors_data[0])
        csvdata.motioncsv(sen.motion(), sensors_data[1], sensors_data[2], sensors_data[3], sensors_data[4])

def startmonit(sen, plug, csvdata, display, fan, atom):
    t1 = threading.Thread(target=monitoring, args=(sen, plug, csvdata, display, fan, atom))
    t1.start()

