from typing import List
import numpy as np
from random import choice, randint
import time


from game_board import GameBoard
from ship import Ship, naval_fleet
from game_interface import choose_ship_placement, input_coordinate
from game_interface import separator


class Player:
    """
    Class Player (Superclass of HumanPlayer, BotPlayer).
    Contains attributes:
    :param name: player's name
    :type name: str

    :param game_board: player's game board
    :type game_board: instance of a GameBoard class

    :param memory: player's memory
    :type memory: Numpy array filled with zeros
    (This parameter is needed in order to prevent player from choosing
    coordinate that has been already chosen before)
    """
    def __init__(self, name: str, game_board: GameBoard):
        """
        Creates instance of a player.
        """
        self._name = name
        self._game_board = game_board
        board_dimension = game_board.boards_edge()
        self._memory = np.zeros((board_dimension, board_dimension), dtype=int)

    def name(self):
        """
        Method that return player's name attribute.
        """
        return self._name

    def memory(self):
        """
        Method that return player's memory attribute.
        """
        return self._memory

    def game_board(self):
        """
        Method that return player's game_board attribute.
        """
        return self._game_board

    def __str__(self):
        """
        Returns name of a player (as a string).
        """
        return self.name()

    def remove_coordinate_from_memory(self, coordinate):
        """
        Method that removes given coordinate from player's memory -
        by marking given coordinate as 1 -by default
        a memory is an array of 0.
        This action in the future prevents player from choosing the coordinate,
        that has been already chosen before.
        """
        self.memory()[coordinate] = 1
        updated_memory = self.memory()
        return updated_memory

    def chosen_before_coordinate(self, coordinate):
        """
        Method that determines whether the coordinate has been chosen before -
        by checking which value in memory does the given coordinate has.
        If it is equal to 1 it means that the coordinate has been chosen,
        otherwise it hasn't been.
        """
        if self.memory()[coordinate] == 1:
            return True
        else:
            return False

    def has_lost(self):
        """
        Method that determines if the player has lost the gameplay
        by checking theirs fleet status.If each ship in a fleet is
        not afloat it means that the player lost,
        otherwise he hasn't lost yet.
        """
        afloat_ships = [each_ship.is_it_afloat(self.game_board())
                        for each_ship in self.game_board().fleet()]
        if not any(afloat_ships):
            return True
        else:
            return False

    def find_ship_tuples(self, starting_point: tuple, size: int,
                         forward: bool, axis: bool):
        """
        Helper method of ship_hull_placement_helper function.
        Creates list of coordinates (of tuples) that define
        the area that is occupied by ship in the board.
        """
        y_coordinate, x_coordinate = starting_point
        if axis:  # horizontal
            if forward:
                tuples_of_ship_position = [
                    (y_coordinate, x_coordinate + pos) for pos in range(size)]
            else:
                tuples_of_ship_position = [
                    (y_coordinate, x_coordinate - pos) for pos in range(size)]
        else:  # vertical
            if forward:
                tuples_of_ship_position = [
                    (y_coordinate + pos, x_coordinate) for pos in range(size)]
            else:
                tuples_of_ship_position = [
                    (y_coordinate - pos, x_coordinate) for pos in range(size)]
        return tuples_of_ship_position

    def ship_hull_placement_helper(self, coordinate: int,  subarray: np,
                                   directions: dict, ships_bow: tuple,
                                   ship_size: int):
        """
        Helper method of ship_hull_placement function.
        Checks possible direction in which the bow can be placed
        By creating each potential subarray where the ship would
        be placed and then checks whether the subarray exceeds
        game boards' edges and if they are big enough for
        the given ship.
        """
        first_subarray = subarray[:coordinate + 1]
        maybe_direction = list(directions)[0]
        board_axis = directions.get(maybe_direction)
        if len(first_subarray) >= ship_size:
            ship_position = subarray[coordinate + 1
                                     - ship_size: coordinate + 1]
            for position in ship_position:
                if position == 1:
                    directions.pop(maybe_direction)
                    break
            else:
                forward = False
                tuples_of_ship_position = self.find_ship_tuples(
                    ships_bow, ship_size, forward, board_axis)
                directions[maybe_direction] = tuples_of_ship_position
        else:
            directions.pop(maybe_direction)
        second_subarray = subarray[coordinate:]
        maybe_direction = list(directions)[-1]
        if len(second_subarray) >= ship_size:
            ship_position = subarray[coordinate: coordinate + ship_size]
            for position in ship_position:
                if position == 1:
                    directions.pop(maybe_direction)
                    break
            else:
                forward = True
                tuples_of_ship_position = self.find_ship_tuples(
                    ships_bow, ship_size, forward, board_axis)
                directions[maybe_direction] = tuples_of_ship_position
        else:
            directions.pop(maybe_direction)
        return directions

    def ship_hull_placement(self, ships_bow: tuple, ships_size: int):
        """
        Function that thanks to the provided ship's bow coordinates determines
        in which directions the rest of the ship (hull) can be allocated.

        Returns possible directions.
        """
        board = self.game_board()
        possible_positions = {}
        y_coordinate, x_coordinate = ships_bow
        hor_subarray = board.ocean_grid()[y_coordinate, :]
        hor_directions = {"left": True, "right": True}
        ver_subarray = board.ocean_grid()[:, x_coordinate]
        ver_directions = {"up": False, "down": False}
        # check possible horizontal positions
        hor_positions = self.ship_hull_placement_helper(
            x_coordinate, hor_subarray, hor_directions, ships_bow, ships_size)
        # check possible vertical positions
        ver_positions = self.ship_hull_placement_helper(
            y_coordinate, ver_subarray, ver_directions, ships_bow, ships_size)
        possible_positions = {**hor_positions, **ver_positions}
        return possible_positions


class HumanPlayer(Player):
    """
    Class HumanPlayer. Subclass of Player.
    Contains all the attributes inherited from Player.
    """

    def ship_bow_placement(self, coordinates: tuple):
        """
        This method determines whether the chosen for bow placement coordinate
        is occupied (by checking which value does the board field contain).
        """
        board = self.game_board()
        y_coordinate, x_coordinate = coordinates
        end_loop = 1
        while end_loop:
            if board.ocean_grid()[y_coordinate, x_coordinate] != 0:
                return
            else:
                return coordinates

    def arrange_ships_on_board(self, ship):
        players_board = self.game_board()
        ships_size = naval_fleet.get(ship)
        coordinates = input_coordinate(players_board)
        ships_bow_coordinates = self.ship_bow_placement(
            coordinates)
        if ships_bow_coordinates:
            possible_positions = self.ship_hull_placement(
                ships_bow_coordinates, ships_size)
            if len(possible_positions) != 0:
                ships_final_coordinates = choose_ship_placement(
                    possible_positions)
                new_ship = Ship(
                    ship, naval_fleet[ship], ships_final_coordinates)
                players_board.add_ship(new_ship)
                return False
        return True

    def attack_opponent(self, opponent: "BotPlayer"):
        """
        Method that defines player's attack. Returns parameters
        which define game status after the players attack.
        """
        damaged_ship = None
        shipwreck = None
        loser = None
        end_loop = True
        opponents_board = opponent.game_board()
        while end_loop:
            possible_hit = input_coordinate(opponents_board)
            was_chosen = self.chosen_before_coordinate(possible_hit)
            if not was_chosen:
                end_loop = False
        self.remove_coordinate_from_memory(possible_hit)
        opponents_board.set_new_board_status(possible_hit)
        for each_ship in opponents_board.fleet():
            ship_damage = each_ship.ship_got_hit(possible_hit)
            if ship_damage:
                damaged_ship = each_ship
                is_afloat = each_ship.is_it_afloat(opponents_board)
                if not is_afloat:
                    shipwreck = each_ship
                    is_loser = opponent.has_lost()
                    if is_loser:
                        loser = opponent
                        return opponent, damaged_ship, shipwreck, loser
                    return opponent, damaged_ship, shipwreck, loser
                return opponent, damaged_ship, shipwreck, loser
        else:
            return opponent, None, None, None

    def graphic_rep(self):
        """
        Method that graphically represents player's board.
        The method differs from the one that is implemented in BotPlayer class
        because it represents game board field's statuses differently.

        Unknown status of a field: "."
        Player's undiscovered by opponent ship placement field: "#"
        Missed shot (empty field): O
        Player's discovered by opponent ship placement field: "X".
        """
        board = self.game_board()
        print(f"{str(self)}'s Ocean Grid")
        time.sleep(0.5)
        separator()
        size = np.shape(board.ocean_grid())[0]
        for numbers in range(size+1):
            if numbers == 0:
                numbers = '  '
                print(numbers, end=' ')
            else:
                print(f' {chr(numbers+64)}', end=' ')
        separator()
        for numbers in range(size):
            time.sleep(0.2)
            print(f'{(numbers+1):2}', end=" ")
            for element in board.ocean_grid()[numbers, :-1]:
                if element == 0:
                    print(" .", end=" ")
                elif element == 1:
                    print(" #", end=" ")
                elif element == 2:
                    print(" X", end=" ")
                else:
                    print(" O", end=" ")
            last_element = board.ocean_grid()[numbers, -1]
            if last_element == 0:
                print(" .")
            elif last_element == 1:
                print(" #")
            elif last_element == 2:
                print(" X")
            else:
                print(" O")


class BotPlayer(Player):
    """
    Class HumanPlayer. Subclass of Player.
    Contains all the attributes inherited from Player.
    Contains its own attributes:
    :param hits_memory: Bot Player memory of hits.
    :param type: List of tuples (coordinates of ships that have been hit.)
    """
    def __init__(self, name: str, game_board: GameBoard,
                 hits_memory: List[tuple] = None):
        super().__init__(name, game_board)
        """
        Creates an instance of Bot Player.
        name by default is set to an Opponent.
        hits_memory by default is empty.
        """
        self._name = "Opponent"
        if not hits_memory:
            self._hits_memory = []
        board_dimension = game_board.boards_edge()
        self._memory = np.zeros((board_dimension, board_dimension), dtype=int)

    def hits_memory(self):
        """
        Method that return player's hits_memory attribute.
        """
        return self._hits_memory

    def add_to_hit_memory(self, new_hit):
        """
        Method that adds new hit to a hits_memory.
        It is crucial to do that in order for a Bot Player to play in
        an intelligent way.
        """
        updated_hit_memory = self.hits_memory().append(new_hit)
        return updated_hit_memory

    def remove_from_hits_memory(self, defeated_ship: Ship):  # if ship has sunk
        """
        Method that removes hits from hits_memory. Those hits are removed
        only when the opponent's ship has sunk and the bot does not need
        to search potential new hits around this area.
        """
        needless_coordinates = defeated_ship.coordinates()
        updated_hit_memory = []
        for coordinate in needless_coordinates:
            self.hits_memory().remove(coordinate)
        updated_hit_memory = self.hits_memory()
        return updated_hit_memory

    def choose_near_successful_hit(self, successful_hit):
        """
        Function that selects coordinates next to the board field, where
        the opponents ship has been shot and only one coordinate of
        the ship is known. Those coordinates are selected randomly,
        from the list of coordinates that are only one field to the
        left/right/up/down from the hit.
        """
        y_coordinate, x_coordinate = successful_hit
        possible_new_hit = [
            (y_coordinate, x_coordinate-1),
            (y_coordinate, x_coordinate+1),
            (y_coordinate-1, x_coordinate),
            (y_coordinate+1, x_coordinate)
        ]
        new_y_coordinate, new_x_coordinate = choice(possible_new_hit)
        return new_y_coordinate, new_x_coordinate

    def ineligible_coordinate(self, player: HumanPlayer,
                              y_coordinate, x_coordinate):
        """
        Function that determines whether the Bot Player can hit at the chosen
        coordinate. It checks value of opponents board's field. If it is marked
        as 2 or 3 it means that the coordinate has been chosen before.
        """
        players_board = player.game_board()
        if players_board.ocean_grid()[y_coordinate][x_coordinate] == 2 \
           or players_board.ocean_grid()[y_coordinate][x_coordinate] == 3:
            return True
        return False

    def choose_along_the_axis(self, player):
        """
        Function that makes Bot Player choose new hit intelligently, if more
        than one hit is stored in hit's memory. It determines which direction
        may the rest of the ship face (the ship that has been hit) and based
        on that chooses new coordinate.
        It checks which - X or Y coordinates are the same in a pair of tuples
        (coordinates) and then determines the axis on which ship lays.
        The function also ensures that the new chosen coordinates are inside
        the board and they are eligible to be a new hit
        (they haven't been chosen before).
        """
        # coordinates are on the same horizontal line
        if self.hits_memory()[0][0] == self.hits_memory()[1][0]:
            x_ordered_coordinates = sorted(self.hits_memory(),
                                           key=lambda coordinate: coordinate[1]
                                           )
            y_coordinate, left_end_x_coordinate = x_ordered_coordinates[0]
            y_coordinate, right_end_x_coordinate = x_ordered_coordinates[-1]
            possible_hits = [
                (y_coordinate, left_end_x_coordinate-1),
                (y_coordinate, right_end_x_coordinate+1)
            ]
        # coordinates are on the same vertical line
        elif self.hits_memory()[0][1] == self.hits_memory()[1][1]:
            y_ordered_coordinates = sorted(self.hits_memory())
            up_end_y_coordinate, x_coordinate = y_ordered_coordinates[0]
            down_end_y_coordinate, x_coordinate = y_ordered_coordinates[-1]
            possible_hits = [
                (up_end_y_coordinate-1, x_coordinate),
                (down_end_y_coordinate+1, x_coordinate)
            ]
        else:
            return False
        not_eligible = 0
        board = self.game_board()
        for (y_coordinate, x_coordinate) in possible_hits:
            if board.outside_board(y_coordinate, x_coordinate) \
                    or self.ineligible_coordinate(player,
                                                  y_coordinate, x_coordinate):
                not_eligible += 1
        if not_eligible != 2:
            new_hit = choice(possible_hits)
            return new_hit
        else:
            return False

    def based_on_hit_memory(self, player):
        """
        Function that determines the way the Bot Player is going to choose
        new hit when the hit memory is not empty. If it contains only one
        coordinate it chooses near a hit that is stored in hits memory
        (4 different directions possible). If there are more than one hit
        in hits memory it chooses an axis (based on those hits/tuples) on
        which a potential board can be allocated.
        """
        end_loop = True
        while end_loop:
            if len(self.hits_memory()) > 1:
                new_hit = self.choose_along_the_axis(player)
                if not new_hit:
                    successful_hit = choice(self.hits_memory())
                    new_hit = self.choose_near_successful_hit(successful_hit)
            else:
                successful_hit = self.hits_memory()[0]
                new_hit = self.choose_near_successful_hit(successful_hit)
            new_y_coordinate, new_x_coordinate = new_hit
            board = self.game_board()
            if not board.outside_board(new_y_coordinate, new_x_coordinate):
                end_loop = False
                new_hit = new_y_coordinate, new_x_coordinate
        return new_hit

    def attack_player(self, player: HumanPlayer):
        """
        Method that defines logic behind Bot Player's new move in game.
        Firstly it checks whether the hits memory is empty, chooses new hit
        (after coordinates validation (if they are inside game board etc.))
        and then updates Bot Players status (memories) and game status.

        """
        opponent = player
        damaged_ship = None
        shipwreck = None
        loser = None
        end_loop = True
        while end_loop:
            if len(self.hits_memory()) != 0:
                possible_hit = self.based_on_hit_memory(player)
            else:
                possible_hit = self.get_random_coordinate()
            was_chosen = self.chosen_before_coordinate(possible_hit)
            if not was_chosen:
                end_loop = False
        self.remove_coordinate_from_memory(possible_hit)
        players_board = player.game_board()
        players_board.set_new_board_status(possible_hit)
        for each_ship in players_board.fleet():
            ship_damage = each_ship.ship_got_hit(possible_hit)
            if ship_damage:
                damaged_ship = each_ship
                self.add_to_hit_memory(possible_hit)
                is_afloat = each_ship.is_it_afloat(players_board)
                if not is_afloat:
                    shipwreck = each_ship
                    self.remove_from_hits_memory(each_ship)
                    is_loser = player.has_lost()
                    if is_loser:
                        loser = player
                        return opponent, damaged_ship, shipwreck, loser
                    return opponent, damaged_ship, shipwreck, loser
                return opponent, damaged_ship, shipwreck, loser
        else:
            return opponent, None, None, None

    def graphic_rep(self):
        """
        Method that graphically represents player's board.
        The method differs from the one that is implemented in HumanPlayer
        class because it represents game board field's statuses differently.

        Unknown status of a field: "."
        Opponent's undiscovered ship placement field: "."
        Missed shot (empty field): O
        Opponents's discovered ship placement field: "X".
        """
        board = self.game_board()
        print(f"{str(self)}'s Ocean Grid")
        time.sleep(0.5)
        separator()
        size = np.shape(board.ocean_grid())[0]
        for numbers in range(size+1):
            if numbers == 0:
                numbers = '  '
                print(numbers, end=' ')
            else:
                print(f' {chr(numbers+64)}', end=' ')
        separator()
        for numbers in range(size):
            time.sleep(0.2)
            print(f'{(numbers+1):2}', end=" ")
            for element in board.ocean_grid()[numbers, :-1]:
                if element == 2:
                    print(" X", end=" ")
                elif element == 3:
                    print(" O", end=" ")
                else:
                    print(" .", end=" ")
            last_element = board.ocean_grid()[numbers, -1]
            if last_element == 2:
                print(" X")
            elif last_element == 3:
                print(" O")
            else:
                print(" .")

    def get_random_coordinate(self):
        """
        Method that chooses a new coordinate in a fully random manner.
        """
        opponent_board = self.game_board()
        selected_row = randint(0, opponent_board.boards_edge()-1)
        selected_column = randint(0, opponent_board.boards_edge()-1)
        coordinates = selected_row, selected_column
        return coordinates

    def opponent_bow_placement(self, coordinates: tuple):
        """
        Method that checks if a given coordinate of a potential
        bow placement is elligible ()
        """
        board = self.game_board()
        y_coordinate, x_coordinate = coordinates
        end_loop = 1
        while end_loop:
            if board.ocean_grid()[y_coordinate, x_coordinate] != 0:
                return
            else:
                return coordinates

    def opponent_chooses_ship_placement(self, possible_positions: dict):
        """
        Method that randomly chooses direction
        in which the rest of the bow should face.
        """
        chosen_direction = choice(list(possible_positions))
        ship_final_placement = possible_positions.get(chosen_direction)
        return ship_final_placement

    def opponent_arranges_ships_on_board(self):
        """
        Method that contains a "full" proccess of arranging ships on board
        that Bot Player needs to go through in order to place ships properly.
        """
        for key in naval_fleet:
            end_loop = 1
            while end_loop:
                ships_size = naval_fleet.get(key)
                opponents_board = self.game_board()
                coordinates = self.get_random_coordinate()
                ships_bow_coordinates = self.opponent_bow_placement(
                    coordinates)
                if ships_bow_coordinates:
                    possible_positions = self.ship_hull_placement(
                        ships_bow_coordinates, ships_size)
                    if len(possible_positions) != 0:
                        ships_final_coordinates = \
                            self.opponent_chooses_ship_placement(
                                possible_positions)
                        new_ship = Ship(
                            key, naval_fleet[key], ships_final_coordinates)
                        opponents_board.add_ship(new_ship)
                        end_loop = 0
