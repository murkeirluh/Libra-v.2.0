from __future__ import print_function
from collections import deque
import sys, datetime # winsound
import Tkinter as tk
import tkFileDialog, tkFont, tkMessageBox
from PIL import Image, ImageOps, ImageDraw, ImageTk
from colors import *
import time

# conditional import of winsound
is_windows_os = True
try:
	import winsound
except ImportError:
	is_windows_os = False

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



class Controller:
	def __init__(self):
		# main window
		self.root = tk.Tk()
		self.root.wm_withdraw()
		# array of states/screens
		self.states = []
		# array of navigation screens
		self.navigation = []
		# states of navigation screens
		self.navi_states = []
		# variable for number of rounds
		self.roundCount = 5
		# variable for number of contestants
		self.contestantCount = 28
		# status of round setup
		self.roundSetup = False
		# status of contestants setup
		self.contestantSetup = False

		self.preTimerBuzzing = True
		# main contestants array
		self.contestants = []
		# contestants array for modifiying info
		self.contestants_info = []
		# rounds array
		self.rounds = []
		# winners array
		self.winners = []
		#clinchers array
		self.clinchers = []
		# window title
		self.title = "Libra v.2.0"
		# toggle for activity log (default: True)
		self.logtofile = True
		# activity log file
		self.logfile = ""
		# start log if logging is true
		self.log_driver()
		self.counter = 0
		# if default rounds are set
		self.default_rounds = True

	# log function
	def log(self,*args, **kwargs):
		if self.logtofile:
			a = "logs/activitylog"
			b = ".txt"
			timestr = time.strftime("%Y%m%d")
			a = a + timestr + b
			self.logfile = open(a, "a")
			print("[" + str(datetime.datetime.now()) + "]", *args, file=self.logfile, **kwargs)
			if debug: print("[DEBUG]", *args, file=sys.stderr, **kwargs)
			# self.logfile.write("[" + str(datetime.datetime.now()) + "] ")
			# self.logfile.write(*args)
			# self.logfile.write("\n")
			self.logfile.close()

	def quit(self):
		self.log("App closed.")
		if self.logtofile:
			self.logfile.write("===============================\n")
			self.logfile.close()
		exit()

	def log_driver(self):
		if self.logtofile:
			a = "logs/activitylog"
			b = ".txt"
			timestr = time.strftime("%Y%m%d")
			a = a + timestr + b
			self.logfile = open(a, "a")
		# log start of file
		self.log("===============================")
		self.log("LIBRA v. 2.0 START.")
		self.log("Activity logging: " + str(self.logtofile))

	def loadNavi(self, i):
		self.navigation[i].load()
		#self.navigation[i].mainloop()

	def get_count(self):
		print("Counter:", self.counter)
		return self.counter
