from typing import List
import numpy as np
from ship import Ship


class GameBoard:
    """
    Class GameBoard.
    Contains attributes:
    :param boards_edge: length of Game Board's edge.
    :type boards_edge: int

    :param fleet:  Fleet on Game Board of a player.
    :type fleet: List of Ships
    """

    def __init__(self, boards_edge: int, fleet: List["Ship"] = None):
        """
        Creates instance of a game board.
        """
        self._boards_edge = boards_edge
        self._ocean_grid = np.zeros((boards_edge, boards_edge), dtype=int)
        if not fleet:
            self._fleet = []
        else:
            self._fleet = fleet

    def boards_edge(self):
        """
        Method that return game board's boards_edge attribute.
        """
        return self._boards_edge

    def ocean_grid(self):
        """
        Method that return game board's ocean_grid attribute.
        """
        return self._ocean_grid

    def fleet(self):
        """
        Method that return game boards's fleet attribute.
        """
        return self._fleet

    def add_ship(self, new_ship: "Ship"):
        """
        Method that adds a new ship to a list of ships on game board.
        """
        self.fleet().append(new_ship)
        for each_ship_coordinate in new_ship.coordinates():
            self.ocean_grid()[each_ship_coordinate] = 1
        new_ocean_grid = self.ocean_grid()
        return new_ocean_grid

    def set_new_board_status(self, new_hit: tuple):
        """
        Method that sets new board status. It is performed after player's move.
        It's field value is changed accordingly to the result of a hit
        (whether it has been a missed shot or a successful hit).
        """
        for each_ship in self.fleet():
            if new_hit in each_ship.coordinates():
                self.ocean_grid()[new_hit] = 2  # hit
                break
        else:
            self.ocean_grid()[new_hit] = 3  # miss
        new_board_status = self.ocean_grid()
        return new_board_status

    def outside_board(self, y_coordinate, x_coordinate):
        """
        Method that checks whether the coordinate is within a board.
        """
        if x_coordinate not in range(self.boards_edge()) \
                or y_coordinate not in range(self.boards_edge()):
            return True
        return False
