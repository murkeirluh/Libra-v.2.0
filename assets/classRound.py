from __future__ import print_function
from collections import deque
import sys, datetime, os
import Tkinter as tk
import tkFileDialog, tkFont, tkMessageBox
from PIL import Image, ImageOps, ImageDraw, ImageTk
from colors import *
import time


debug = True
logtofile = True

# check directory
dirc = os.getcwd().split('\\')
path = ""
if dirc[-1] != 'libra': 
	dirc = dirc[:dirc.index('libra')+1]
	for d in dirc:
		path += d + "\\"
	os.chdir(path)

a = "assets/logs/activitylog"
b = ".txt"
timestr = time.strftime("%Y%m%d")
a = a + timestr + b
logfile = open(a, "a")

def _debug(*args, **kwargs):
	if debug:
		print("[DEBUG]", *args, file=sys.stderr, **kwargs)

def log(*args, **kwargs):
	if logtofile:
		print("[" + str(datetime.datetime.now()) + "]", *args, file=logfile, **kwargs)


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
