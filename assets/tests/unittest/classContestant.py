from __future__ import print_function
from collections import deque
import sys, datetime # winsound
import Tkinter as tk
import tkFileDialog, tkFont, tkMessageBox
from PIL import Image, ImageOps, ImageDraw, ImageTk
from colors import *
from classRound import *

import time

# conditional import of winsound
is_windows_os = True
try:
	import winsound
except ImportError:
	is_windows_os = False

debug = False
logtofile = False

a = "activitylog"
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



#########		  CONTESTANT 		  #########

class Contestant:
	def __init__(self, number, control, master=None):
		# frame
		self.master = master
		self.control = control

		## contestant info ##
		self.number = number%6
		if self.number == 0: self.number = 6
		#self.name = ""
		#self.school = ""

		## game variables ##
		# key assignment
		self.key = ""
		if self.number == 1:
			self.key = 'i' # contestant 1
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
		# sound assignment
		self.sound = "sounds/"+str(self.number)+".wav"
		# round assignment
		self.round = Round(1)
		# current score
		self.score = 0
		# if contestant has buzzed
		self.buzzed = False
		# if contestant can buzz
		self.canBuzz = True

		## buttons ##
		# photo filename
		self._photo = "images/" + self.getRound().getName().lower() + "/contestant"+str(self.number)+".png"
		# transparent photo filename
		self._t_photo = "images/" + self.getRound().getName().lower() + "/contestant"+str(self.number)+"_t.png"
		# for displaying contestant photo
		self.button = tk.Label(master, bg=light)
		# contestant photo
		self.photo = ""
		# less opacity photo
		self.t_photo = ""
		# contestant score
		self.num_canvas = tk.Label(master, text=self.score, bg=light, bd=0, highlightcolor=light, highlightbackground=light)

		self.setPhoto()

	# sets photo for contestant
	# if contestant photo does not exist, default contestant photos will be displayed
	def setPhoto(self):
		try:
			self.photo = ImageTk.PhotoImage(Image.open(self._photo))
			self.t_photo = ImageTk.PhotoImage(Image.open(self._t_photo))
		except Exception:
			self._photo = "images/" + str(self.getNum()) + ".png"
			self._t_photo = "images/" + str(self.getNum()) + ".png"
		finally:
			self.photo = ImageTk.PhotoImage(Image.open(self._photo))
			self.t_photo = ImageTk.PhotoImage(Image.open(self._t_photo))
			self.button.config(image=self.t_photo)
			self.button.update()
			#self.button.bind("<ButtonPress-1>", self.__on__press)
			#self.button.bind("<ButtonRelease-1>", self.__on__release)
			self.manip_photo()

	# behavior on mousebutton press
	# if upload photo is on display, photo color will invert
	# else, contestant number will be printed on console
	def __on__press(self, event):
		if self._photo == "images/upload1.png":
			self._photo = "images/upload2.png"
			self.photo = ImageTk.PhotoImage(Image.open(self._photo))
			self.button.config(image=self.photo)
			self.button.update()
		else:
			self.control.log("Contestant "+str(self.number))

	# behavior on mousebutton release
	# if upload photo is on display, photo color will revert
	def __on__release(self, event):
		if self._photo == "images/upload2.png":
			self._photo = "images/upload1.png"
			self.photo = ImageTk.PhotoImage(Image.open(self._photo))
			self.button.config(image=self.photo)
			self.button.update()
			self.upload(event)

	# buzz function for queue
	def buzz(self):
		self.set_photo()
		if self.canBuzz == False:
			return
		self.buzzed = True
		# if infinite buzzing: self.canBuzz = True
		# else:
		self.canBuzz = False
		if is_windows_os: winsound.PlaySound(self.getSound(), winsound.SND_FILENAME and winsound.SND_ASYNC)
		self.control.log("Contestant number " + str(self.number) + " has buzzed!")

	def buzz_test(self):
		if is_windows_os: winsound.PlaySound(self.getSound(), winsound.SND_FILENAME and winsound.SND_ASYNC)
		self.control.log("Contestant number " + str(self.number) + " has buzzed!")

	# resets contestant's buzz variables
	def unbuzz(self, event):
		self.canBuzz = False
		self.buzzed = False
		self.set_tphoto()

	# sets the round
	def setRound(self, r):
		self.round = r

	# sets the contestant's buzz sound
	def setSound(self, sound):
		self.sound = sound

	# sets contestant's name
	#def setName(self, name):
	#	self.name = name

	# returns contestant's nane
	#def getName(self):
	#	return self.name

	# sets contestant's key
	def setKey(self, key):
		self.key = key

	# sets contestant's school
	#def setSchool(self, school):
	#	self.school = school

	# returns contestant's school
	#def getSchool(self):
	#	return self.school

	# returns contestant's round
	def getRound(self):
		return self.round

	# returns contestant's sound
	def getSound(self):
		return self.sound

	# sets contestant's score
	def setScore(self,score):
		self.score = score

	# returns contestant's score
	def getScore(self):
		return self.score

	# returns contestant's key
	def getKey(self):
		return self.key

	# returns contestant's number
	def getNum(self):
		return self.number

	# increments score by number of points
	def _plus(self, points):
		self.score += points
		self.num_canvas.config(text=self.getScore(), fg='red')
		self.num_canvas.update()
		time.sleep(0.15)
		self.num_canvas.config(fg='black')
		self.num_canvas.update()

	# decrements score by number of points
	def _minus(self, points):
		if (self.score > 0):
			self.score -= points
			self.num_canvas.config(text=self.getScore(), fg='red')
			self.num_canvas.update()
			time.sleep(0.15)
			self.num_canvas.config(fg='black')
			self.num_canvas.update()

	# plays correct sound
	def correct(self):
		if is_windows_os: winsound.PlaySound("sounds/correct.wav", winsound.SND_FILENAME and winsound.SND_ASYNC)

	# plays wrong sound
	def wrong(self):
		if is_windows_os: winsound.PlaySound("sounds/correct.wav", winsound.SND_FILENAME and winsound.SND_ASYNC)

	# prints all contestant's attributes
	def getAll(self):
		self.control.log("Contestant #" + str(self.getNum()))
		#self.control.log("Name: " + self.getName())
		#self.control.log("School: " + self.getSchool())
		self.control.log("Key: " + self.getKey())
		self.control.log("Sound: " + self.getSound())
		self.control.log("Round: " + self.getRound().getName())

	# set button as transparent photo
	def set_tphoto(self):
		self.button.config(image=self.t_photo, bg=light)
		self.button.update()

	# set button as visible photo
	def set_photo(self):
		self.button.config(image=self.photo, bg=light_txt)
		self.button.update()

	# browses for a contestant photo
	def upload(self, event):
		self._upload()

	def _upload(self):
		path = tkFileDialog.askopenfilename(filetypes=[('Image files',('.png','.jpg', '.jpeg'))], title='Choose contestant photo', initialdir='/images/')
		# handles exception if file is not found or no filename was entered.
		# finds a photo named (self.number).png or .jpg if no filename was entered
		try:
			im = Image.open(path)
		except IOError:
			try:
				path = "images/"+str(self.number)+".png"
				im = Image.open(path)
			except IOError:
				self.control.log("Error: " + str(self.number) + ".png not found")
				path = "images/"+str(self.number)+".jpg"
				self.control.log("Setting " + str(self.number) + ".jpg as path")
				im = Image.open(path)
		except:
			self.control.log("No contestant photo found.")
		finally:
			self.control.log("File found. Photo for contestant " + str(self.number) + " has been set.")
			self.manip_photo(path)
			self.button.update()

	# manipulates photo into a circular photo
	def manip_photo(self, path=None):
		size = (190, 190)
		mask = Image.open('images/mask.png').convert('L')
		t_mask = Image.open('images/t_mask.png').convert('L')
		draw = ImageDraw.Draw(mask)
		t_draw = ImageDraw.Draw(t_mask)
		draw.ellipse((0,0) + size, fill=255)
		if path:
			im = Image.open(path)
		else:
			path = "images/"+str(self.number)+".png"
			im = Image.open(path)
		self.photo = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
		self.photo.putalpha(mask)
		self.photo.save("images/" + self.getRound().getName().lower() + '/contestant'+str(self.number)+'.png')
		self.t_photo = ImageOps.fit(im, t_mask.size, centering=(0.5, 0.5))
		self.t_photo.putalpha(t_mask)
		self.t_photo.save("images/" + self.getRound().getName().lower() + '/contestant'+str(self.number)+'_t.png')
		self.t_photo = ImageTk.PhotoImage(Image.open("images/" + self.getRound().getName().lower() + '/contestant'+str(self.number)+'_t.png'))
		self.photo = ImageTk.PhotoImage(Image.open("images/" + self.getRound().getName().lower() + '/contestant'+str(self.number)+'_t.png'))
		self._photo = "images/" + self.getRound().getName().lower() + '/contestant'+str(self.number)+'.png'
		self.button.config(image=self.t_photo)

#########		  CUSTOM BUTTON 		  #########

class CustomButton(tk.Canvas):
	def __init__(self, parent, width, height, txt, bg, fg, command):
		## initialization variables ##
		self.bg = bg
		self.fg = fg
		self.command = command
		self.text = (True if txt else False)
		self.font = tkFont.Font(family='Consolas', size=50, weight='bold')
		self.parent = parent
		tk.Canvas.__init__(self, parent, borderwidth=1, relief=tk.FLAT, highlightthickness=0, bg=self.bg)
		padding = 4
		self.oval_id = self.create_oval(padding, padding, width+padding, height+padding, outline=self.fg)
		if self.text: self.text_id = self.create_text((width)/2+padding,(height)/2+padding, text=txt, fill=self.fg)
		(x0,y0,x1,y1) = self.bbox("all")
		width = (x1-x0) + padding
		height = (y1-y0) + padding
		self.configure(width=width, height=height)
		self.bind("<ButtonPress-1>", self.__on__press)
		self.bind("<ButtonRelease-1>", self.__on__release)

	# behavior on mousebutton press
	def __on__press(self, event):
		self.itemconfigure(self.oval_id, fill=self.fg)
		if self.text: self.itemconfigure(self.text_id, fill=self.bg)
		self.command()

	# behavior on mousebutton release
	def __on__release(self, event):
		self.itemconfigure(self.oval_id, fill=self.bg)
		if self.text: self.itemconfigure(self.text_id, fill=self.fg)
		self.update()
