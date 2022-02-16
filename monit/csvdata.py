import csv
from os.path import exists
import time
class Csv(object):
	def __init__(self):
            self.csvpath = "/home/pi/github/webpage/web/.txts/dane.csv"
            self.motionpath = "/home/pi/github/webpage/web/.txts/motion.csv"
            self.temptxtpath = "/home/pi/github/webpage/web/.txts/last_motion.txt"
            self.headerList = ["wilgotnosc", "temperatura", "godzina","dzientyg","dzienmsc","miesiac","rok"]
            self.motionheader = ["Ruch", "godzina", "dzien", "miesiac", "rok"]
            self.before = time.time()
            self.oldtime = time.time()

	def process(self, data):
            if not exists(self.csvpath):
                self.createfile(self.csvpath, self.headerList)
            after = time.time()
            if after - self.before >= 1800:
                with open(self.csvpath, 'a') as f:
                    write = csv.writer(f)
                    write.writerow(data)
                    self.before = time.time()

	def createfile(self, path, header):
            with open (path, 'w') as f:
                write = csv.writer(f)
                write.writerow(header)
                return 0

	def motioncsv(self, motion, clock, day, month, year):
            if not exists(self.motionpath):
                self.createfile(self.motionpath, self.motionheader)
            motionlist = []
            if motion == 1:
                motionlist.append(motion)
                motionlist.append(clock)
                motionlist.append(day)
                motionlist.append(month)
                motionlist.append(year)
                with open (self.motionpath, 'a') as f:
                    write = csv.writer(f)
                    write.writerow(motionlist)
                with open(self.temptxtpath, 'w') as f:
                    f.write(clock)
            return 0

