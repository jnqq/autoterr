from gpiozero import LED
class Led(object):
	def __init__(self):
		self.red = LED(16)
		self.pointer = False
	def On(self):
		self.red.on()
		self.pointer = True
	def Off(self):
		self.red.off()
		self.pointer = False

