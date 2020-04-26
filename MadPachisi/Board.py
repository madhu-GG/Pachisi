from MadPachisi.constants import *
from MadPachisi.Player import Player
import random

class Board(object):
    def __init__(self, num_players: int):
        """
        :type num_players: int
        """
        assert(isinstance(num_players, int))
        assert(PlayerConsts.MINIMUM <= num_players <= PlayerConsts.MAXIMUM)

        self.NumPlayers = num_players
        # board will be a dictionary with key = position, and value is a list of players
        self.Board = dict()
        self.Players = [Player(i) for i in range(1, num_players + 1)]
        self.CurrentPlayerNum = 1
        self.CurrentPlayer = self.Players[self.CurrentPlayerNum - 1]
        self.Winners = []
        self.GameOver = False

    def NextPlayer(self):
        if len(self.Winners) >= self.NumPlayers - 1:
            self.GameOver = True
            return

        while(True):
            if self.CurrentPlayerNum == self.NumPlayers:
                self.CurrentPlayerNum = 1
            else:
                self.CurrentPlayerNum += 1

            self.CurrentPlayer = self.Players[self.CurrentPlayerNum - 1]
            if self.CurrentPlayer not in self.Winners:
                break

    def MoveCurrentPlayerPiece(self, piece_num: int, count: int):
        assert(1 <= count <= 6)
        assert(1 <= piece_num <= PlayerConsts.PIECES_PER_PLAYER)

        piece = self.CurrentPlayer.GetPiece(piece_num)
        old_position = piece.position

        if not(self.CurrentPlayer.CanMoveForward(piece_num, count)):
            return False
        else:
            retVal = self.CurrentPlayer.MoveForward(piece_num, count)
            if retVal == True:
                self.RemovePieceFromPosition(piece, old_position)
                self.AddPieceToPosition(piece, piece.position)
                # don't capture other's pieces in winning ramp
                if piece.position <= BoardConsts.MAX_BOXES:
                    self.CaptureOthersInPosition(piece.position)

            if self.CurrentPlayer.CheckWinCondition() == True:
                self.Winners.append(self.CurrentPlayer)

            return retVal


    def AddPieceToPosition(self, piece, position: int):
        assert (0 <= position <= BoardConsts.WINNING_POSITION)

        if self.Board.get(position) is not None:
            self.Board[position].append(piece)
        else:
            self.Board[position] = [piece]


    def RemovePieceFromPosition(self, piece, position: int):
        assert (0 <= position <= BoardConsts.WINNING_POSITION)

        pieces_in_pos = self.Board.get(position)

        # the piece is not found in that position
        if (pieces_in_pos is None) or (piece not in pieces_in_pos):
            return False
        else:
            pieces_in_pos.remove(piece)
            return True

    def CaptureOthersInPosition(self, position: int):
        pieces_in_pos = self.Board.get(position)

        for piece in pieces_in_pos:
            if piece.player != self.CurrentPlayerNum:
                self.Players[piece.player - 1].CapturePiece(piece.number)
                self.RemovePieceFromPosition(piece, position)
                self.AddPieceToPosition(piece, BoardConsts.OUTSIDE_POSITION)

if __name__ == "__main__":
    random.seed()
    try:
        roll_no = 0
        mboard = Board(2)
        print("Num Players == {}".format(mboard.NumPlayers))

        while not mboard.GameOver:
            roll_no += 1
            print("Roll Number: {} ########################################################".format(roll_no))
            print ("Player positions: ")
            for player in mboard.Players:
                print(player)
            print ("==> Rolling Dice!")
            dice = random.randint(1, 6)

            print("Rolled a {}".format(dice))

            movable = list(mboard.CurrentPlayer.GetMoveablePieces(dice))

            if len(movable) == 1:
                print("Moving only piece = {}".format(movable[0]))
                mboard.MoveCurrentPlayerPiece(movable[0].number, dice)
            elif len(movable) > 1:
                print("Current Player: {}".format(mboard.CurrentPlayer))
                while(True):
                    piece_num = int(input("You Rolled a {}, Select piece (1-4):".format(dice)))
                    if mboard.MoveCurrentPlayerPiece(piece_num, dice):
                        break
                    else:
                        print("Invalid Move!")

            mboard.NextPlayer()

        print(mboard.Winners)

    except RuntimeError as e:
        print(e)
    else:
        print("Initialized board successfully!")
