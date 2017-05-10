from __future__ import print_function
from collections import deque
import sys, datetime # winsound
import Tkinter as tk
import tkFileDialog, tkFont, tkMessageBox
from PIL import Image, ImageOps, ImageDraw, ImageTk
from colors import *
import time

debug = True
logtofile = True

a = "logs/activitylog"
b = ".txt"
timestr = time.strftime("%Y%m%d")
a = a + timestr + b
logfile = open(a, "a")

def _debug(*args, **kwargs):
	if debug:
		print("[DEBUG]", *args, file=sys.stderr, **kwargs)

def log(*args, **kwargs):
	if logtofile:
		print("[" + str(datetime.datetime.now()) + "]", *args, file=logfile, **kwargs)

#########		  QUEUE 		  #########

class Queue(deque):
	def __init__(self, maxlen):
		# for ordinary game queue
		if maxlen > 0:
			deque.__init__(self, maxlen=maxlen)
		# for infinite buzzing queue (no maxlen)
		else:
			deque.__init__(self)
		self.preTimerBuzzing = False
		self.buzzCount = 0

	def _print(self):
		log("Queue: ")
		sys.stderr.write("[DEBUG] Queue: ")
		if (len(self)):
			for i in range(len(self)):
				log(str(self[i].getNum()) + " ")
				sys.stderr.write(str(self[i].getNum()) + " ")
		else: sys.stderr.write("Empty")
