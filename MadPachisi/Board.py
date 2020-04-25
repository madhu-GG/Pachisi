from MadPachisi.Player import PlayerCount


class Board(object):
    def __init__(self, num_players: int):
        """

        :type num_players: int
        """
        if not (isinstance(num_players, int)) or (num_players < PlayerCount.MINIMUM or
                                                  num_players > PlayerCount.MAXIMUM):
            raise RuntimeError('Number of players expected between {} and {}, received = {}'
                               .format(PlayerCount.MINIMUM, PlayerCount.MAXIMUM, num_players))

        self.NumPlayers = num_players
        self.Board = []


if __name__ == "__main__":
    try:
        mboard = Board(2)
        print("Players == {}", mboard.NumPlayers)
    except RuntimeError as e:
        print(e)
    else:
        print("Initialized board successfully!")
