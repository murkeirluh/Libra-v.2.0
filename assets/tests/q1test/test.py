import unittest
import Q1_code

test = Q1_code.Mainscreen()
test2 = Q1_code.Mainscreen()
checkbox = Q1_code.HowManyRoundsScreen()
validate1 = Q1_code.HowManyRoundsScreenValidation()
validate2 = Q1_code.RoundNumberandTypeScreen()
validate3 = Q1_code.PointsAndTimerSettingScreen()

class Unit_Test(unittest.TestCase):
  def test_buzzers(self):
    # valid inputs (keys assigned to a buzzer)
    self.assertEqual(0, test.searchKey("i"))
    self.assertEqual(1, test.searchKey("]"))
    self.assertEqual(2, test.searchKey("k"))
    self.assertEqual(3, test.searchKey("p"))
    self.assertEqual(4, test.searchKey("["))
    self.assertEqual(5, test.searchKey("u"))
    self.assertEqual(0, test.searchKey("I"))
    self.assertEqual(2, test.searchKey("K"))
    self.assertEqual(3, test.searchKey("P"))
    self.assertEqual(5, test.searchKey("U"))

    # invalid: keys not assigned to any buzzer
    self.assertEqual(-1, test.searchKey("y"))
    self.assertEqual(-1, test.searchKey("Q"))
    self.assertEqual(-1, test.searchKey("4"))
    self.assertEqual(-1, test.searchKey("*"))
    # invalid: empty input
    self.assertEqual(-1, test.searchKey(""))

  def test_recent_scorer(self):
    self.assertEqual(0, test.wrong()) # invalid: min - 1

    self.assertEqual(0, test._buzz("")) # valid: min
    self.assertEqual(1, test._buzz("i")) # valid: min + 1
    self.assertEqual(2, test._buzz("]"))
    self.assertEqual(2, test._buzz("]")) # note: pressing "]" again will yield same length of queue since contestant has buzzed already
    self.assertEqual(3, test._buzz("k"))
    self.assertEqual(4, test._buzz("p"))
    self.assertEqual(5, test._buzz("[")) # valid: max - 1
    self.assertEqual(6, test._buzz("u")) # valid: max

    self.assertEqual(6, test._buzz("u")) # invalid: max + 1 (queue is full)

    # current state of queue: Contestant 1, 2, ..., 6
    self.assertEqual(1, test._correct()) # recent scorer is Contestant 1
    self.assertEqual(5, test.wrong()) # pop Contestant 1 from queue
    self.assertEqual(2, test._correct()) # recent scorer is Contestant 2
    self.assertEqual(4, test.wrong()) # pop Contestant 2 from queue
    self.assertEqual(3, test._correct())
    self.assertEqual(3, test.wrong())
    self.assertEqual(4, test._correct())
    self.assertEqual(2, test.wrong())
    self.assertEqual(5, test._correct())
    self.assertEqual(1, test.wrong())
    self.assertEqual(6, test._correct())
    self.assertEqual(0, test.wrong())

  def test_check_ties(self):
    self.assertEqual(False, test.checkTies()) # contestants' scores are all 0. this should NOT be recognized as a tie
    self.assertEqual(7, test.contestants[0]._plus(7)) # set a contestant's score to 7
    self.assertEqual(False, test.checkTies()) # no ties still
    self.assertEqual(7, test.contestants[4]._plus(7)) # set another contestant with same score
    self.assertEqual(True, test.checkTies()) # there should now be a tie

  def test_get_placers(self):
    self.assertEqual([], test2.getplacers()) # no one should have a place

    self.assertEqual(7, test2.contestants[0]._plus(7)) # set a contestant's score to 7
    self.assertEqual(6, test2.contestants[4]._plus(6))
    self.assertEqual(5, test2.contestants[5]._plus(5))

    self.assertEqual([7,6,5], test2.getplacers()) # now placers should exist

    self.assertEqual(4, test2.control.winners[0].getRound()) # 1st placer should be in Final round (5th round if default round settings are set)
    self.assertEqual(3, test2.control.clinchers[0].getRound()) # 2nd placer should be in Wildcard Round (4th round if default round settings are set)
    self.assertEqual(3, test2.control.clinchers[1].getRound()) # 3rd placer should be in Wildcard Round (4th round if default round settings are set)

  def test_checkbox(self):
    self.assertEqual(1, checkbox.toggle()) # checkbox is set to 0 by default
    self.assertEqual(True, checkbox.transition()) # is preTimerBuzzing indeed set to 1
    self.assertEqual(0, checkbox.toggle())
    self.assertEqual(False, checkbox.transition())

  def test_timer_reset(self):
    self.assertEqual(15, test.reset())

  def test_undo_redo(self):
    # this fxn tests the values of history_ptr in Mainscreen.py
    # values of history_ptr = [-1] union S, where S is a set containing valid indices of the array history (i.e. elements are nonnegative)
    self.assertEqual(-1, test.undo()) # invalid: S = [], h_p = -2
    self.assertEqual(-1, test.redo()) # invalid: S = [], h_p = 0

    # fill up queue
    self.assertEqual(1, test._buzz("i"))
    self.assertEqual(2, test._buzz("]"))
    self.assertEqual(3, test._buzz("k"))
    self.assertEqual(4, test._buzz("p"))
    self.assertEqual(5, test._buzz("["))
    self.assertEqual(6, test._buzz("u"))

    self.assertEqual(0, test.correct()) # valid: S = [0], h_p = 0

    self.assertEqual(0, test.redo()) # invalid: S = [0], h_p = 1
    self.assertEqual(-1, test.undo()) # valid: S = [0], h_p = -1
    self.assertEqual(-1, test.undo()) # invalid: S = [0], h_p = -2
    self.assertEqual(0, test.redo()) # valid: S = [0], h_p = 0

    # fill up queue
    self.assertEqual(1, test._buzz("i"))
    self.assertEqual(2, test._buzz("]"))
    self.assertEqual(3, test._buzz("k"))
    self.assertEqual(4, test._buzz("p"))
    self.assertEqual(5, test._buzz("["))
    self.assertEqual(6, test._buzz("u"))

    self.assertEqual(1, test.correct()) # valid: S = [0,1], h_p = 1

    # fill up queue
    self.assertEqual(1, test._buzz("i"))
    self.assertEqual(2, test._buzz("]"))
    self.assertEqual(3, test._buzz("k"))
    self.assertEqual(4, test._buzz("p"))
    self.assertEqual(5, test._buzz("["))
    self.assertEqual(6, test._buzz("u"))

    self.assertEqual(2, test.correct()) # valid: S = [0,1,2], h_p = 2

    # fill up queue
    self.assertEqual(1, test._buzz("i"))
    self.assertEqual(2, test._buzz("]"))
    self.assertEqual(3, test._buzz("k"))
    self.assertEqual(4, test._buzz("p"))
    self.assertEqual(5, test._buzz("["))
    self.assertEqual(6, test._buzz("u"))

    self.assertEqual(3, test.correct()) # valid: S = [0,1,2,3], h_p = 3

    # fill up queue
    self.assertEqual(1, test._buzz("i"))
    self.assertEqual(2, test._buzz("]"))
    self.assertEqual(3, test._buzz("k"))
    self.assertEqual(4, test._buzz("p"))
    self.assertEqual(5, test._buzz("["))
    self.assertEqual(6, test._buzz("u"))

    self.assertEqual(4, test.correct()) # valid: S = [0,1,2,3,4], h_p = 4

    # fill up queue
    self.assertEqual(1, test._buzz("i"))
    self.assertEqual(2, test._buzz("]"))
    self.assertEqual(3, test._buzz("k"))
    self.assertEqual(4, test._buzz("p"))
    self.assertEqual(5, test._buzz("["))
    self.assertEqual(6, test._buzz("u"))

    self.assertEqual(5, test.correct()) # valid: S = [0,1,2,3,4,5], h_p = 5

    # fill up queue
    self.assertEqual(1, test._buzz("i"))
    self.assertEqual(2, test._buzz("]"))
    self.assertEqual(3, test._buzz("k"))
    self.assertEqual(4, test._buzz("p"))
    self.assertEqual(5, test._buzz("["))
    self.assertEqual(6, test._buzz("u"))

    self.assertEqual(6, test.correct()) # valid: S = [0,1,2,3,4,5,6], h_p = 6

    self.assertEqual(6, test.redo()) # invalid: S = [0,1,2,3,4,5,6], h_p = 7

    self.assertEqual(5, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = 5
    self.assertEqual(6, test.redo()) # valid: S = [0,1,2,3,4,5,6], h_p = 6
    self.assertEqual(5, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = 5

    self.assertEqual(4, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = 4
    self.assertEqual(5, test.redo()) # valid: S = [0,1,2,3,4,5,6], h_p = 5
    self.assertEqual(4, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = 4

    self.assertEqual(3, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = 3
    self.assertEqual(4, test.redo()) # valid: S = [0,1,2,3,4,5,6], h_p = 4
    self.assertEqual(3, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = 3

    self.assertEqual(2, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = 2
    self.assertEqual(3, test.redo()) # valid: S = [0,1,2,3,4,5,6], h_p = 3
    self.assertEqual(2, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = 2

    self.assertEqual(1, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = 1
    self.assertEqual(2, test.redo()) # valid: S = [0,1,2,3,4,5,6], h_p = 2
    self.assertEqual(1, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = 1

    self.assertEqual(0, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = 0
    self.assertEqual(1, test.redo()) # valid: S = [0,1,2,3,4,5,6], h_p = 1
    self.assertEqual(0, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = 0

    self.assertEqual(-1, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = -1
    self.assertEqual(0, test.redo()) # valid: S = [0,1,2,3,4,5,6], h_p = 0
    self.assertEqual(-1, test.undo()) # valid: S = [0,1,2,3,4,5,6], h_p = -1

    self.assertEqual(-1, test.undo()) # invalid: S = [0,1,2,3,4,5,6], h_p = -2

  def test_number_of_rounds(self):
    self.assertEqual(True, validate1.validate_input("2"))
    self.assertEqual(True, validate1.validate_input("    3"))
    self.assertEqual(False, validate1.validate_input(""))
    self.assertEqual(False, validate1.validate_input("asdf"))
    self.assertEqual(False, validate1.validate_input("234!#$"))
    self.assertEqual(False, validate1.validate_input(" "))
    self.assertEqual(True, validate1.validate_input("0"))
    self.assertEqual(False, validate1.validate_input("-1"))

  def test_number_of_q_contestants(self):
    # number of Qs INVALID; number of contestants INVALID
    self.assertEqual(False, validate2.validate_input(" ", " "))
    self.assertEqual(False, validate2.validate_input("234!#$", "!"))
    self.assertEqual(False, validate2.validate_input("asdf", "as"))
    self.assertEqual(False, validate2.validate_input("", ""))
    self.assertEqual(False, validate2.validate_input("-1", "-1"))

    # number of Qs INVALID; number of contestants VALID
    self.assertEqual(False, validate2.validate_input("", "1"))
    self.assertEqual(False, validate2.validate_input("-1", "1"))

    # number of Qs VALID; number of contestants INVALID
    self.assertEqual(False, validate2.validate_input("1", ""))

    # number of Qs VALID; number of contestants VALID
    self.assertEqual(True, validate2.validate_input("2", "1"))
    self.assertEqual(True, validate2.validate_input("2", "0"))
    self.assertEqual(True, validate2.validate_input("    3", " 2"))
    self.assertEqual(True, validate2.validate_input("0", "0"))

  def test_points_timer(self):
    # points INVALID; timer durations INVALID
    q_pts = []
    t_duration = []
    question_count = 10 # placeholder
    for x in range(question_count):
      q_pts.append(str(x))
      t_duration.append(str(x))
    q_pts[0] = "R#@#$"
    t_duration[0] = ""
    validate3.load()
    self.assertEqual(False, validate3.validate_input(q_pts, t_duration))

    # points INVALID; timer durations VALID
    q_pts = []
    t_duration = []
    question_count = 10 # placeholder
    for x in range(question_count):
      q_pts.append(str(x))
      t_duration.append(str(x))
    q_pts[0] = "   "
    validate3.load()
    self.assertEqual(False, validate3.validate_input(q_pts, t_duration))

    # points VALID; timer durations INVALID
    q_pts = []
    t_duration = []
    question_count = 10 # placeholder
    for x in range(question_count):
      q_pts.append(str(x))
      t_duration.append(str(x))
    t_duration[0] = "-1"
    validate3.load()
    self.assertEqual(False, validate3.validate_input(q_pts, t_duration))

    # points VALID; timer durations VALID
    q_pts = []
    t_duration = []
    question_count = 10 # placeholder
    for x in range(question_count):
      q_pts.append(str(x))
      t_duration.append(str(x))
    validate3.load()
    self.assertEqual(True, validate3.validate_input(q_pts, t_duration))

unittest.main()
