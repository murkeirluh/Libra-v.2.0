from __future__ import print_function
from PIL import ImageTk, Image
import sys
import Tkinter as tk
import tkFont, tkMessageBox
from Tkinter import Text
import time

from classTimer import *
from classQueue import *
from classRound import *
from classContestant import *
from classController import *

from colors import *

#conditional import of winsound
is_windows_os = True
try:
	import winsound
except ImportError:
	is_windows_os = False

#### BUZZER TEST SCREEN ####
class BuzzerTestScreen(tk.Frame):
	def __init__(self, control):
		self.root = tk.Tk()
		self.root.wm_withdraw()
		tk.Frame.__init__(self, self.root, bd=4, width=800, bg=light)
		self.title = "Buzzer Test"
		self.root.title(self.title)
		self.control = control

		## customization variables ##
		self.main_font = tkFont.Font(self, family='Code Bold', size=28)
		self.label_font = tkFont.Font(self, family='Arial', size=13)
		self.button_font = tkFont.Font(self, family='Consolas', size=13)

		## arrays ##
		self.frames = []
		self.contestants = []

		## frames ##
		for i in range(3):
			self.frames.append(tk.Frame(self))

		## top frame ##
		self.titleOfScreen = tk.Label(self.frames[0], text="Buzzer Test", font=self.main_font, relief=tk.FLAT, justify=tk.LEFT, bg=light, fg=dark)

		## second frame ##
		self.buzzLabel = tk.Label(self.frames[1], text="", bg=light, font=self.label_font, pady=20)
		self.exitButton = tk.Button(self.frames[2], text="Exit", font=self.button_font, command=self.unload, bg=dark, fg=light)

		## contestant variables ##
                self.contestantCount = 6
		self.keys = ['i', ']', 'k', 'p', '[', 'u'] #should be lowercase
                for i in range(self.contestantCount):
                        c = self.keys[i]
                        if c == "":
                          # default contestant keys: ABCDEF
                          self.bind_all(chr(i+65), self._buzz)
                          self.bind_all(chr(i+65).lower, self._buzz)
                        else:
                          self.bind_all(c, self._buzz)
                          self.bind_all(c.upper(), self._buzz)

	# buzz function
	# currently bound to i, k, u, p, [, ]
	def _buzz(self, event):
		i = self.searchKey(event.char)
		self.control.log("[BUZZER TEST] Key pressed:", event.char)
		if i >= 0:
			self.buzz_test(i)

	# returns contestant number whose key was pressed
	# if output < 0, key unassigned to contestant
	def searchKey(self, key):
                if key.lower() in self.keys:
                  return self.keys.index(key.lower())
		return -1

	def buzz_test(self, number):
		if is_windows_os:
			winsound.PlaySound("assets/sounds/"+str(number+1)+".wav", winsound.SND_FILENAME and winsound.SND_ASYNC)
		self.buzzLabel.config(text="Buzzer #" + str(number+1) + " is okay!")
		self.buzzLabel.update()

	# load
	def load(self):
		self.control.log("Buzzer Test")
		self.grid()
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.frames[0].grid(row=0, sticky=tk.W+tk.E)
		self.frames[1].grid(row=1)
		self.frames[2].grid(row=2, sticky=tk.SW)

		self.titleOfScreen.grid(row=0, column=0, sticky=tk.NW)
		self.buzzLabel.grid(row=0, column=0, sticky=tk.E+tk.W)
		self.exitButton.grid(row=0, column=2, sticky=tk.W)
		self.root.wm_deiconify()
		self.mainloop()

	def unload(self):
		#self.grid_remove()
		self.root.wm_withdraw()
		self.buzzLabel.config(text='')
		self.buzzLabel.update()
		self.quit()
