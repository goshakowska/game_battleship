from typing import List

"""
Global dictionary that contains names of particular ships in
the fleet (keys) and their lengths (values).
"""

naval_fleet = {
    "Carrier": 5,
    "Battleship": 4,
    "Destroyer": 3,
    "Submarine": 3,
    "Patrol boat": 2
}


class Ship:
    """
    Class Ship. Contains attributes:
    :param name: Ship's name
    :type name: str

    :param size: Ship's size
    :type size: int

    :param coordinates: Ship's coordinates. By default == None
    :type coordinates: List of tuples

    :param afloat: Condition - shows whether ship is afloat.
    :type afloat: Boolean expression. By default == True.
    """
    def __init__(self, name: str, size: int,
                 coordinates: List[tuple] = None, afloat: bool = True):
        """
        Creates instance of a ship.
        """
        self._name = name
        self._size = size
        if not coordinates:
            self._coordinates = []
        else:
            self._coordinates = coordinates
        self._afloat = afloat

    def name(self):
        """
        Method that return ship's name attribute.
        """
        return self._name

    def size(self):
        """
        Method that return ship's size attribute.
        """
        return self._size

    def coordinates(self):
        """
        Method that return ship's coordinates attribute.
        """
        return self._coordinates

    def ship_got_hit(self, hit: tuple):
        """
        Method that determines whether the ship has been hit by checking if
        the hit coordinate is in list of ship coordinates
        """
        if hit in self.coordinates():
            return True

    def is_it_afloat(self, board):
        """
        Method that determines whether the ship is afloat or not by
        checking status (what number it has) of each field that ship occupies.
        """
        not_afloat = 0
        for each_coordinate in self.coordinates():
            if board.ocean_grid()[each_coordinate] == 2:
                not_afloat += 1
        if not_afloat != len(self.coordinates()):
            return True
        else:
            return False

    def __str__(self):
        """
        Method that returns ship's name.
        """
        return self.name()
