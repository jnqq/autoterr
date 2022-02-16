import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
import threading

class Camera(object):
	def __init__(self):
		self.vc = PiVideoStream(resolution=(640,480), framerate = 30).start()
		self.pcp = '/home/pi/github/webpage/web/.txts/pics_counter.txt'
		self.vcp = '/home/pi/github/webpage/web/.txts/vids_counter.txt'
		self.picsFolder = '/home/pi/github/webpage/web/Pictures/screenshot'
		self.vidsFolder = '/home/pi/github/webpage/web/Videos/video'
		self.fourcc = cv2.VideoWriter_fourcc(*'H264')
		time.sleep(2.0)

	def generate(self):
		while True:
			frame = self.vc.read()
			ret, jpeg = cv2.imencode('.jpg', frame)
			img = jpeg.tobytes()
			yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')

	def takescreen(self):
		with open(self.pcp,'r') as f:
			counter = f.read()
		image = self.vc.read()
		counter = int(counter) + 1
		cv2.imwrite(self.picsFolder+str(counter)+'.jpg', image)
		with open (self.pcp, 'w') as f:
			f.write(str(counter))

	def recordingg(self, rtime):
		with open(self.vcp, 'r') as f:
			counter = f.read()
		out = cv2.VideoWriter(self.vidsFolder+str(counter)+'.mp4', self.fourcc, 30, (640, 480))
		oldtime = time.time()
		counter = int(counter) + 1
		while time.time() - oldtime <= rtime:
			cv2.waitKey(21)
			frame = self.vc.read()
			out.write(frame)
		out.release()
		with open(self.vcp, 'w') as f:
			f.write(str(counter))

	def recording(self, rtime):
		x = threading.Thread(target = self.recordingg, args = (rtime,))
		x.start()
		return 0


