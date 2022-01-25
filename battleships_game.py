import time
from players import HumanPlayer, BotPlayer
from game_board import GameBoard
from game_interface import before_enemys_attack, before_players_attack
from game_interface import game_description, input_arrange_ships_on_board
from game_interface import result_of_enemys_attack, result_of_players_attack
from game_interface import separator


def main():
    """
    Main function of Battleships.
    Contains whole gameplay, including initialization of
    human player, bot player and their's boards.
    """
    board_game, player = initialize_game()
    input_arrange_ships_on_board(player)
    opponents_board_size = board_game.boards_edge()
    opponents_board_game = GameBoard(opponents_board_size)
    opponent = BotPlayer("Your Opponent", opponents_board_game)
    opponent.opponent_arranges_ships_on_board()
    print(opponent.game_board().ocean_grid())
    game_description()
    winner = gameplay(player, opponent)
    print(f'The winner is {str(winner)}.')


def initialize_game():
    """
    Function that initializes Human player and their game board.
    Processes player's input - gets player's name (it cannot be empty)
    and desired game board's size which impacts game level.
    Accepted game board's size's were set between 8*8 and 16*16.
    Checks if player's input is correct.
    """
    print("Welcome to the game of Warships!")
    time.sleep(1)
    print("Before you face your opponent please tell us what is your name.")
    time.sleep(1)
    players_name = input("Enter your name: ")
    while not players_name:
        players_name = input("Ups! Try again - enter your name: ")
    separator()
    print("Select your game level - choose the desired Ocean Grid's dimension")
    print("from 8 to 16 (10 is a standard grid's size for the game).")
    time.sleep(4)
    end_loop = 1
    while end_loop:
        time.sleep(0.5)
        try:
            boards_dimensions = input("Enter length of board's edge: ")
            int_boards_dimensions = int(boards_dimensions)
            if int_boards_dimensions in range(8, 16+1):
                end_loop = 0
            else:
                print("Ups! Try again.", end=" ")
        except ValueError:
            print("Ups! Try again.", end=" ")
    game_board = GameBoard(int_boards_dimensions)
    human_player = HumanPlayer(players_name, game_board)
    return game_board, human_player


def gameplay(player: HumanPlayer, opponent: BotPlayer):
    """
    This function covers whole Battleship's gameplay.
    After each round the conditions, which determine
    round's outcome are checked. Thanks to
    "result_of ... attack" function
    an appropriate message is shown to the player.
    """
    end_loop = True
    while end_loop:
        before_players_attack(player, opponent)
        players_opponent, damaged_ship1, shipwreck1, loser1 \
            = player.attack_opponent(opponent)
        players_not_final_move \
            = result_of_players_attack(players_opponent,
                                       damaged_ship1, shipwreck1,
                                       loser1)
        if players_not_final_move:
            before_enemys_attack(player)
            bot_opponent, damaged_ship2, shipwreck2, loser2 = \
                opponent.attack_player(player)
            opponent_not_final_move = result_of_enemys_attack(
                bot_opponent, damaged_ship2, shipwreck2, loser2)
            if not opponent_not_final_move:
                winner = opponent
                end_loop = False
        else:
            winner = player
            end_loop = False
    return winner


if __name__ == "__main__":
    main()
