from __future__ import print_function
from collections import deque
import sys
import Tkinter as tk
import tkFileDialog, tkFont, tkMessageBox
from PIL import Image, ImageOps, ImageDraw, ImageTk

from classTimer import *
from classQueue import *
from classRound import *
from classContestant import *
from classController import *

from classEditRounds import *
from classActivityLog import *
from classEditContestants import *
from classBuzzerTest import *

import StartupScreen, RoundScreen, Mainscreen

from colors import *

debug = True

def _debug(*args, **kwargs):
    if debug:
    	print("[DEBUG]", *args, file=sys.stderr, **kwargs)

# driver class
class Libra:
	def __init__(self, control):
		self.root = control.root
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.control = control
		self.setRounds()
		self.setupNavi()

	def load(self):
		self.control.states[0].load()
		self.control.states[0].mainloop()

	def unload(self):
		self.control.states.pop(0)
		if len(self.control.states) == 0:
			quit()

	def setRounds(self):
		self.control.rounds = [Round(i+1) for i in range(self.control.roundCount)]

		# set up prefinal and wildcard rounds
		for p in range(3):
			self.control.rounds[p].setName("Prefinal Round " + str(p+1))
			self.control.rounds[p].setNum(p+1)
			self.control.rounds[p].setCCount(6)
		self.control.rounds[3].setName("Wildcard Round")
		self.control.rounds[3].setNum(4)
		self.control.rounds[3].setCCount(6)

		for p in range(4):
			index = 0
			for num in range(5, 0, -1):
				for i in range(num):
					self.control.rounds[p].setPoints(index, 2*(6-num))
					index += 1

		# set up final round
		self.control.rounds[4].setName("Final Round")
		self.control.rounds[4].setNum(5)
		self.control.rounds[4].setQCount(20)
		self.control.rounds[4].setCCount(4)
		index = 0
		for num in range(6, 1, -1):
			for i in range(num):
				self.control.rounds[4].setPoints(index, 2*(7-num))
				index += 1

		self.control.roundSetup = False

	# set contestants for modification
	def setContestants(self):
		i = 0
		for r in range(self.control.roundCount):
			current = self.control.rounds[r]
			self.control.contestants_info += [Contestant(j+1, self.control) for j in range(current.getCCount())]
			for ctr in range(current.getCCount()):
				self.control.contestants_info[i].setRound(current)
				i += 1
		self.control.contestantSetup = True

	def setupNavi(self):
		self.control.navigation.append(EditRoundsScreen(self.control))
		self.control.navigation.append(RoundListScreen(self.control))
		self.control.navigation.append(BuzzerTestScreen(self.control))
		self.control.navigation.append(ActivityLogScreen(self.control))

	def on_closing(self):
		if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?", parent=self.root):
			self.control.log("Window closed.")
			self.root.destroy()
			quit()

if __name__ == '__main__':
	# controller variable
	control = Controller()
	control.root.update_idletasks()
	x = (control.root.winfo_screenwidth()) - (control.root.winfo_screenwidth() / 2) - control.root.winfo_width() - 30
	y = control.root.winfo_screenheight() - (control.root.winfo_screenheight() / 2) - control.root.winfo_height() - 20
	control.root.geometry('+'+str(x)+'+'+str(y))
	control.root.columnconfigure(0, weight=2)
	control.root.rowconfigure(0, weight=2)
	control.root.resizable(True, True)

	LIBRA = Libra(control)
	control.states.append(StartupScreen.__StartupScreen__(control))
	control.root.wm_deiconify()
	LIBRA.load()

	if control.roundSetup == True:
		LIBRA.setContestants()
		for i in range(control.roundCount):
			_debug(control.states)
			control.states.append(RoundScreen.__RoundScreen__(control, control.rounds[i]))
			LIBRA.load()
			LIBRA.load()
