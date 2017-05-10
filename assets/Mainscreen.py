from __future__ import print_function
from PIL import Image, ImageOps, ImageDraw, ImageTk
import sys, time
import Tkinter as tk
import tkFont, tkFileDialog

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

class __MainScreen__(tk.Frame):
	def __init__(self, control, __round, master=None):
		_debug("MainScreen in states.")
		tk.Frame.__init__(self, master, bd=4, width=800, bg=light)
		self.round = __round
		self.title = "Libra v.2.0"
		self.master.title(self.title)
		self.master.update_idletasks()
		x = (self.master.winfo_screenwidth()) - (self.master.winfo_screenwidth() / 2) - self.master.winfo_width() + 50
		y = 35
		self.master.geometry('+'+str(x)+'+'+str(y))
		self.control = control

		## customization variables ##
		self.main_font = tkFont.Font(self, family='Code Bold', size=28)
		self.score_font = tkFont.Font(self, family='Code Bold', size=13)
		self.arrow_font = tkFont.Font(self, family='Consolas', size=25)
		self.second_font = tkFont.Font(self, family='Franklin Gothic Medium', size=20)
		self.button_font = tkFont.Font(self, family='Consolas', size=13)
		self.timer_font = tkFont.Font(self, family='Code Bold', size=50)

		## arrays ##
		self.frames = []
		self.contestants = []
		self.history = []

		## frames ##
		for i in range(6):
			self.frames.append(tk.Frame(self, bg=light))

		self.frames[0].config(width=2)
		self.roundNumber = self.round.getNum()
		self.questionNumber = 1
		self.time = self.round.timer_seconds[0]
		self.queue = Queue(self.control.contestantCount)
		# timer variable
		self.timer = Timer(self.frames[1], self.time, self.queue)
		# recent scorer
		self.recent_scorer = ""
		# undo/redo counter
		self.history_ptr = -1

		## top frame ##
		_debug(self.round.getName())
		self.roundText = self.round.getName()
		self.roundName = tk.Label(self.frames[0], text=self.roundText, font=self.main_font, relief=tk.FLAT, justify=tk.LEFT, bg=light, fg='#002B36')
		self.arrow = tk.Label(self.frames[0], text='next', font=self.arrow_font, bg=light, fg=light_txt, padx=2)
		self.questionNumber_text = 'Question '
		self.questionNumber_label = tk.Label(self.frames[0], text="Question " + str(self.questionNumber) + "/" + str(self.round.questionCount), font=self.second_font, justify=tk.LEFT, bg=light, fg=light_txt)

		## second frame ##
		# top row
		## contestant variables ##
		self.contestantCount = self.round.getCCount()

		for i in range(self.contestantCount):
			self.contestants.append(Contestant(i+1, self.control, self.frames[2]))

		# append contestants to main contestants array
		self.control.contestants += self.contestants
		self.copy_info()

		for i in range(self.contestantCount):
			c = self.contestants[i].getKey()
			if c == "":
				self.contestants[i].setKey(chr(i+65))
				self.bind_all(chr(i+65), self._buzz)
				#self.contestants[i].setKey(chr(i))
				#self.bind_all(chr(i), self._buzz)
			else:
				self.bind_all(c, self._buzz)
				self.bind_all(c.upper(), self._buzz)

		# bottom frame
		self.menuButton = tk.Button(self.frames[4], text='Menu', font=self.button_font, command=self.PauseGame, anchor=tk.E, justify=tk.LEFT, bg=dark, fg=dark_txt, highlightbackground='#93A1A1', highlightcolor='#002B36')
		self.undo_button = CustomButton(self.frames[4], 40, 40, "undo", light, dark_txt, self.undo)
		self.redo_button = CustomButton(self.frames[4], 40, 40, "redo", light, dark_txt, self.redo)
		self.back_button = CustomButton(self.frames[5], 50, 50, "back", light, dark_txt, self.decrement)
		self.next_button = CustomButton(self.frames[5], 50, 50, "NEXT", light, dark_txt, self.increment)

		# key bindings
		self.bind_all('<KeyPress-Return>', self.correct)
		self.bind_all('<KeyPress-Escape>', self.wrong)
		self.timer.stop_button.bind('<Double-Button-1>', self.reset)
		self.bind_all('<KeyPress-Shift_L>', self.timer.startTimer)
		self.bind_all('<Double-KeyPress-Shift_L>', self.reset)
		self.bind_all('<KeyPress-Shift_R>', self.timer.stop)

		self.winner = 0
		self.control.log("Question #", self.questionNumber, "("+str(self.round.question_pts[self.questionNumber-1]), "points for", self.time, "seconds)")

	# buzz function
	# currently bound to a, b, c, d, e
	def _buzz(self, event):
		allowBuzz = False
		_debug("Key pressed: " + str(event.keysym))
		# if (len(self.queue) == self.queue.maxlen):
		# 	_debug("Queue full")

		# if pre-timer buzzing is enabled and timer hasn't started yet
		if (self.control.preTimerBuzzing == True and (self.timer.ticked == False or self.timer.ticked == True)):
			allowBuzz = True

		# if pre-timer buzzing is disabled and timer has started
		elif (self.control.preTimerBuzzing == False and self.timer.ticked == True):
			allowBuzz = True

		# if conditions permit buzzing
		if allowBuzz == True:
			i = self.searchKey(event.char)
			# searchKey() may return -1, thus self.contestants[-1] may be appended to the queue
			if i >= 0:
				if self.contestants[i].canBuzz and self.contestants[i] not in self.queue:
					#_debug("Buzzed!")
					# if timer has started, pause timer
					if self.timer.ticked == True:
						self.timer.stop(event)
					# if queue is full
					if (len(self.queue) == self.queue.maxlen):
						_debug("Queue full")
					# if not, increment buzzcount
					else:
						self.queue.buzzCount += 1
						self.queue.append(self.contestants[i])

					# if queue has contents
					if (len(self.queue)):
						# call contestant's buzz function
						self.queue[0].buzz()
						self.queue._print()
				else:
					_debug("This contestant cannot buzz!")

			# if queue has contents
			if (len(self.queue)):
				# call contestant's buzz function
				self.queue[0].buzz()

		else:
			_debug("Buzzing is disabled!")

	# if contestant on top of queue answers correctly
	def correct(self, event):
		if (len(self.queue)):
			_debug("Contestant number " + str(self.queue[0].getNum()) + " got it correct!")
			self.control.log("Contestant number " + str(self.queue[0].getNum()) + " got it correct!")
			self.queue[0]._plus(self.round.question_pts[self.questionNumber-1])
			_debug("Contestant " + str(self.queue[0].getNum()) + " score: " + str(self.queue[0].getScore()))
			self.control.log("Contestant " + str(self.queue[0].getNum()) + " score: " + str(self.queue[0].getScore()))
			# self.queue[0].num_canvas.config(text=self.queue[0].getScore())
			# self.queue[0].num_canvas.update()
			self.queue[0].correct()
			self.update_info()
			self.recent_scorer = self.queue[0]
			# if history pointer is not pointing at the recent item
			if (len(self.history) and self.history_ptr >= 0 and self.history_ptr+1 < len(self.history)):
				self.history[self.history_ptr+1] = (self.recent_scorer, self.round.question_pts[self.questionNumber-1])
				self.history_ptr += 1
				self.history = self.history[:self.history_ptr+1]
				self.history_ptr = len(self.history)-1
			# if history pointer still matches
			elif (self.history_ptr == len(self.history)-1):
				self.history.append((self.recent_scorer, self.round.question_pts[self.questionNumber-1]))
				self.history_ptr += 1
			elif (self.history_ptr == -1 and len(self.history) == 0):
				self.history.append((self.recent_scorer, self.round.question_pts[self.questionNumber-1]))
				self.history_ptr += 1
			elif (self.history_ptr == -1 and len(self.history)):
				self.history[self.history_ptr+1] = (self.recent_scorer, self.round.question_pts[self.questionNumber-1])
				self.history_ptr += 1
				self.history = self.history[:self.history_ptr+1]
				self.history_ptr = len(self.history)-1
			self.queue.clear()
			self.queue.buzzCount = 0
			self.reset(event)

	def wrong(self, event):
		if (len(self.queue)):
			self.queue[0].wrong()
			self.queue[0].unbuzz(event)
			self.queue.popleft()
		if (len(self.queue)):
			self._buzz(event)
		else:
			# if queue is empty and time is up
			if self.timer.ticked and self.timer.timer == 0:
				_debug("Nobody got the correct answer!")
				self.control.log("Nobody got the correct answer!")
				self.reset(event)
				for contestants in self.contestants:
					contestants.canBuzz = True
				self.queue.buzzCount = 0
			# if queue is empty but timer is still running
			elif self.timer.ticked and self.timer.timer > 0:
				_debug("Buzzcount: " + str(self.queue.buzzCount))
				if self.queue.buzzCount != self.contestantCount:
					self.timer.id = self.timer.label.after(1000, lambda:self.timer.startTimer(event))
				else:
					_debug("Nobody got the correct answer!")
					self.control.log("Nobody got the correct answer!")
					self.reset(event)
					#_debug("Queue is cleared!")
					for contestants in self.contestants:
						contestants.canBuzz = True
					self.queue.buzzCount = 0
		self.queue._print()

	# returns contestant number whose key was pressed
	# if output < 0, key unassigned to contestant
	def searchKey(self, key):
		for i in range(len(self.contestants)):
			if key.upper() == self.contestants[i].getKey().upper():
				return i
		return -1

	# reset contestants and timer
	def reset(self, event=None):
		self.timer.reset()
		self.setTimer()
		for i in range(self.contestantCount):
			self.contestants[i].canBuzz = True
			self.contestants[i].buzzed = False
			self.contestants[i].set_tphoto()

	def setTimer(self):
		self.timer.setTimer(self.time)

	# next question
	def increment(self):
		self.reset()
		if self.questionNumber < self.round.questionCount:
			self.questionNumber += 1
			self.time = self.round.timer_seconds[self.questionNumber-1]
			self.setTimer()
			self.questionNumber_label.config(text="Question " + str(self.questionNumber) + "/" + str(self.round.questionCount), fg=green)
			self.questionNumber_label.update()
			time.sleep(0.15)
			self.questionNumber_label.config(fg=light_txt)
			self.questionNumber_label.update()
			_debug("Next question")
			self.control.log("Question #", self.questionNumber, "("+str(self.round.question_pts[self.questionNumber-1]), "points for", self.time, "seconds)")
		elif self.questionNumber >= self.round.questionCount:
			if self.checkTies() == True:
				_debug("Ties found.")
				self.questionNumber_label.config(text="Question " + str(self.questionNumber) + "/" + str(self.round.questionCount), fg=green)
				self.questionNumber_label.update()
				time.sleep(0.15)
				self.questionNumber_label.config(fg=light_txt)
				self.questionNumber_label.update()
			else:
				_debug("STOP INCREMENT")
				self.questionNumber = 1
				self.quit()
				self.destroy()
				self.control.states.remove(self)

	def decrement(self):
		self.reset()
		if self.questionNumber > 1 and self.questionNumber < self.round.questionCount:
			self.questionNumber -= 1
			self.time = self.round.timer_seconds[self.questionNumber-1]
			self.setTimer()
			_debug("Previous question")
		else:
			_debug("STOP DECREMENT")
			self.questionNumber = 1
		self.questionNumber_label.config(text="Question " + str(self.questionNumber) + "/" + str(self.round.questionCount), fg=green)
		self.questionNumber_label.update()
		time.sleep(0.15)
		self.questionNumber_label.config(fg=light_txt)
		self.questionNumber_label.update()
		self.control.log("Question #", self.questionNumber, "("+str(self.round.question_pts[self.questionNumber-1]), "points for", self.time, "seconds)")
		

	def checkTies(self):
		if self.control.default_rounds:
			curr = 0
			second = 0
			third = 0
			scores = []
			temp = self.contestants
			for c in temp:
				if c.getScore() > curr:
					third = second
					second = curr
					curr = c.getScore()
				elif c.getScore() > second:
					third = second
					second = c.getScore()
				elif c.getScore() > third:
					third = c.getScore()
				scores.append(c.getScore())
			scores.sort()
			_debug(scores)
			_debug(curr, second, third)

			_debug(scores.count(curr))
			_debug(scores.count(second))
			_debug(scores.count(third))
			if curr != 0:
				if (scores.count(curr) > 1):
					return True
				elif (scores.count(second) > 1):
					return True if (second != 0) else False
				elif (scores.count(third) > 1):
					return True if (third != 0) else False
				else:
					return False
			else:
				return False
		else:
			return False

	def getplacers(self):
		if self.control.default_rounds:
			for i in range(3):
				curr = 0
				for c in self.contestants:
					if c.getScore() > curr:
						self.winner = c
						curr = c.getScore()

				if self.winner != 0:
					_debug(self.winner.getScore())
					self.contestants.remove(self.winner)
					if i == 0:
						self.winner.setRound(self.control.rounds[4])
						self.control.winners.append(self.winner)
					else:
						self.winner.setRound(self.control.rounds[3])
						self.control.clinchers.append(self.winner)
			if self.winner == 0:
				return 0
		else:
			return 0

	# copy info from contestants_info array
	def copy_info(self):
		m = 0
		for m in range(len(self.control.contestants_info)):
			if (self.control.contestants_info[m].getRound() == self.round): break
		for i in range(self.contestantCount):
			self.contestants[i].setScore(self.control.contestants_info[m+i].getScore())
			self.contestants[i].setKey(self.control.contestants_info[m+i].getKey())
			self.bind_all(self.control.contestants_info[m+i].getKey().lower(), self._buzz)
			self.bind_all(self.control.contestants_info[m+i].getKey().upper(), self._buzz)
			self.contestants[i].setSound(self.control.contestants_info[m+i].getSound())
			self.contestants[i].num_canvas.config(text=self.contestants[i].getScore())
			self.contestants[i].num_canvas.update()

	# update contestants_info with contestants' infos
	def update_info(self):
		m = 0
		for m in range(len(self.control.contestants_info)):
			if (self.control.contestants_info[m].getRound() == self.round): break
		for i in range(self.contestantCount):
			self.control.contestants_info[m+i].setScore(self.contestants[i].getScore())
			self.control.contestants_info[m+i].setKey(self.contestants[i].getKey())
			self.control.contestants_info[m+i].setSound(self.contestants[i].getSound())

	def undo(self):
		if (self.history_ptr >= 0 and self.history_ptr < len(self.history)):
			recent_action = self.history[self.history_ptr]
			recent_action[0]._minus(recent_action[1])
			self.history_ptr -= 1
			self.update_info()
			_debug("Undo")
		else:
			_debug("Nothing to undo")

	def redo(self):
		if (self.history_ptr+1 < len(self.history)):
			recent_action = self.history[self.history_ptr+1]
			recent_action[0]._plus(recent_action[1])
			self.update_info()
			_debug("Redo")
			self.history_ptr += 1
		else:
			_debug("Nothing to redo")
		_debug("Ctr:", self.history_ptr, "Length:", len(self.history))

	# load
	def load(self):
		_debug("MainGame screen loaded.")
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		## gridding frames ##
		# top frame 1/2
		self.frames[0].grid_propagate()
		self.frames[0].grid(row=0, column=0, sticky=tk.W+tk.E)
		# top frame 2/2
		self.frames[1].grid(row=0, column=1, columnspan=4, sticky=tk.NE, padx=10)
		# middle frame
		self.frames[2].grid(row=1, column=0, rowspan=6, columnspan=2, padx=40, pady=20, sticky=tk.W+tk.E)
		# divider frame
		self.frames[3].grid(row=7, pady=4, sticky=tk.W+tk.E)
		# bottom frame 1/2
		self.frames[4].grid(row=8, column=0, rowspan=3, pady=7, sticky=tk.SW)
		# bottom frame 2/2
		self.frames[5].grid(row=8, column=1, rowspan=3, pady=7, sticky=tk.SE)

		for i in range(6):
			self.frames[i].rowconfigure(i, weight=1)
			self.frames[i].columnconfigure(i, weight=1)

		self.roundName.grid(row=0, column=0, sticky=tk.NW, padx=3)
		self.questionNumber_label.grid(row=1, column=0, sticky=tk.SW, padx=3)

		self.timer.start_button.grid(row=0, column=1, padx=2, pady=5, sticky=tk.E)
		self.timer.stop_button.grid(row=0, column=2,  padx=4, pady=5, sticky=tk.E)
		self.timer.label.grid(row=0, column=8, rowspan=2, columnspan=5, padx=15, sticky=tk.E)

		## top row ##
		divider = 3
		_range = self.contestantCount/divider
		if self.contestantCount == 6:
			divider = 3
			_range = self.contestantCount/divider+1
		elif self.contestantCount == 4:
			divider = 2
			_range = self.contestantCount/divider
		for i in range(_range):
			# row 0
			self.contestants[i].num_canvas.config(font=self.score_font)
			self.contestants[i].num_canvas.grid(row=0, column=i, pady=2)
			# row 1
			self.contestants[i].button.grid(row=1, column=i, padx=10)
		for i in range(_range, self.contestantCount):
			self.contestants[i].num_canvas.config(font=self.score_font)
			# row 2
			self.contestants[i].num_canvas.grid(row=3, column=i%divider, pady=3)
			# row 3
			self.contestants[i].button.grid(row=4, column=i%divider, padx=10, pady=2)

		## bottom frame ##
		self.menuButton.grid(row=0, column=0, sticky=tk.W, padx=2)
		self.undo_button.grid(row=0, column=1, sticky=tk.E, padx=2)
		self.redo_button.grid(row=0, column=2, sticky=tk.E, padx=1)
		self.back_button.grid(row=0, column=0, sticky=tk.W)
		self.next_button.grid(row=0, column=1, sticky=tk.E)

		self.grid()

	def Quit(self):
		_debug("Quit.")
		self.quit()

	def PauseGame(self):
		GamePauseScreen(self.control, self)
		self.copy_info()

class GamePauseScreen(tk.Frame):
	def __init__(self, control, Mainscreen, master=None):
		self.root = tk.Tk()
		self.root.title("Game Paused")
		self.root.wm_withdraw()
		tk.Frame.__init__(self, self.root, bg=dark)
		self.control = control
		self.mainscreen = Mainscreen

		self.main_font = tkFont.Font(self, family='Calibri', size=20)
		self.button_font = tkFont.Font(self, family='Calibri', size=13)
		self.custom_font = tkFont.Font(self, family='Calibri', size=13)

		self.resumeButton = tk.Button(self, text='Resume Game', command=self.unload,font=self.button_font,bg=light, fg=light_txt)
		self.editContestants = tk.Button(self, text='Edit Contestants', command=lambda:self.control.loadNavi(1), font=self.button_font, bg=light, fg=light_txt)
		self.testBuzzers = tk.Button(self, text='Test Buzzers',font=self.button_font, command=lambda:self.control.loadNavi(2), bg=light, fg=light_txt)
		self.activityLog = tk.Button(self, text='Activity Log', font=self.button_font, command=lambda:self.control.loadNavi(3), bg=light, fg=light_txt)

		self.load()

	def load(self):
		_debug("Game Pause screen loaded.")
		top = self.winfo_toplevel()
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0,weight=1)
		self.rowconfigure(0, weight=1)
		self.columnconfigure(0, weight=1)

		self.resumeButton.grid(row=0, column=0, pady=15, padx=20)
		self.editContestants.grid(row=1, column=0, pady=15, padx=20)
		self.testBuzzers.grid(row=2, column=0, pady=15, padx=20)
		self.activityLog.grid(row=3, column=0, pady=15, padx=20)

		self.root.wm_deiconify()
		self.grid()
		self.mainloop()
		self.mainscreen.copy_info()

	def unload(self):
		self.root.wm_withdraw()
		self.quit()
