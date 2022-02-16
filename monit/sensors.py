import Adafruit_DHT
import time
from datetime import datetime
import RPi.GPIO as GPIO
class Sensors(object):
	def __init__(self):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(20, GPIO.IN)
		GPIO.setup(23, GPIO.IN)
		self.weekdays = ["Poniedzialek", "Wtorek", "Sroda", "Czwartek", "Piatek", "Sobota", "Niedziela"]
		self.oldtime = time.time()
		humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
		self.dhtresult = int(humidity), int(temperature)

	def dht(self):
		if not time.time() - self.oldtime <= 5:
			humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
			if humidity is not None and temperature is not None:
				self.dhtresult = int(humidity), int(temperature)
				self.oldtime = time.time()
				return self.dhtresult
			else:
				return self.dhtresult
		else:
			return self.dhtresult

	def smoke(self):
		if GPIO.input(23):
			return "0"
		else:
			return "1"

	def motion(self):
		if GPIO.input(20):
			return 1
		else:
			return 0

	def getData(self):
            time.sleep(0.5)
            current_time = datetime.now()
            info = []
            info.append(self.dht()[0])
            info.append(self.dht()[1])
            info.append(current_time.strftime("%H:%M"))
            info.append(self.weekdays[current_time.weekday()])
            info.append(current_time.strftime("%d"))
            info.append(current_time.month)
            info.append(current_time.strftime("%Y"))

            with open('/home/pi/github/webpage/web/.txts/actual.txt', 'w') as f:
                for element in info:
                    f.write(str(element) + '\n')

            return info, current_time.strftime('%H:%M:%S'), current_time.strftime('%d'), current_time.strftime('%m'), current_time.strftime('%Y')

