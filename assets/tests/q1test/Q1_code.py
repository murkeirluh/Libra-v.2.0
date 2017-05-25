from __future__ import print_function
from collections import deque
import sys
import Tkinter as tk

class Controller:
	def __init__(self):
		# array of states/screens
		self.states = []
		# array of navigation screens
		self.navigation = []
		# states of navigation screens
		self.navi_states = []
		# variable for number of rounds
		self.roundCount = 5
		# variable for number of contestants
		self.contestantCount = 18
		# status of round setup
		self.roundSetup = False
		# status of contestants setup
		self.contestantSetup = False

		self.preTimerBuzzing = True
		# main contestants array
		self.contestants = []
		# contestants array for modifiying info
		self.contestants_info = []
		# rounds array
		self.rounds = []
		# winners array
		self.winners = []
		#clinchers array
		self.clinchers = []
		# window title
		self.title = "Libra v.2.0"
		# toggle for activity log (default: True)
		self.logtofile = True
		# activity log file
		self.logfile = ""
		# start log if logging is true
		self.counter = 0

	def loadNavi(self, i):
		self.navigation[i].load()

	def get_count(self):
		return self.counter

class Queue(deque):
    def __init__(self, maxlen):
        # for ordinary game queue
        if maxlen > 0: 
                deque.__init__(self, maxlen=maxlen)
        self.preTimerBuzzing = False
        self.buzzCount = 0

class Round:
	def __init__(self, num):
		self.number = num
		self.name = 'Prefinal Round ' + str(self.number)
		# number of questions
		self.questionCount = 15
		# number of points per question
		self.question_pts = [0 for i in range(self.questionCount)]
		self.timer_seconds = [15 for i in range(self.questionCount)]
		# number of contestants for the round
		self.contestantCount = 6

	# set the round name
	def setName(self, name):
		self.name = name

	# set the number of questions for round
	def setQCount(self, count):
		self.questionCount = count
		self.question_pts = [0 for i in range(self.questionCount)]
		self.timer_seconds = [15 for i in range(self.questionCount)]

	# set number of contestants
	def setCCount(self, num):
		self.contestantCount = num

	# set a number of points for question number q_num
	def setPoints(self, q_num, pts):
		self.question_pts[q_num] = pts
		self.setDuration(q_num)

        # set a timer duration for timer number t_num
        def setTimeDuration(self, t_num, seconds):
                self.timer_seconds[t_num] = seconds

	# sets round number
	def setNum(self, num):
		self.number = num

	# sets the round
	def setRound(self, r):
		self.round = r

	# return name of round
	def getName(self):
		return self.name

	# return number of round
	def getNum(self):
		return self.number

	# return number of round
	def getCCount(self):
		return self.contestantCount

        # get number of questions
        def getQCount(self):
                return self.questionCount

	# set timer durations
	def setDuration(self, i):
		pts = self.question_pts[i]
		if pts == 2:
			self.timer_seconds[i] = 15
		elif pts == 4:
			self.timer_seconds[i] = 30
		elif pts == 6:
			self.timer_seconds[i] = 45
		elif pts == 8:
			self.timer_seconds[i] = 60
		elif pts == 10:
			self.timer_seconds[i] = 90

class Contestant:
	def __init__(self, number):
		## contestant info ##
		self.number = number%6
		if self.number == 0: self.number = 6

		## game variables ##
		# key assignment
		self.key = ""
		if self.number == 1:
			self.key = "i" # contestant 1
		elif self.number == 2:
			self.key = "]" # contestant 2
		elif self.number == 3:
			self.key = "k" # contestant 3
		elif self.number == 4:
			self.key = "p" # contestant 4
		elif self.number == 5:
			self.key = "[" # contestant 5
		elif self.number == 6:
			self.key = "u" # contestant 6
                # current score
                self.score = 0
		# if contestant has buzzed
		self.buzzed = False
		# if contestant can buzz
		self.canBuzz = True
                self.round = Round(1)

	# buzz function for queue
	def buzz(self):
		if self.canBuzz == False:
			return
		self.buzzed = True
		self.canBuzz = False

	# resets contestant's buzz variables
	def unbuzz(self, event):
		self.canBuzz = False
		self.buzzed = False

	# returns contestant's key
	def getKey(self):
		return self.key

        # returns contestant's score
        def getScore(self):
                return self.score

	# returns contestant's number
	def getNum(self):
		return self.number

        def getRound(self):
                return self.round

	# increments score by number of points
	def _plus(self, points):
		self.score += points
                return self.score

	# decrements score by number of points
	def _minus(self, points):
		if (self.score > 0):
			self.score -= points
                return self.score

	# sets the round
	def setRound(self, r):
		self.round = r

class Mainscreen:
        def __init__(self):
          app = tk.Tk()
          self.contestants = []
          self.history = []
          self.history_ptr = -1
          self.contestantCount = 6
          for i in range(self.contestantCount):
            self.contestants.append(Contestant(i+1))
          self.queue = Queue(self.contestantCount)
          self.recent_scorer = ""
          self.control = Controller()
          for i in range(5):
              self.control.rounds.append(Round(i+1))
          self.round = self.control.rounds[0] # placeholder round
          self.questionNumber = 1
          self.time = self.round.timer_seconds[self.questionNumber-1]
          self.timer = Timer(self.time)
          self.winner = 0

	# returns contestant number whose key was pressed
	# if output < 0, key unassigned to contestant
	def searchKey(self, key):
		for i in range(len(self.contestants)):
			if key.upper() == self.contestants[i].getKey().upper():
				return i
		return -1

	# buzz function
	def _buzz(self, char):
                i = self.searchKey(char)

                # searchKey() may return -1, thus self.contestants[-1] may be appended to the queue
                if i >= 0:
                        if self.contestants[i].canBuzz and self.contestants[i] not in self.queue:
                                # if queue is full
                                if (len(self.queue) == self.queue.maxlen):
                                        return len(self.queue)
                                # if not, increment buzzcount
                                else:
                                        self.queue.buzzCount += 1
                                        self.queue.append(self.contestants[i])
                                        return len(self.queue)

                        else:
                            return len(self.queue)

                return len(self.queue)

	def wrong(self):
		if (len(self.queue)):
			self.queue.popleft()
                return len(self.queue)

        def _correct(self):
                self.recent_scorer = self.queue[0]
                return self.recent_scorer.number

        def correct(self):
		if (len(self.queue)):
			self.queue[0]._plus(self.round.question_pts[self.questionNumber-1])
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
			self.reset()
                return self.history_ptr

	def undo(self):
		#if (self.history_ptr > len(self.history)):
		#	recent_action = self.history[-1]
		#	recent_action[0]._minus(recent_action[1])
		#	self.history_ptr -= 1
		if (self.history_ptr >= 0 and self.history_ptr < len(self.history)):
			recent_action = self.history[self.history_ptr]
			recent_action[0]._minus(recent_action[1])
			self.history_ptr -= 1
                return self.history_ptr

	def redo(self):
		#if (self.history_ptr == -1):
		#	self.history_ptr += 1
		#	recent_action = self.history[0]
		#	recent_action[0]._plus(recent_action[1])
		if (self.history_ptr+1 < len(self.history)):
			recent_action = self.history[self.history_ptr+1]
			recent_action[0]._plus(recent_action[1])
			self.history_ptr += 1
                return self.history_ptr

	def checkTies(self):
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

	def getplacers(self):
                self.placers = []
		for i in range(3):
			curr = 0
			for c in self.contestants:
				if c.getScore() > curr:
					self.winner = c
					curr = c.getScore()

			if self.winner != 0:
				self.contestants.remove(self.winner)
				if i == 0:
					self.winner.setRound(4)
					self.control.winners.append(self.winner)
                                        self.placers.append(self.winner.getScore())
				else:
					self.winner.setRound(3)
					self.control.clinchers.append(self.winner)
                                        self.placers.append(self.winner.getScore())
                return self.placers

	# reset contestants and timer
	def reset(self):
		self.timer.reset()
		self.setTimer()
                return self.timer.timer

	def setTimer(self):
		self.timer.setTimer(self.time)

class HowManyRoundsScreen:
    def __init__(self):
        app = tk.Tk()
        self.control = Controller()
        self.checkbox_input = tk.IntVar()

    def toggle(self):
        if (self.checkbox_input.get() == 0):
            self.checkbox_input.set(1)
        else:
            self.checkbox_input.set(0)
        return self.checkbox_input.get()

    def transition(self):
        self.control.preTimerBuzzing = self.checkbox_input.get()
        return self.control.preTimerBuzzing

class Timer:
	def __init__(self, time):
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

	def setTimer(self, time):
		self.timer = time
		self._timer.set(time)

	def reset(self):
		self.ticked = False
		self.paused = True
		self.timer = self.time
		self._timer.set(self.time)

class HowManyRoundsScreenValidation():
	def __init__(self):
                app = tk.Tk()
		self.roundLabel = tk.Entry()
                self.checkbox_input = tk.IntVar()

        def validate_input(self, user_input):
                self.roundLabel.insert(0, user_input)
                try:
                  temp = int(self.roundLabel.get())
                  if (temp < 0):
                      raise ValueError
                  self.roundLabel.delete(0, tk.END)
                  return True
                except ValueError:
                  self.roundLabel.delete(0, tk.END)
                  return False

class RoundNumberandTypeScreen():
	def __init__(self):
                app = tk.Tk()
                self.questionEntry = tk.Entry()
		self.ccountEntry = tk.Entry()

        def validate_input(self, q, c):
                self.questionEntry.insert(0, q)
                self.ccountEntry.insert(0, c)
                try:
                  temp = int(self.questionEntry.get())
                  if (temp < 0):
                      raise ValueError
                  temp = int(self.ccountEntry.get())
                  if (temp < 0):
                      raise ValueError
                  self.questionEntry.delete(0, tk.END)
                  self.ccountEntry.delete(0, tk.END)
                  return True
                except ValueError:
                  self.questionEntry.delete(0, tk.END)
                  self.ccountEntry.delete(0, tk.END)
                  return False

class PointsAndTimerSettingScreen():
	def __init__(self):
                app = tk.Tk()
                self.question_count = 10 # placeholder

        def validate_input(self, q, t):
                for x in range(self.question_count):
                    self.q_entry[x].insert(0, q[x])
                    self.t_entry[x].insert(0, t[x])
                try:
                  for x in range(self.question_count):
                    temp = int(self.q_entry[x].get())
                    if (temp < 0):
                        raise ValueError
                    temp = int(self.t_entry[x].get())
                    if (temp < 0):
                        raise ValueError
                  for x in range(self.question_count):
                    self.q_entry[x].delete(0, tk.END)
                    self.t_entry[x].delete(0, tk.END)
                  return True
                except ValueError:
                  for x in range(self.question_count):
                    self.q_entry[x].delete(0, tk.END)
                    self.t_entry[x].delete(0, tk.END)
                  return False

	def load(self):
                self.q_entry = []
                self.t_entry = []
		for i in range(self.question_count):
			self.q_entry.append(tk.Entry())
			self.t_entry.append(tk.Entry())
