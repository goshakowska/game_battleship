from game_board import GameBoard
from ship import Ship


def test_init_gameboard_default():
    board = GameBoard(8)
    assert board.boards_edge() == 8
    assert board.fleet() == []


def test_init_gameboard_with_ships():
    ship1 = Ship("Carrier", 5)
    ship2 = Ship("Patrol boat", 2)
    ships = [ship1, ship2]
    board = GameBoard(8, ships)
    assert board.boards_edge() == 8
    assert board.fleet() == ships


def test_add_ship():
    coord1 = (0, 0)
    coord2 = (1, 0)
    coordinates = [coord1, coord2]
    ship1 = Ship("Patrol boat", 2, coordinates)
    board = GameBoard(8)
    board.add_ship(ship1)
    assert board.ocean_grid()[coord1] == 1
    assert board.ocean_grid()[coord2] == 1
    assert len(board.fleet()) == 1


def test_set_new_board_status_hit():
    coord1 = (0, 0)
    coord2 = (1, 0)
    coordinates = [coord1, coord2]
    ship1 = Ship("Patrol boat", 2, coordinates)
    board = GameBoard(8)
    board.add_ship(ship1)
    hit = (0, 0)
    board.set_new_board_status(hit)
    assert board.ocean_grid()[hit] == 2


def test_set_new_board_status_miss():
    coord1 = (0, 0)
    coord2 = (1, 0)
    coordinates = [coord1, coord2]
    ship1 = Ship("Patrol boat", 2, coordinates)
    board = GameBoard(8)
    board.add_ship(ship1)
    hit = (0, 2)
    board.set_new_board_status(hit)
    assert board.ocean_grid()[hit] == 3
