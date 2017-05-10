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


#### ACTIVITY LOG SCREEN ####

class ActivityLogScreen(tk.Frame):
	def __init__(self, control):
		self.root = tk.Tk()
		self.root.title("Activity Log")
		self.root.wm_withdraw()

		tk.Frame.__init__(self, self.root)
		self.control = control

		self.log_font = tkFont.Font(self, family='Courier New', size=10)
		self.button_font = tkFont.Font(self, family='Consolas', size=10)

		self.top_frame = tk.Frame(self)
		self.text_frame = tk.Frame(self)
		self.scroll_frame = tk.Frame(self.text_frame)
		self.lower_frame = tk.Frame(self)

		self.logbox = tk.Text(self.text_frame, bg=light, wrap=tk.WORD, font=self.log_font)
		self.scrollbar= tk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.logbox.yview)
		self.logbox.config(yscrollcommand=self.scrollbar.set)
		self.exitButton = tk.Button(self.lower_frame, text='Exit', command=self.unload, font=self.button_font, padx=10)
		self.bind_all('<MouseWheel>', self.scroll)

	def scroll(self, event):
		self.logbox.yview_scroll(-1*(event.delta/120), "units")

	def load(self):
		try:
			text = self.control.logfile.read()
		except:
			a = "activitylog"
			b = ".txt"
			timestr = time.strftime("%Y%m%d")
			a = a + timestr + b
			self.control.logfile = open(a, "r")
		finally:
			text = self.control.logfile.read()
		self.grid(rowspan=2)
		self.top_frame.grid(row=0, sticky=tk.N+tk.S+tk.E+tk.W)
		self.text_frame.grid(row=2, sticky=tk.N+tk.S)
		self.scroll_frame.grid(column=1, sticky=tk.N+tk.S)
		self.lower_frame.grid(row=3)
		top=self.winfo_toplevel()
		self.rowconfigure(2, weight=1)
		self.logbox.insert("1.0", text)
		self.logbox.configure(state=tk.DISABLED)
		self.logbox.grid(row=1, column=0, sticky=tk.E+tk.W, padx=10, pady=10)
		self.scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S, pady=10)
		self.exitButton.grid(row=3)
		self.root.wm_deiconify()
		self.mainloop()

	def unload(self):
		self.grid_remove()
		self.logbox.grid_forget()
		self.root.wm_withdraw()
		self.quit()
