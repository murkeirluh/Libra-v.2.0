import Tkinter as tk
import tkFileDialog, tkFont, tkMessageBox
from PIL import Image, ImageOps, ImageDraw, ImageTk

import RoundScreen, Mainscreen
from classRound import *
from colors import *

class __Libra__:
	def __init__(self, control):
		self.root = control.root
		self.control = control
		self.setRounds()

	def load(self):
		#self.control.states[0].load()
		#self.control.states[0].mainloop()
		#self.current = self.control.states[self.counter]
		#self.control.states.append(item)
		self.control.counter += 1

	def unload(self):
		self.control.states.pop(0)

	def setRounds(self):
		self.control.rounds = [Round(i+1) for i in range(self.control.roundCount)]
		# set up prefinal and wildcard rounds
		for p in range(3):
			self.control.rounds[p].setName("Prefinal Round " + str(p+1))
			self.control.rounds[p].setCCount(6)
		self.control.rounds[3].setName("Wildcard Round")
		self.control.rounds[3].setCCount(6)

		for p in range(4):
			index = 0
			for num in range(5, 0, -1):
				for i in range(num):
					self.control.rounds[p].setPoints(index, 2*(6-num))
					index += 1

		# set up final round
		self.control.rounds[4].setName("Final Round")
		self.control.rounds[4].setQCount(20)
		self.control.rounds[4].setCCount(4)
		index = 0
		for num in range(6, 1, -1):
			for i in range(num):
				self.control.rounds[4].setPoints(index, 2*(7-num))
				index += 1

		self.control.roundSetup = True