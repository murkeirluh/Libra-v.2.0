from __future__ import print_function
from collections import deque
from PIL import Image, ImageOps, ImageDraw, ImageTk
import sys
import Tkinter as tk
import tkFont, tkMessageBox

from Tkinter import Text
from colors import *
debug = True

# debug function
def _debug(*args, **kwargs):
    if debug:
    	print("[DEBUG]", *args, file=sys.stderr, **kwargs)

class __StartupScreen__(tk.Frame):
	def __init__(self, control, master=None):

		_debug("StartupScreen in states.")
		self.control = control

		tk.Frame.__init__(self, master, bg=dark, bd=4)
		self.title = "Libra v.2.0"
		self.master.title(self.title)

		## fonts #
		self.main_font = tkFont.Font(self, family='Calibri', size=30, weight='bold')
		self.button_font = tkFont.Font(self, family='Calibri', size=13)

		## frames ##
		self.frame1 = tk.Frame(self, bg=dark)
		self.frame2 = tk.Frame(self, bg=dark)

		## logo ##
		self.path = "assets/images/upmc logo.png"
		self.img = Image.open(self.path)
		self.resImg = self.img.resize((300,300), Image.ANTIALIAS)
		self.upmc = ImageTk.PhotoImage(self.resImg)
		self.logo = tk.Label(self.frame1, image=self.upmc, bg=dark)

		## buttons ##
                print(self.control.roundSetup)
		self.startButton = tk.Button(self.frame2, text='START\nGAME', font=self.main_font, command=self.__startGame, bg=light , fg = green, bd=1, padx=25, state="disabled" if (self.control.roundSetup == False) else "normal")
                self.editRounds = tk.Button(self.frame2, text='Edit Rounds', command=self.edit_rounds, font=self.button_font, bg=light, fg=light_txt)
		self.editContestants = tk.Button(self.frame2, text='Edit Contestants', command=lambda:self.control.loadNavi(1), font=self.button_font, bg=light, fg=light_txt)
		self.testBuzzers = tk.Button(self.frame2, text='Test Buzzers', command=lambda:self.control.loadNavi(2), font=self.button_font, bg=light, fg=light_txt)
		self.activityLog = tk.Button(self.frame2, text='Activity Log', command=lambda:self.control.loadNavi(3), font=self.button_font, bg=light, fg=light_txt)

		## array ##
		self.frameschildren = []

        def edit_rounds(self):
                self.control.loadNavi(0)
                if (self.control.roundSetup == True):
                        self.startButton.config(state="normal")

	def load(self):
		_debug("Startup screen loaded.")
		self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
		top = self.winfo_toplevel()
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0,weight=1)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

		self.frame1.grid(row=0, column=0, sticky=tk.N+tk.S)
		self.frame2.grid(row=0, column=1, sticky=tk.N+tk.S)
		
		self.logo.grid(row=0, rowspan=6, column=0, columnspan=5, padx=3)
		self.frameschildren.append(self.logo)
		self.startButton.grid(row=0, column=1, pady=30, padx=15, sticky=tk.E+tk.W)
		self.frameschildren.append(self.startButton)
		
                self.editRounds.grid(row=1, column=1, pady=2, padx=5, sticky=tk.E+tk.W)
		self.editContestants.grid(row=2, column=1, pady=2, padx=5, sticky=tk.E+tk.W)
		self.testBuzzers.grid(row=3, column=1, pady=2, padx=5, sticky=tk.E+tk.W)
		self.activityLog.grid(row=4, column=1, pady=2, padx=5, sticky=tk.E+tk.W)

                self.frameschildren.append(self.editRounds)
		self.frameschildren.append(self.editContestants)
		self.frameschildren.append(self.testBuzzers)
		self.frameschildren.append(self.activityLog)
		#self.quitButton = tk.Button(self, text='Exit', font=self.button_font, command=self.quit)
		#self.quitButton.grid(row=5, column=5)

	def __startGame(self):
		self.quit()
		self.destroy()
		self.control.states.remove(self)
