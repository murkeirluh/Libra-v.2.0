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

debug = True

def _debug(*args, **kwargs):
    if debug:
    	print("[DEBUG]", *args, file=sys.stderr, **kwargs)

#### EDIT ROUNDS SCREEN ####
class EditRoundsScreen(tk.Frame):
	def __init__(self, control):
		self.root = tk.Tk()
		self.root.wm_withdraw()
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.root.update_idletasks()
		x = (self.root.winfo_screenwidth()) - (self.root.winfo_screenwidth() / 2) - self.root.winfo_width() - 100
		y = self.root.winfo_screenheight() - (self.root.winfo_screenheight() / 2) - self.root.winfo_height() - 50
		self.root.geometry('+'+str(x)+'+'+str(y))
		tk.Frame.__init__(self, self.root, bd=4, width=800, bg=light)
		self.title = "Edit Rounds"
		self.root.title(self.title)
		self.control = control

		## customization variables ##
		self.main_font = tkFont.Font(self, family='Code Bold', size=28)
		self.button_font = tkFont.Font(self, family='Consolas', size=13)

		## arrays ##
		self.frames = []

		## frames ##
		for i in range(5):
			self.frames.append(tk.Frame(self))

		## top frame ##
		self.titleOfScreen = tk.Label(self.frames[0], text="Rounds and Question Settings", font=self.main_font, relief=tk.FLAT, justify=tk.LEFT, bg=light, fg=dark)

		## second frame ##
		self.view_settings = tk.Button(self.frames[1], text="View Current Settings", command=self.viewSettings, font=self.button_font, fg=light, bg=dark, width=25)

		## third frame ##
		self.set_defaultButton = tk.Button(self.frames[2], text="Set to Default", command=self.set_default, font=self.button_font, fg=light, bg=dark, width=25, state="normal" if (self.control.roundSetup == False) else "disabled")

		## fourth frame ##
		self.customButton = tk.Button(self.frames[3], text="Set Custom Rounds", command=self.custom, font=self.button_font, fg=light, bg=dark, width=25, state="normal" if (self.control.roundSetup == False) else "disabled")

		## fifth frame ##
		self.exit_button = tk.Button(self.frames[4], text="Back to Menu", command=self.unload, font=self.button_font, fg=light, bg=dark, width=25)

	def viewSettings(self):
		next_screen = ViewSettingsScreen(self.control)
		next_screen.load()

	def set_default(self):
		next_screen = SummaryScreen(self.control)
		next_screen.load()
		if (self.control.roundSetup == True):
			self.disable_buttons()
		self.control.default_rounds = True
		self.unload()

	def custom(self):
		next_screen = HowManyRoundsScreen(self.control)
		next_screen.load()
		if (self.control.roundSetup == True):
			self.disable_buttons()
		self.unload()

	def disable_buttons(self):
		self.set_defaultButton.config(state="disabled")
		self.customButton.config(state="disabled")

	# load
	def load(self):
		self.control.log("Edit Rounds")
		self.grid()
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.frames[0].grid(row=0)
		self.frames[1].grid(row=1)
		self.frames[2].grid(row=2)
		self.frames[3].grid(row=3)
		self.frames[4].grid(row=4)

		self.titleOfScreen.grid(row=0, column=0, sticky=tk.NW)
		self.view_settings.grid()
		self.set_defaultButton.grid()
		self.customButton.grid()
		self.exit_button.grid()
		self.root.wm_deiconify()
		self.mainloop()

	def unload(self):
		self.root.wm_withdraw()
		self.quit()

	def on_closing(self):
		if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?", parent=self.root):
			self.control.log("Edit rounds closed.")
			self.root.wm_withdraw()
			self.quit()
			_debug("here sa edit rounds")


class ViewSettingsScreen(tk.Frame):
	def __init__(self, control):
		self.root = tk.Tk()
		self.root.wm_withdraw()
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.root.update_idletasks()
		x = (self.root.winfo_screenwidth()) - (self.root.winfo_screenwidth() / 2) - self.root.winfo_width() - 50
		y = self.root.winfo_screenheight() - (self.root.winfo_screenheight() / 2) - self.root.winfo_height() - 50
		self.root.geometry('+'+str(x)+'+'+str(y))
		tk.Frame.__init__(self, self.root, bd=4, width=800)
		self.title = "Round Setting Confirmation"
		self.root.title(self.title)
		self.control = control

		self.text = ""
		self.generate_text()

		## customization variables ##
		self.main_font = tkFont.Font(self, family='Code Bold', size=28)
		self.label_font = tkFont.Font(self, family='Arial', size=13)
		self.log_font = tkFont.Font(self, family='Courier New', size=10)
		self.button_font = tkFont.Font(self, family='Consolas', size=13)

		## arrays ##
		self.top_frame = tk.Frame(self)
		self.text_frame = tk.Frame(self)
		self.scroll_frame = tk.Frame(self.text_frame)
		self.lower_frame = tk.Frame(self)

		self.titleOfScreen = tk.Label(self.top_frame, text="Please confirm:", font=self.main_font, relief=tk.FLAT)
		self.logbox = tk.Text(self.text_frame, wrap=tk.WORD, font=self.log_font, bg=light, fg=dark)
		self.scrollbar= tk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.logbox.yview)
		self.logbox.config(yscrollcommand=self.scrollbar.set)
		self.confirmButton = tk.Button(self.lower_frame, text='Confirm', command=self.unload, font=self.button_font, padx=10, bg=dark, fg=light)
		self.bind_all('<MouseWheel>', self.scroll)

	def scroll(self, event):
		self.logbox.yview_scroll(-1*(event.delta/120), "units")

        def generate_text(self):
                self.text += "Number of Rounds: "+str(self.control.roundCount)+"\n"
                self.text += "Allow buzzing before timer starts: "
                self.text +=  "Yes" if (self.control.preTimerBuzzing == True) else "No"
                self.text += "\n\n"
                for r in self.control.rounds:
                        self.text += r.name + "\n"
                        self.text += "Contestant Count: " + str(r.getCCount()) + "\n"
                        self.text += "Question  "
                        for q in range(len(r.question_pts)):
                          self.text += str(q+1)
                          if (q+1 >= 10):
                            self.text += " "
                          else:
                            self.text += "  "
                        self.text += "\n"
                        self.text += "Point/s   "
                        for pts in r.question_pts:
                          self.text += str(pts)
                          if (pts >= 10):
                            self.text += " "
                          else:
                            self.text += "  "
                        self.text += "\n"
                        self.text += "Timer (s) "
                        for time in r.timer_seconds:
                          self.text += str(time)
                          if (time >= 10):
                            self.text += " "
                          else:
                            self.text += "  "
                        self.text += "\n\n"

	# load
	def load(self):
		self.control.log("Summary")
		self.grid(rowspan=2)
		self.lower_frame.grid(row=3)
		top=self.winfo_toplevel()
		self.rowconfigure(2, weight=1)
		self.logbox.insert("1.0", self.text)
		self.logbox.configure(state=tk.DISABLED)
		self.logbox.grid(row=1, column=0, sticky=tk.E+tk.W, padx=10, pady=10)
		self.scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S, pady=10)
		self.confirmButton.grid(row=3)

		self.top_frame.grid(row=0, sticky=tk.N+tk.S+tk.E+tk.W)
		self.text_frame.grid(row=2, sticky=tk.N+tk.S)
		self.scroll_frame.grid(column=1, sticky=tk.N+tk.S)

		self.titleOfScreen.grid(row=0, column=0)

		self.root.wm_deiconify()
		self.mainloop()

	def unload(self):
                self.grid_remove()
                self.logbox.grid_forget()
		self.root.wm_withdraw()
		self.quit()

	def on_closing(self):
		self.control.log("Summary window closed.")
		self.root.wm_withdraw()
		self.quit()


class SummaryScreen(tk.Frame):
	def __init__(self, control):
		self.root = tk.Tk()
		self.root.wm_withdraw()
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.root.update_idletasks()
		x = (self.root.winfo_screenwidth()) - (self.root.winfo_screenwidth() / 2) - self.root.winfo_width() - 100
		y = self.root.winfo_screenheight() - (self.root.winfo_screenheight() / 2) - self.root.winfo_height() - 50
		self.root.geometry('+'+str(x)+'+'+str(y))
		tk.Frame.__init__(self, self.root, bd=4, width=800)
		self.title = "Rounds Summary"
		self.root.title(self.title)
		self.control = control

		self.text = ""
		self.generate_text()

		## customization variables ##
		self.main_font = tkFont.Font(self, family='Code Bold', size=28)
		self.label_font = tkFont.Font(self, family='Arial', size=13)
		self.log_font = tkFont.Font(self, family='Courier New', size=10)
		self.button_font = tkFont.Font(self, family='Consolas', size=13)

		## arrays ##
		self.top_frame = tk.Frame(self)
		self.text_frame = tk.Frame(self)
		self.scroll_frame = tk.Frame(self.text_frame)
		self.lower_frame = tk.Frame(self)

		self.titleOfScreen = tk.Label(self.top_frame, text="Please confirm:", font=self.main_font, relief=tk.FLAT)
		self.logbox = tk.Text(self.text_frame, wrap=tk.WORD, font=self.log_font, bg=light, fg=dark)
		self.scrollbar= tk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.logbox.yview)
		self.logbox.config(yscrollcommand=self.scrollbar.set)
		self.confirmButton = tk.Button(self.lower_frame, text='Confirm', command=self.confirm, font=self.button_font, padx=10, bg=dark, fg=light)
		self.bind_all('<MouseWheel>', self.scroll)
	
	def confirm(self):
		self.control.roundSetup = True
		self.unload()

	def scroll(self, event):
		self.logbox.yview_scroll(-1*(event.delta/120), "units")

	def generate_text(self):
		self.text += "Number of Rounds: "+str(self.control.roundCount)+"\n"
		self.text += "Allow buzzing before timer starts: "
		self.text +=  ("Yes" if (self.control.preTimerBuzzing == True) else "No")
		self.text += "\n\n"
		for r in self.control.rounds:
			self.text += r.name + "\n"
			self.text += "Contestant Count: " + str(r.getCCount()) + "\n"
			self.text += "Question  "
			for q in range(len(r.question_pts)):
				self.text += str(q+1)
				if (q+1 >= 10): self.text += " "
			  	else: self.text += "  "
			self.text += "\n"
			self.text += "Point/s   "
			for pts in r.question_pts:
			  	self.text += str(pts)
			  	if (pts >= 10): self.text += " "
			  	else: self.text += "  "
			self.text += "\n"
			self.text += "Timer (s) "
			for time in r.timer_seconds:
			  	self.text += str(time)
			  	if (time >= 10):
			  		self.text += " "
			  	else:
			  		self.text += "  "
			self.text += "\n\n"

	# load
	def load(self):
		self.control.log("Summary")
		self.grid(rowspan=2)
		self.lower_frame.grid(row=3)
		top=self.winfo_toplevel()
		self.rowconfigure(2, weight=1)
		self.logbox.insert("1.0", self.text)
		self.logbox.configure(state=tk.DISABLED)
		self.logbox.grid(row=1, column=0, sticky=tk.E+tk.W, padx=10, pady=10)
		self.scrollbar.grid(row=1, column=1, sticky=tk.N+tk.S, pady=10)
		self.confirmButton.grid(row=3)

		self.top_frame.grid(row=0, sticky=tk.N+tk.S+tk.E+tk.W)
		self.text_frame.grid(row=2, sticky=tk.N+tk.S)
		self.scroll_frame.grid(column=1, sticky=tk.N+tk.S)

		self.titleOfScreen.grid(row=0, column=0)

		self.root.wm_deiconify()
		self.mainloop()

	def unload(self):
		self.grid_remove()
		self.logbox.grid_forget()
		self.root.wm_withdraw()
		self.quit()

	def on_closing(self):
		self.control.log("Summary window closed.")
		self.root.wm_withdraw()
		self.quit()


class HowManyRoundsScreen(tk.Frame):
	def __init__(self, control):
		self.root = tk.Tk()
		self.root.wm_withdraw()
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.root.update_idletasks()
		x = (self.root.winfo_screenwidth()) - (self.root.winfo_screenwidth() / 2) - self.root.winfo_width() - 100
		y = self.root.winfo_screenheight() - (self.root.winfo_screenheight() / 2) - self.root.winfo_height() - 50
		self.root.geometry('+'+str(x)+'+'+str(y))
		tk.Frame.__init__(self, self.root, bd=4, width=800, bg=light)
		self.title = "Custom Rounds Setting - Round Count"
		self.root.title(self.title)
		self.control = control

		## customization variables ##
		self.main_font = tkFont.Font(self, family='Code Bold', size=15)
		self.label_font = tkFont.Font(self, family='Arial', size=13)
		self.button_font = tkFont.Font(self, family='Consolas', size=13)

		## arrays ##
		self.frames = []

		## frames ##
		for i in range(3):
			self.frames.append(tk.Frame(self))

		## top frame ##
		self.titleOfScreen = tk.Label(self.frames[0], text="Number of rounds: ", font=self.main_font, relief=tk.FLAT, justify=tk.LEFT, bg=light, fg=dark)
		self.roundLabel = tk.Entry(self.frames[0], width=19, font=self.label_font, validatecommand=self.checkText)
		self.roundLabel.register(self.checkText)
		self.roundLabel.insert(0, str(5))

		## second frame ##
		self.checkbox_input = tk.IntVar()
		self.checkbox = tk.Checkbutton(self.frames[1], text="Allow buzzing before timer starts", font=self.main_font, variable=self.checkbox_input, bg=light, fg=dark, highlightcolor=light, relief=tk.FLAT, command=self.checkshit)
		self.checkbox.select()
		self.checkbox_input.set(1)
		## third frame ##
		self.nextButton = tk.Button(self.frames[2], text='Next', command=self.validate_input, font=self.button_font, fg=light, bg=dark)
		self.control.contestantCount = 0
		self.control.contestants_info = []
		self.control.default_rounds = False

	def checkText(self):
		return self.roundLabel.get().isdigit()

        def validate_input(self):
                try:
                  temp = int(self.roundLabel.get())
                  if (temp < 0):
                      raise ValueError
                  self.transition()
                except ValueError:
                  tkMessageBox.showerror(title="Error!", message="Please enter a valid number.")
                  self.roundLabel.delete(0, tk.END)

	def transition(self):
		self.control.roundCount = int(self.roundLabel.get())
		self.control.rounds = [Round(i+1) for i in range(self.control.roundCount)]
		self.control.preTimerBuzzing = self.checkbox_input.get()
		for rScreen in range(self.control.roundCount):
			next_screen = RoundNumberandTypeScreen(self.control, rScreen)
			next_screen.load()
		next_screen = SummaryScreen(self.control)
		next_screen.load()
		self.unload()

	def checkshit(self):
		if (self.checkbox_input.get() == 0):
			self.checkbox_input.set(1)
		else:
			self.checkbox_input.set(0)
		
	# load
	def load(self):
		self.control.log("Number of Rounds")
		self.grid()
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.frames[0].grid(row=0)
		self.frames[1].grid(row=1)
		self.frames[2].grid(row=2)

		self.titleOfScreen.grid(row=0, column=1)
		self.roundLabel.grid(row=0, column=4)
		self.checkbox.grid()
		self.nextButton.grid()

		self.root.wm_deiconify()
		self.mainloop()

	def unload(self):
		self.root.wm_withdraw()
		self.quit()

	def on_closing(self):
		self.control.log("How many rounds screen window closed.")
		self.root.wm_withdraw()
		self.quit()

class RoundNumberandTypeScreen(tk.Frame):
	def __init__(self, control, round_number):
		self.root = tk.Tk()
		self.root.wm_withdraw()
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		tk.Frame.__init__(self, self.root, bd=4, width=800, bg=light)
		self.title = "Custom Rounds Setting - Round Details"
		self.root.title(self.title)
		self.control = control
                self.round_number = round_number

		## customization variables ##
		self.main_font = tkFont.Font(self, family='Code Bold', size=15)
		self.label_font = tkFont.Font(self, family='Arial', size=13)
		self.button_font = tkFont.Font(self, family='Consolas', size=13)

		## arrays ##
		self.frames = []

		## frames ##
		for i in range(5):
			self.frames.append(tk.Frame(self))

		## first frame ##
		self.title = tk.Label(self.frames[0], text="Round "+str(self.round_number+1)+" out of "+str(self.control.roundCount), font=self.main_font, fg=dark, bg=light)
		## second frame ##
		self.roundText = tk.Label(self.frames[1], text="Round name:", font=self.main_font, fg=light_txt, bg=light)
		self.roundEntry = tk.Entry(self.frames[1], width=20, font=self.label_font)

		## third frame ##
		self.questionText = tk.Label(self.frames[2], text="Number of questions:", font=self.main_font, fg=light_txt, bg=light)
		self.questionEntry = tk.Entry(self.frames[2], width=10, font=self.label_font)

		## fourth frame ##
		self.ccountText = tk.Label(self.frames[3], text="Number of contestants:", font=self.main_font, fg=light_txt, bg=light)
		self.ccountEntry = tk.Entry(self.frames[3], width=8, font=self.label_font)
		self.ccountEntry.insert(0, str(6))

		## fifth frame ##
		self.nextButton = tk.Button(self.frames[4], text='Next', command=self.validate_input, font=self.button_font, fg=light, bg=dark)

        def validate_input(self):
                try:
                  temp = int(self.questionEntry.get())
                  if (temp < 0):
                      raise ValueError
                  temp = int(self.ccountEntry.get())
                  if (temp < 0):
                      raise ValueError
                  self.transition()
                except ValueError:
                  tkMessageBox.showerror(title="Error!", message="Please enter a valid number.")

	def transition(self):
		self.control.rounds[self.round_number].setName(self.roundEntry.get())
		self.control.rounds[self.round_number].setNum(self.round_number+1)
		self.control.rounds[self.round_number].setQCount(int(self.questionEntry.get()))
		self.control.rounds[self.round_number].setCCount(int(self.ccountEntry.get()))
		self.control.contestantCount += int(self.ccountEntry.get())
		next_screen = PointsAndTimerSettingScreen(self.control, self.round_number)
		next_screen.load()
		self.unload()

	# load
	def load(self):
		self.control.log("Define Round")
		self.grid()
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.frames[0].grid(row=0)
		self.frames[1].grid(row=1)
		self.frames[2].grid(row=2)
		self.frames[3].grid(row=3)
		self.frames[4].grid(row=4)

		self.title.grid()
		self.roundText.grid(row=0, column=0)
		self.roundEntry.grid(row=0, column=1)
		self.questionText.grid(row=0, column=0)
		self.questionEntry.grid(row=0, column=1)
		self.ccountText.grid(row=0, column=0)
		self.ccountEntry.grid(row=0, column=1)
		self.nextButton.grid()
		self.root.wm_deiconify()
		self.mainloop()

	def unload(self):
		self.root.wm_withdraw()
		self.quit()

	def on_closing(self):
		self.control.log("Round number and type screen closed.")
		self.root.wm_withdraw()
		self.quit()


class PointsAndTimerSettingScreen(tk.Frame):
	def __init__(self, control, round_number):
		self.root = tk.Tk()
		self.root.wm_withdraw()
		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.root.update_idletasks()
		x = (self.root.winfo_screenwidth()) - (self.root.winfo_screenwidth() / 2) - self.root.winfo_width() - 100
		y = self.root.winfo_screenheight() - (self.root.winfo_screenheight() / 2) - self.root.winfo_height() - 50
		self.root.geometry('+'+str(x)+'+'+str(y))
		tk.Frame.__init__(self, self.root, bd=4, width=800, bg=light)
		self.title = "Custom Round Setting - Points and Time"
		self.root.title(self.title)
		self.control = control
		self.round_number = round_number
		self.roundAddress = self.control.rounds[round_number]

		## customization variables ##
		self.main_font = tkFont.Font(self, family='Code Bold', size=15)
		self.label_font = tkFont.Font(self, family='Arial', size=13)
		self.button_font = tkFont.Font(self, family='Consolas', size=13)

		## arrays ##
		self.frames = []
		self.labels = []
		self.q_entry = []
		self.t_entry = []

		## frames ##
		for i in range(4):
			self.frames.append(tk.Frame(self))

		## top frame ##
		self.titleOfScreen = tk.Label(self.frames[0], text=self.roundAddress.getName(), font=self.main_font, fg=dark, bg=light)

		## second frame ##
		self.blankLabel = tk.Label(self.frames[1], text="", font=self.label_font, fg=dark, bg=light, width=13)
		self.pointLabel = tk.Label(self.frames[1], text="Points", font=self.label_font, fg=light_txt, bg=light, width=10)
		self.timerLabel = tk.Label(self.frames[1], text="Timer (seconds)", font=self.label_font, fg=light_txt, bg=light, width=13)

		## third frame ##
		self.nextButton = tk.Button(self.frames[3], text='Next', command=self.validate_input, font=self.button_font, fg=light, bg=dark)

        def validate_input(self):
                try:
                  for x in range(self.roundAddress.getQCount()):
                    temp = int(self.q_entry[x].get())
                    if (temp < 0):
                        raise ValueError
                    temp = int(self.t_entry[x].get())
                    if (temp < 0):
                        raise ValueError
                  self.transition()
                except ValueError:
                  tkMessageBox.showerror(title="Error!", message="Please enter a valid number.")

	def transition(self):
		self.save()
		self.unload()

	def save(self):
		for x in range(self.roundAddress.getQCount()):
			self.roundAddress.setPoints(x, int(self.q_entry[x].get()))
			self.roundAddress.setTimeDuration(x, int(self.t_entry[x].get()))

	# load
	def load(self):
		self.control.log("Set Points and Timer")
		self.grid()
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)

		self.frames[0].grid(row=0)
		self.frames[1].grid(row=1)
		self.frames[2].grid(row=2)
		self.frames[3].grid(row=3)

		self.titleOfScreen.grid()
		self.blankLabel.grid(row=0, column=1)
		self.pointLabel.grid(row=0, column=4)
		self.timerLabel.grid(row=0, column=8)
		for i in range(self.roundAddress.getQCount()):
			self.labels.append(tk.Label(self.frames[2], text="Question #"+str(i+1), font=self.label_font, fg=light_txt, bg=light, width=13))
			self.q_entry.append(tk.Entry(self.frames[2], font=self.label_font, width=10))
			self.t_entry.append(tk.Entry(self.frames[2], font=self.label_font, width=13))
			self.labels[i].grid(row=i, column=1)
			self.q_entry[i].grid(row=i, column=4)
			self.t_entry[i].grid(row=i, column=8)
		self.nextButton.grid()

		self.root.wm_deiconify()
		self.mainloop()

	def unload(self):
		self.root.wm_withdraw()
		self.quit()

	def on_closing(self):
		self.control.log("Points and shit screen window closed.")
		self.root.wm_withdraw()
		self.quit()
