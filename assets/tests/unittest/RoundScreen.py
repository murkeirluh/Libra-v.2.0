from __future__ import print_function
import sys
import Tkinter as tk
import tkFont

from colors import *
import Mainscreen

# debug variable (default: False)
debug = True

# debug function
def _debug(*args, **kwargs):
    if debug:
    	print("[DEBUG]", *args, file=sys.stderr, **kwargs)

class __RoundScreen__(tk.Frame):
	def __init__(self, control, _round, master=None):
		tk.Frame.__init__(self, master, bg=light)
		self.round = _round
		self.roundName = self.round.getName()
		self.control = control
		self.master.title(self.roundName)
		_debug("RoundScreen ", self.round.getName(), " in states.")

		## fonts ##
		self.main_font = tkFont.Font(self, family='Code Bold', size=30)
		self.button_font = tkFont.Font(self, family='Consolas', size=15)

	def load(self):
		_debug(self.round.getName() + " screen loaded.")
		self.control.log(str(self.round.getName() + " start."))
		self.roundText = tk.Label(self, text=self.roundName, font=self.main_font, justify=tk.CENTER, relief=tk.FLAT, padx=50, pady=20, anchor=tk.CENTER, fg=light_txt, bg=light)
		self.roundText.grid(row=0)
		self.startButton = tk.Button(self, text='START',font=self.button_font, command=self.__callMainscreen, bg=dark, fg=light)
		self.startButton.grid(row=1, column=0 ,sticky=tk.E)
		self.grid()
		
	def __callMainscreen(self):
		self.quit()
		self.destroy()
		self.control.states.append(Mainscreen.__MainScreen__(self.control, self.round))
		self.control.states.remove(self)