from game_board import GameBoard
from ship import Ship


def test_init_ship_default():
    new_ship = Ship("Carrier", 5)
    assert new_ship._name == "Carrier"
    assert new_ship.name() == "Carrier"
    assert new_ship._size == 5
    assert new_ship.size() == 5
    assert new_ship._coordinates == []
    assert new_ship._afloat is True


def test_ship_got_hit():
    ship1 = Ship("Patrol boat", 2, [(0, 2), (0, 1)])
    ship2 = Ship("Patrol boat", 2, [(0, 0), (0, 1)])
    possible_hit = (0, 0)
    assert ship1.ship_got_hit(possible_hit) is None
    assert ship2.ship_got_hit(possible_hit) is True


def test_ship_str():
    ship1 = Ship("Patrol boat", 2)
    ship2 = Ship("", 2)
    assert str(ship1) == "Patrol boat"
    assert str(ship2) == ""


def test_is_it_afloat_true():
    ship = Ship("Patrol boat", 2, [(0, 1), (1, 1)])
    board = GameBoard(3, [ship])
    hit1 = (0, 1)
    board.set_new_board_status(hit1)
    assert ship.is_it_afloat(board) is True


def test_is_it_afloat_false():
    ship = Ship("Patrol boat", 2, [(0, 1), (1, 1)])
    board = GameBoard(3, [ship])
    hit1 = (0, 1)
    hit2 = (1, 1)
    board.set_new_board_status(hit1)
    board.set_new_board_status(hit2)
    assert ship.is_it_afloat(board) is False


def test_is_it_afloat_missed_hit():
    ship = Ship("Patrol boat", 2, [(0, 1), (1, 1)])
    board = GameBoard(3, [ship])
    hit1 = (0, 2)
    board.set_new_board_status(hit1)
    assert ship.is_it_afloat(board) is True
