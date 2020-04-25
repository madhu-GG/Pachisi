import unittest
from MadPachisi.Board import Board
from MadPachisi.Player import PlayerCount


class BoardCreateUnitTest(unittest.TestCase):
    num_players_test = [1, 2, 3, 4, 5, 0, "hello", 2.3, 3.4, -2, -3, -4]
    def test_Board(self):
        for num in self.num_players_test:
            self.exception_raised = False
            try:
                b = Board(num)
            except TypeError as te:
                self.exception_raised = True
                if isinstance(num, int) or isinstance(num, float):
                    self.fail("TypeError should not be raised for number = {}".format(num))
            except RuntimeError as e:
                self.exception_raised = True
                if isinstance(num, int) and PlayerCount.MINIMUM <= num <= PlayerCount.MAXIMUM:
                    self.fail("Should not throw Error for {} when min. "
                              "players = {}, and max. players = {}".format(num, PlayerCount.MINIMUM,
                                                                           PlayerCount.MAXIMUM))
            else:
                if not(isinstance(num, int)) or (num < PlayerCount.MINIMUM or num > PlayerCount.MAXIMUM):
                    self.fail("Should raise Error for {} number of players for given min. "
                              "players = {}, and max. players = {}".format(num, PlayerCount.MINIMUM,
                                                                       PlayerCount.MAXIMUM))


if __name__ == '__main__':
    unittest.main()
