from __future__ import print_function
from PIL import ImageTk, Image
import sys, os
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

debug = True

def _debug(*args, **kwargs):
    if debug:
    	print("[DEBUG]", *args, file=sys.stderr, **kwargs)

#### EDIT CONTESTANTS SCREEN ####
class RoundListScreen(tk.Frame):
	def __init__(self, control):
		## initialization ##
		self.root = tk.Tk()
		self.root.wm_withdraw()
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.root.update_idletasks()
		x = (self.root.winfo_screenwidth()) - (self.root.winfo_screenwidth() / 2) - self.root.winfo_width() - 30
		y = self.root.winfo_screenheight() - (self.root.winfo_screenheight() / 2) - self.root.winfo_height() - 20
		self.root.geometry('+'+str(x)+'+'+str(y))
		tk.Frame.__init__(self, self.root, width=640, height=480, pady=20, bg=light)
		self.title = "Rounds List"
		self.root.title(self.title)
		self.control = control

		## customization variables ##
		self.main_font = tkFont.Font(self, family='Code Bold', size=30)
		self.choice_font = tkFont.Font(self, family='Consolas', size=11)
		self.button_font = tkFont.Font(self, family='Consolas', size=9)

		## arrays ##
		self.rounds = self.control.rounds
		self.buttons = []
		self.elements = []

		# other elements #
		self.header = tk.Label(self, text="Rounds List", font=self.main_font, relief=tk.FLAT, justify=tk.CENTER, anchor=tk.CENTER, padx=20, pady=10, bg=light)
		self.quitButton = tk.Button(self, text="Exit", font=self.button_font, command=self._quit, fg=light,bg=dark,relief=tk.GROOVE, overrelief=tk.RIDGE, bd=4, padx=20, highlightbackground='black', highlightcolor='black', highlightthickness=3)
		self.elements.append(self.header)
		self.elements.append(self.quitButton)

	def onButtonClick(self, i):
		self.control.navi_states[i].load()

	def createButton(self, i):
		temp_button = tk.Button(self, text=self.rounds[i].getName(), state=tk.NORMAL, command=lambda:self.onButtonClick(i), relief=tk.GROOVE, font=self.choice_font, fg=light,bg=dark,overrelief=tk.RIDGE, bd=4, padx=20, highlightbackground='black', highlightcolor='black', highlightthickness=3)
		self.buttons.append(temp_button)

	def addButtons(self):
		for i in range(len(self.buttons)):
			self.buttons[i].grid(column=1,sticky=tk.N+tk.S+tk.E+tk.W, pady=3)

	def load(self):
		self.setup()
		self.header.grid(column=0, columnspan=3, sticky=tk.N+tk.E+tk.S+tk.W)
		self.addButtons()
		self.quitButton.grid(column=1, row=10, pady=10, sticky=tk.N+tk.S)
		self.grid()
		self.root.wm_deiconify()
		self.mainloop()

	def setup(self):
		# if rounds are default
		if self.control.contestantSetup == False or len(self.control.contestants_info) == 0:
			# set contestants_info array first
			i = 0
			for r in range(self.control.roundCount):
				current = self.control.rounds[r]
				self.control.contestants_info += [Contestant(j+1, self.control) for j in range(current.getCCount())]
				for ctr in range(current.getCCount()):
					self.control.contestants_info[i].setRound(current)
					i += 1
		if self.control.default_rounds == True:
			m = 0
			n = 6
			for i in range(3):
				self.control.navi_states.append(ContestantsListScreen(self.root, self.control, self.control.rounds[i], self.control.contestants_info[m:n]))
				m = n
				n = m + 6
			self.control.navi_states.append(ContestantsListScreen(self.root, self.control, self.control.rounds[3], self.control.contestants_info[18:24]))
			self.control.navi_states.append(ContestantsListScreen(self.root, self.control, self.control.rounds[4], self.control.contestants_info[24:28]))
		# if rounds are custom
		elif self.control.default_rounds == False:
			m = 0
			n = self.control.rounds[0].getCCount()
			for i in range(self.control.roundCount):
				self.control.navi_states.append(ContestantsListScreen(self.root, self.control, self.control.rounds[i], self.control.contestants_info[m:n]))
				m = n
				n = m + self.control.rounds[i].getCCount()
		self.control.navi_states.append(self)
		self.rounds = self.control.rounds
		if len(self.buttons) != self.control.roundCount:
			for i in range(self.control.roundCount):
				self.createButton(i)
			self.elements += self.buttons

	def unload(self):
		#for i in range(len(self.elements)):
		#	self.elements[i].grid_remove()
		self.quitButton.grid_remove()
		self.grid_remove()
		self.quit()

	def _quit(self):
		for i in range(len(self.elements)):
			self.elements[i].grid_remove()
		self.quitButton.grid_remove()
		self.grid_remove()
		self.control.log("Rounds list screen window closed1.")
		self.root.wm_withdraw()
		self.quit()

	def on_closing(self):
		if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?", parent=self.root):
			self.control.log("Rounds list screen window closed2.")
			self.root.wm_withdraw()
			self.quit()

class ContestantsListScreen(tk.Frame):
	def __init__(self, master, control, _round, contestants):
		## initialization ##
		tk.Frame.__init__(self, master, width=640, height=480, pady=20,bg=light)
		self.title = "Contestant Delegation"
		self.master.title(self.title)
		self.control = control
		self.round = _round

		## customization variables ##
		self.main_font = tkFont.Font(self, family='Code Bold', size=24)
		self.choice_font = tkFont.Font(self, family='Consolas', size=11)
		self.button_font = tkFont.Font(self, family='Consolas', size=9)

		## arrays ##
		self.buttons = []
		self.icons = []
		self.contestants = contestants

		# Prefinal Round 1 - c[0:6]
		# Prefinal Round 2 - [6:12]
		# Prefinal Round 3 - [12:18]
		# Wildcard Round - [18:24]
		# Finals - [24:27]

		## other elements ##
		self.header = tk.Label(self, text=self.round.getName(), font=self.main_font, fg=dark, bg=light, relief=tk.FLAT, justify=tk.CENTER, anchor=tk.CENTER, padx=20, pady=10, name='contestantsHeader')
		self.quitButton = tk.Button(self, text="< Back", font=self.button_font, command=self.unload, bg=dark,fg=light,relief=tk.GROOVE, overrelief=tk.RIDGE, bd=4, padx=20, highlightbackground='black', highlightcolor='black', highlightthickness=3)

	def onButtonClick(self, i):
		E = EditContestantProfileScreen(self.contestants[i], self.control)
		E.load()

	def createButton(self, i):
		temp_text = "Contestant " + str(i+1)
		temp_button = tk.Button(self, text=temp_text, state=tk.NORMAL, command=lambda:self.onButtonClick(i), font=self.choice_font, relief=tk.GROOVE, overrelief=tk.RIDGE, bd=4, padx=20, highlightbackground='black', highlightcolor='black', highlightthickness=3, name=str("contestant"+str(i+1)), bg=dark, fg=light)
		self.buttons.append(temp_button)

	def addButtons(self):
		for i in range(len(self.contestants)):
			self.createButton(i)
		for i in range(len(self.buttons)):
			self.buttons[i].grid(column=1,sticky=tk.N+tk.S, padx=25)

	def load(self):
		self.control.navi_states[-1].unload()
		self.header.grid(column=1, sticky=tk.N+tk.E+tk.S+tk.W)
		self.addButtons()
		self.grid()
		self.quitButton.grid(column=1, row=10, pady=10, sticky=tk.N+tk.S)
		self.mainloop()

	def unload(self):
		self.quitButton.grid_remove()
		self.grid_remove()
		self.quit()
		self.control.navi_states[-1].grid()
		self.control.navi_states[-1].quitButton.grid()



class EditContestantProfileScreen(tk.Frame):
	def __init__(self, contestant, control):
		self.root = tk.Tk()
		self.root.title("Edit Contestant " + str(contestant.getNum()))
		self.root.update_idletasks()
		x = (self.root.winfo_screenwidth()) - (self.root.winfo_screenwidth() / 2) - self.root.winfo_width() - 30
		y = self.root.winfo_screenheight() - (self.root.winfo_screenheight() / 2) - self.root.winfo_height() - 20
		self.root.geometry('+'+str(x)+'+'+str(y))
		self.root.wm_withdraw()
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		tk.Frame.__init__(self, self.root, bg=light)
		self.contestant = contestant
		self.control = control

		## customization variables ##
		self.main_font = tkFont.Font(self, family='Consolas', size=14)
		self.button_font = tkFont.Font(self, family='Consolas', size=50)
		self.check_font = tkFont.Font(self, family='Webdings', size=50)

		## essential variables ##
		self.elements = []
		self.frames = [tk.Frame(self,bg=light) for i in range(4)]
		self.field_names = 'Key', 'Sound', 'Score'
		self.fields_labels = [tk.Label(self.frames[2], font=self.main_font, text=self.field_names[i], anchor=tk.W, justify=tk.LEFT, bg=light) for i in range(3)]
		self.fields = [tk.Entry(self.frames[2]) for i in range(3)]
		self.contestantText = tk.Label(self.frames[0], text="Contestant Number", font=self.main_font, justify=tk.CENTER, relief=tk.FLAT, anchor=tk.CENTER, bg=light)

		self.smalltextField = tk.Entry(self.frames[0], width=3)

		self.setButton = tk.Button(self.frames[3], text='Set Info', command=self.set, bg=dark, fg=light)

		for frames in self.frames:
			self.elements.append(frames)
		for stuff in range(6):
			self.elements.append(self.fields_labels[i])
			self.elements.append(self.fields[i])
		self.elements.append(self.contestantText)
		self.elements.append(self.smalltextField)


	def set(self):
		self.contestant.setKey(self.fields[0].get())
		self.contestant.setSound(self.fields[1].get())
		self.contestant.setScore(int(self.fields[2].get()))

		# log set fields
		self.contestant.getAll()
		self.contestant.num_canvas.config(text=self.contestant.getScore())
		self.contestant.num_canvas.update()
		# close window
		self.root.wm_withdraw()
		self.quit()

	def load(self):
		self.frames[0].grid(row=0, column=0, sticky=tk.W)
		self.frames[1].grid(row=1, column=0, sticky=tk.W)
		self.frames[2].grid(row=1, column=0, sticky=tk.E)
		self.frames[3].grid(row=2, column=1, columnspan=3, sticky=tk.E+tk.W)

		self.contestantText.grid(row=0, column=0)

		self.smalltextField.grid(row=0, column=1, padx=5)
		self.smalltextField.insert(tk.END, self.contestant.getNum())

		for i in range(len(self.fields)):
			self.fields_labels[i].grid(row=i, column=0)
			self.fields[i].grid(row=i, column=1, pady=5, padx=5)

		# if fields are already set beforehand, display values
		self.fields[0].insert(tk.END, self.contestant.getKey())
		self.fields[1].insert(tk.END, self.contestant.getSound())
		self.fields[2].insert(tk.END, self.contestant.getScore())

		self.setButton.grid(column=3)
		self.grid()
		self.root.wm_deiconify()
		self.mainloop()

	def on_closing(self):
		self.control.log("Edit contestant profile screen window closed.")
		self.root.wm_withdraw()
		self.quit()