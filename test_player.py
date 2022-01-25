from game_board import GameBoard
from players import BotPlayer, HumanPlayer, Player
from ship import Ship


def test_init_player():
    board = GameBoard(8)
    player = Player("Gosia", board)
    assert player._name == "Gosia"
    assert player._game_board == board


def test_players_getters():
    board = GameBoard(8)
    player = Player("Gosia", board)
    assert player.name() == "Gosia"
    assert player.game_board() == board


def test_players_str():
    board = GameBoard(8)
    player = Player("Gosia", board)
    assert str(player) == "Gosia"


def test_remove_coordinate_from_memory():
    board = GameBoard(8)
    player = Player("Gosia", board)
    coordinate = (0, 0)
    new_memory = player.remove_coordinate_from_memory(coordinate)
    assert new_memory[coordinate] == 1


def test_chosen_before_coordinate():
    board = GameBoard(8)
    player = Player("Gosia", board)
    coordinate = (0, 0)
    player.remove_coordinate_from_memory(coordinate)
    new_coordinate = (0, 0)
    chosen = player.chosen_before_coordinate(new_coordinate)
    assert chosen is True


def test_not_chosen_before_coordinate():
    board = GameBoard(8)
    player = Player("Gosia", board)
    coordinate = (0, 0)
    player.remove_coordinate_from_memory(coordinate)
    new_coordinate = (0, 1)
    chosen = player.chosen_before_coordinate(new_coordinate)
    assert chosen is False


def test_hasnt_lost():
    ship = Ship("Patrol boat", 2, [(0, 1), (1, 1)])
    ships = [ship]
    board = GameBoard(8, ships)
    player = Player("Gosia", board)
    hit1 = (0, 1)
    hit2 = (1, 2)
    board.set_new_board_status(hit1)
    board.set_new_board_status(hit2)
    ship.is_it_afloat(board)
    hasnt_lost = player.has_lost()
    assert hasnt_lost is False


def test_has_lost():
    ship = Ship("Patrol boat", 2, [(0, 1), (1, 1)])
    ships = [ship]
    board = GameBoard(8, ships)
    player = Player("Gosia", board)
    hit1 = (0, 1)
    hit2 = (1, 1)
    board.set_new_board_status(hit1)
    board.set_new_board_status(hit2)
    ship.is_it_afloat(board)
    has_lost = player.has_lost()
    assert has_lost is True


def test_ship_bow_placement_unoccupied():
    ship = Ship("Patrol boat", 2, [(0, 0), (0, 1)])
    board = GameBoard(8)
    board.add_ship(ship)
    player = HumanPlayer("Gosia", board)
    coordinates = (2, 2)
    result = player.ship_bow_placement(coordinates)
    assert result is not None


def test_ship_bow_placement_occupied():
    ship = Ship("Patrol boat", 2, [(0, 0), (0, 1)])
    board = GameBoard(8)
    board.add_ship(ship)
    player = HumanPlayer("Gosia", board)
    coordinates = (0, 0)
    result = player.ship_bow_placement(coordinates)
    assert result is None


def test_init_bot_player():
    board = GameBoard(8)
    opponent = BotPlayer("Przeciwnik", board)
    assert opponent.name() == "Opponent"
    assert opponent.hits_memory() == []


def test_add_to_hit_memory():
    board = GameBoard(8)
    opponent = BotPlayer("Przeciwnik", board)
    hit = (0, 0)
    opponent.add_to_hit_memory(hit)
    assert len(opponent.hits_memory()) == 1


def test_remove_from_hits_memory_not_empty():
    ship = Ship("Patrol boat", 2, [(0, 1), (1, 1)])
    ships = [ship]
    board = GameBoard(8, ships)
    opponent = BotPlayer("Przeciwnik", board)
    hit1 = (0, 0)
    hit2 = (0, 1)
    hit3 = (1, 1)
    opponent.add_to_hit_memory(hit1)
    opponent.add_to_hit_memory(hit2)
    opponent.add_to_hit_memory(hit3)
    opponent.remove_from_hits_memory(ship)
    assert len(opponent.hits_memory()) == 1


def test_remove_from_hits_memory_empty():
    humans_ship = Ship("Patrol boat", 2, [(0, 1), (1, 1)])
    board = GameBoard(8)
    opponent = BotPlayer("Przeciwnik", board)
    hit2 = (0, 1)
    hit3 = (1, 1)
    opponent.add_to_hit_memory(hit2)
    opponent.add_to_hit_memory(hit3)
    opponent.remove_from_hits_memory(humans_ship)
    assert len(opponent.hits_memory()) == 0
