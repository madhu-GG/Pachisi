from MadPachisi.constants import *


class Piece(object):
    position: int
    player: int

    def __init__(self, number: int, player: int):
        self.number = number
        self.player = player
        self.position = BoardConsts.OUTSIDE_POSITION

    def __str__(self):
        return "Piece number: {}, Player number: {}, Current Position: {}\n".format(
            self.number, self.player, self.position
        )

    def CanMoveForward(self, count: int):
        assert (1 <= count <= 6)

        # if the piece already made it to the last square then can't move it
        if self.position == BoardConsts.WINNING_POSITION:
            return False
        # piece can be brought in only by rolling a 6 on the dice
        elif self.position == BoardConsts.OUTSIDE_POSITION:
            if count == 6:
                return True
            else:
                return False
        # piece is on the winning ramp from 53 to 58
        elif self.position > BoardConsts.MAX_BOXES:
            # cannot move past the winning square
            if count + self.position > BoardConsts.WINNING_POSITION:
                return False
            else:
                return True
        else:
            # can move forward in the board
            return True

    def MoveForward(self, start_position, end_position, count):
        assert (1 <= start_position <= BoardConsts.MAX_BOXES)
        assert (1 <= end_position <= BoardConsts.MAX_BOXES)
        assert (1 <= count <= 6)

        # if the piece already made it to the last square then can't move it
        if self.position == BoardConsts.WINNING_POSITION:
            return False
        # piece can be brought in only by rolling a 6 on the dice
        elif self.position == BoardConsts.OUTSIDE_POSITION:
            if count == 6:
                self.position = start_position
            else:
                return False
        # piece is on the winning ramp from 53 to 58
        elif self.position > BoardConsts.MAX_BOXES:
            # cannot move past the winning square
            if count + self.position > BoardConsts.WINNING_POSITION:
                return False
            else:
                self.position += count
        # if the move causes the piece to move from the main board to the winning ramp,
        # then calculate the amount to be moved from start of the winning ramp
        elif self.position <= end_position and self.position + count > end_position:
            total = self.position + count
            overflow = total - end_position

            if BoardConsts.MAX_BOXES + overflow > BoardConsts.WINNING_POSITION:
                return False

            self.position = BoardConsts.MAX_BOXES + overflow
        else:
            # move forward in the board
            self.position = (self.position + count) % BoardConsts.MAX_BOXES

        return True

    def SetPosition(self, position: int):
        assert (0 <= position <= BoardConsts.WINNING_POSITION)
        self.position = position


class Player(object):
    def __init__(self, player_num: int):
        assert (isinstance(player_num, int) and (0 < player_num <= PlayerConsts.MAXIMUM))

        # Start position is the second square on the player's quadrant
        # Finishing square is start - 2 or 52 - (Start - 2)
        self.Number = player_num
        self.StartPosition = (player_num - 1) * BoardConsts.PLAYER_OFFSET + 2
        self.EndPosition = self.StartPosition - 2
        if self.EndPosition <= 0:
            self.EndPosition = BoardConsts.MAX_BOXES + self.EndPosition

        self.Pieces = [Piece(i, player_num) for i in range(1, 5)]

    def __str__(self):
        retVal = "Player Number: {}\nStart: {}\n End: {}\n".format(
            self.Number, self.StartPosition, self.EndPosition)

        for piece in self.Pieces:
            retVal += '\n' + str(piece)

        return retVal

    def MoveForward(self, piece_num: int, count: int):
        assert (1 <= piece_num <= 4)

        if self.CanMoveForward(piece_num, count):
            piece = self.Pieces[piece_num - 1]
            previous_position = piece.position
            retVal = piece.MoveForward(self.StartPosition, self.EndPosition, count)

            assert (previous_position != piece.position)
            return retVal
        else:
            return False

    def CanMoveForward(self, piece_num: int, count: int):
        assert (1 <= piece_num <= PlayerConsts.PIECES_PER_PLAYER)
        piece = self.Pieces[piece_num - 1]
        return piece.CanMoveForward(count)

    def CheckWinCondition(self):
        pieces_reached_winning = [piece.position == BoardConsts.WINNING_POSITION for piece in self.Pieces]
        if False in pieces_reached_winning:
            return False
        else:
            return True

    def CapturePiece(self, piece_num: int):
        assert (1 <= piece_num <= PlayerConsts.PIECES_PER_PLAYER)
        piece = self.Pieces[piece_num - 1]
        piece.SetPosition(BoardConsts.OUTSIDE_POSITION)

    def GetPiece(self, piece_num: int):
        return self.Pieces[piece_num - 1]

    def GetPiecesInPosition(self, position: int):
        return filter(lambda piece: piece.position == position, self.Pieces)

    def GetMoveablePieces(self, count: int):
        return filter(lambda piece: piece.CanMoveForward(count), self.Pieces)

    def Reset(self):
        for piece in self.Pieces:
            piece.SetPosition(BoardConsts.OUTSIDE_POSITION)