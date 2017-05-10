from __future__ import print_function
from collections import deque
import sys, datetime # winsound
import Tkinter as tk
import tkFileDialog, tkFont, tkMessageBox
from PIL import Image, ImageOps, ImageDraw, ImageTk
from colors import *
import time

global is_windows_os
# conditional import of winsound
is_windows_os = True
try:
	import winsound
except ImportError:
	is_windows_os = False

debug = False
logtofile = True

a = "activitylog"
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


#########		  TIMER 		  #########
class Timer:
	def __init__(self, master, time, queue):
		# font
		self.font = tkFont.Font(family='Code Bold', size=50)
		# time set for the round (constant)
		self.time = time
		# timer variable
		self.timer = self.time
		self._timer = tk.StringVar()
		# id for timer function
		self.id = 0
		# True if the timer has started
		self.ticked = False
		# True if timer is paused
		self.paused = True
		# timer label
		self.label = tk.Label(master, text=str(self.timer), font=self.font, relief=tk.FLAT, width=2, bg=light, fg=red)
		# queue reference
		self.queue = queue
		# sound
		self.sound = "sounds/din.wav"

		## start/stop button ##
		self.start_img = Image.open('images/start.png')
		self.stop_img = Image.open('images/stop.png')
		self._start = ImageTk.PhotoImage(self.start_img)
		self._stop = ImageTk.PhotoImage(self.stop_img)
		self.start_button = tk.Label(master, image=self._start, bg=light)
		self.stop_button = tk.Label(master, image=self._stop, bg=light)

		self.start_button.bind('<ButtonRelease>', self.startTimer)
		self.stop_button.bind('<ButtonRelease>', self.stop)

	def setTimer(self, time):
		self.timer = time
		self._timer.set(time)
		self.label.config(text=self.timer)
		self.label.update()

	# triggers timer start
	def startTimer(self, event):
		if self.ticked == False or self.paused == True:
			self._timer.set(self.time)
			self.timer += 1
			self.ticked = True
			_debug("Timer started.")
			self.start()
		self.paused = False

	def start(self):
		self.timer -= 1
		self.label.config(text=str(self.timer))
		if is_windows_os: winsound.PlaySound(self.sound, winsound.SND_FILENAME and winsound.SND_ASYNC)

		if (self.timer > 0): self.id = self.label.after(1000, self.start)
		if (self.timer == 0):
			self._timer.set(self.time)
			self.label.after_cancel(self.id)
			self.label.config(fg='red')
			if is_windows_os: winsound.PlaySound("sounds/timesup.wav", winsound.SND_FILENAME and winsound.SND_ASYNC)
			_debug("Time is up!")
			self.id = self.label.after(1000, self.reset)

	def stop(self, event):
		# if timer has started, pause timer
		if (self.ticked == True):
			_debug("Timer paused/stopped")
			self.label.after_cancel(self.id)
			self.paused = True

	def reset(self):
		self.ticked = False
		self.paused = True
		self.timer = self.time
		self._timer.set(self.time)
		self.label.config(text=str(self.timer), fg='#DC322F')
		self.label.after_cancel(self.id)
		_debug("Timer reset.")
		self.queue.clear()
		self.queue._print()
		_debug("Queue cleared.")
