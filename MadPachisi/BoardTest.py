import unittest

from MadPachisi.Board import Board
from MadPachisi.constants import *


class BoardCreateUnitTest(unittest.TestCase):
    num_players_test = [1, 2, 3, 4, 5, 0, "hello", 2.3, 3.4, -2, -3, -4, None, [], ()]

    def test_Board(self):
        for num in self.num_players_test:
            self.exception_raised = False
            try:
                b = Board(num)
            except AssertionError as e:
                self.exception_raised = True
                if isinstance(num, int) and PlayerConsts.MINIMUM <= num <= PlayerConsts.MAXIMUM:
                    self.fail("Should not throw Error for {} when min. "
                              "players = {}, and max. players = {}".format(num, PlayerConsts.MINIMUM,
                                                                           PlayerConsts.MAXIMUM))
            else:
                if not(
                        (isinstance(num, int)) and
                        (PlayerConsts.MINIMUM <= num <= PlayerConsts.MAXIMUM)):
                    self.fail("Should raise Error for {} number of players for given min. "
                              "players = {}, and max. players = {}".format(num, PlayerConsts.MINIMUM,
                                                                       PlayerConsts.MAXIMUM))


if __name__ == '__main__':
    unittest.main()
