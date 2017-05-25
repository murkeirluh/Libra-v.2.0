import unittest, random
import Libra, Mainscreen, classBuzzerTest
from colors import *
from classController import *

global control
control = Controller()

###### classes ###### 
# event simulator
class Event:
	def __init__(self, key):
		self.char = key
		self.keysym = key


# test case
class TestButtons(unittest.TestCase):
	def test_undo_redo(self):
		print("\n================================TEST UNDO/REDO================================")
		current = control.states[0]
		# tuple
		item = (current.contestants[0], current.round.question_pts[current.questionNumber-1])
		# score variable
		k = 6
		# first contestant buzzes thrice
		for t in range(3):
			# first contestant buzzes
			current._buzz(Event('i'))
			# simulate correct answer
			current.correct(Event('i'))
			# recent tuple in history array is item
			self.assertTupleEqual(current.history[-1], item)
			# size of history array is t+1
			self.assertEqual(len(current.history), t+1)
			# history pointer is at t
			self.assertEqual(current.history_ptr, t)

		# size of history array is 3
		self.assertEqual(len(current.history), 3)
		# history_ptr undo variable
		u = 2

		# undo score thrice
		for t in range(3):
			# check if contestant #1's score is k
			self.assertEqual(current.contestants[0].getScore(), k)
			# decrement k by 2
			k -= 2
			# undo contestant's recent score
			current.undo()
			# check if history_ptr == u
			self.assertEqual(current.history_ptr, u-1)
			# decrement u
			u -= 1
			# check if contestant's score is (decremented) k 
			self.assertEqual(current.contestants[0].getScore(), k)

		# redo score thrice
		for t in range(3):
			# check if contestant #1's score is k
			self.assertEqual(current.contestants[0].getScore(), k)
			# increment k by 2
			k += 2
			# undo contestant's recent score
			current.redo()
			# increment u
			u += 1
			# check if history_ptr == u
			self.assertEqual(current.history_ptr, u)
			# check if contestant's score is (incremented) k 
			self.assertEqual(current.contestants[0].getScore(), k)
		u = 2
		# re-undo score thrice
		for t in range(3):
			# check if contestant #1's score is k
			self.assertEqual(current.contestants[0].getScore(), k)
			# decrement k by 2
			k -= 2
			# undo contestant's recent score
			current.undo()
			# check if history_ptr == u
			self.assertEqual(current.history_ptr, u-1)
			# decrement u
			u -= 1
			# check if contestant's score is (decremented) k 
			self.assertEqual(current.contestants[0].getScore(), k)
		
		# buzz contestant #2
		current._buzz(Event(']'))
		current.correct(Event(']'))
		# new item
		item = (current.contestants[1], current.round.question_pts[current.questionNumber-1])
		self.assertEqual(current.history[-1], item)
		self.assertEqual(current.history_ptr, 0)
		self.assertEqual(current.contestants[1].getScore(), current.round.question_pts[current.questionNumber-1])
		self.assertEqual(len(current.history), 1)

		# undo twice
		for t in range(2):
			current.undo()
			self.assertEqual(current.history_ptr, -1)
			self.assertEqual(current.contestants[1].getScore(), 0)

		# buzz 1
		current._buzz(Event('i'))
		current.correct(Event('i'))
		self.assertEqual(current.history_ptr, 0)
		# buzz 2
		current._buzz(Event(']'))
		current.correct(Event(']'))
		self.assertEqual(current.history_ptr, 1)
		self.assertEqual(current.contestants[0].getScore(), current.contestants[1].getScore())

		# undo
		current.undo()
		self.assertEqual(current.history_ptr, 0)
		self.assertEqual(current.contestants[1].getScore(), 0)

		# redo twice
		for t in range(2):
			current.redo()
			self.assertEqual(current.history_ptr, 1)
			self.assertEqual(current.contestants[0].getScore(), current.contestants[1].getScore())
			self.assertEqual(current.contestants[0].getScore(), current.round.question_pts[current.questionNumber-1])
			self.assertEqual(current.contestants[1].getScore(), current.round.question_pts[current.questionNumber-1])

		current._buzz(Event('i'))
		current.correct(Event('i'))
		self.assertEqual(current.history_ptr, 2)
		self.assertEqual(current.contestants[0].getScore(), 4)

	def runTest(self):
		self.test_undo_redo()


class TestReset(unittest.TestCase):
	# timer should reset, after correct(), question number should not increment first
	def test_increment_decrement(self):
		print("\n================================TEST INCREMENT================================")
		current = control.states[0]
		# reset contestant #1's score
		current.contestants[0].setScore(0)
		# buzz and mark as correct thrice
		for i in range(3):
			current._buzz(Event('i'))
			current.correct(Event('i'))
			# score should be [current_pts] * 3
			self.assertEqual(current.contestants[0].getScore(), current.round.question_pts[current.questionNumber-1] * (i+1))
			# time should be reset
			self.assertEqual(current.timer.time, current.round.timer_seconds[current.questionNumber-1])
			self.assertEqual(current.timer.label["text"], current.timer.time)
			# question number has not changed
			self.assertEqual(current.questionNumber, 1)

		for i in range(5):
			current.increment()
			self.assertEqual(current.time, current.round.timer_seconds[current.questionNumber-1])
			# question number has changed
			self.assertEqual(current.questionNumber, i+2)

			
		print("\n================================TEST DECREMENT================================")
		# decrement thrice
		for i in range(5, 0, -1):
			current.decrement()
			self.assertEqual(current.timer.time, current.round.timer_seconds[current.questionNumber-1])
			self.assertEqual(current.timer.label["text"], current.timer.time)
			# question number has changed
			self.assertEqual(current.questionNumber, i)

class TestCheckTies(unittest.TestCase):
	def test_checkties(self):
		print("\n===============================TEST CHECKTIES==============================")
		current = control.states[0]

		for i in range(6):
			current.contestants[i].setScore(5)

		self.assertTrue(current.checkTies())

		for i in range(6):
			current.contestants[i].setScore(i)

		self.assertFalse(current.checkTies())

		for i in range(6):
			current.contestants[i].setScore(0)

		self.assertFalse(current.checkTies())

		for i in range(2):
			current.contestants[i].setScore(i+1)

		self.assertFalse(current.checkTies())

class TestBuzzers(unittest.TestCase):
	def test_Buzzers(self):
		print("\n=============================TEST BUZZERS===============================")
		current = control.states[1]

		for i in range(6):
			current.buzz_test(i)
			self.assertEqual(current.buzzLabel.cget("text"), "Buzzer #"+ str(i+1) + " is okay!")

	def runTest(self):
		self.test_Buzzers()

class TestDefaultSoundsandPhotos(unittest.TestCase):
	def test_DefaultSounds(self):
		print("\n=============================TEST SOUNDS===============================")
		current = control.states[0]
		for i in range(6):
			self.assertEqual(current.contestants[i].getSound(), "sounds/"+str(i+1)+".wav")

		print("\n=============================TEST PHOTOS===============================")
		for i in range(6):
			self.assertEqual(current.contestants[i]._photo, "images/"+ current.contestants[i].getRound().getName().lower()+ "/contestant" + str(i+1) + ".png")



if __name__ == '__main__':
	_libra = Libra.__Libra__(control)
	control.root.wm_deiconify()

	control.counter = 1
	control.states.append(Mainscreen.__MainScreen__(control, control.rounds[0]))
	control.states.append(classBuzzerTest.BuzzerTestScreen(control))
	_libra.load()
	unittest.main()