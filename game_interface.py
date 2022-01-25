import time
from ship import naval_fleet

"""
This file contains functions that are responsible for printiong out
the messages to the player and that are proccessing player's input.
"""


def decode_input(input_position: str, board):
    """
    Function that decodes player's input into a specific coordinate
    in a numpy array.
    """
    capitalized_letter = input_position[0].upper()
    x_coordinate = ord(capitalized_letter) - 65
    y_coordinate = int(input_position[1:]) - 1
    check_coordinates = board.outside_board(y_coordinate, x_coordinate)
    if check_coordinates:
        return
    return y_coordinate, x_coordinate


def input_coordinate(board):
    """
    Function that communicates with player while they provide an input.
    Proccesses each input and returns suitable message (which depends
    whether the player's input is valid or not)
    """
    end_loop = 1
    while end_loop:
        time.sleep(0.5)
        players_input = input("Please enter the coordinates: ")
        if players_input is None or len(players_input) not in range(2, 3+1):
            print("Improper coordinate's length. Try again.")
        elif ord(players_input[0]) not in range(65, 90+1) and \
                ord(players_input[0]) not in range(97, 122+1):
            print("First coordinate should be a letter. Try again.")
        else:
            for each_number in players_input[1:]:
                if ord(each_number) not in range(48, 57+1):
                    print("Second coordinate should be an integer. Try again.")
                    break
            else:
                coordinates = decode_input(players_input, board)
                if coordinates is None:
                    print("Wrong values. Try again.", end=' ')
                else:
                    end_loop = 0
    return coordinates


def game_description():
    """
    Provides game description with basic rules of game of Warships.
    """
    print("You and Your opponent will face each other in a warship battle!")
    print("Your goal is to destroy Your opponent's fleet.")
    print("To do that, each round You will provide coordinates-")
    print("the ones, where You think the ship may be.")


def separator():
    """
    Blank line separator
    """
    print()


def new_turn_separator():
    """
    Separator that is used between game rounds.
    """
    for _ in range(80):
        print("*", end="")
        time.sleep(0.05)
    separator()


def choose_ship_placement(possible_positions: dict):
    """
    Function that informs player of possible directions which
    the rest of the ship can face.
    """
    letter_meanings = {"u": "up", "d": "down", "l": "left", "r": "right"}
    keys = possible_positions.keys()
    possible_letter_meanings = {}
    for letter in letter_meanings:
        if letter_meanings[letter] in possible_positions:
            possible_letter_meanings[letter] = letter_meanings[letter]
    end_loop = 1
    time.sleep(0.5)
    separator()
    print("Please choose the direction which rest of the ship should face.")
    time.sleep(0.5)
    print('To do that, write shortcuts of directions:')
    print('"u" for up, "d" for down, "l" for left and "r" for right.')
    time.sleep(2)
    separator()
    while end_loop:
        print("Your ship can be placed in this directions:")
        time.sleep(0.5)
        print(*keys, sep=', ')
        separator()
        time.sleep(0.5)
        players_input = input(
            "Rest of the ship will face this direction: ")
        time.sleep(1)
        if players_input in possible_letter_meanings:
            print("Success! Your ship is now placed in Your Ocean Grid")
            chosen_direction = letter_meanings.get(players_input)
            ship_final_placement = possible_positions.get(chosen_direction)
            end_loop = 0
        else:
            print("Ups! You entered the wrong letter. Try again.")
            separator()
    return ship_final_placement


def input_arrange_ships_on_board(human_player):
    """
    Function that through messages navigates player
    while they choose ship placement on their board.
    """
    time.sleep(0.5)
    print("Perfect! Now let's choose your ships positions!")
    separator()
    time.sleep(2)
    print("Hint: To place your ship first You will need to choose location")
    print("for your ship's bow (the front part of the ship).")
    time.sleep(4)
    print("If the position is correct You will be able to choose")
    print("which direction should the rest of the ship face.")
    time.sleep(54)
    print("The directions provided will be the ones")
    print("for which Your ship placement is possible.")
    time.sleep(2)
    separator()
    for ship in naval_fleet:
        separator()
        print(f"Let's place {ship}:")
        time.sleep(1)
        separator()
        print("The position of ship's bow should be given as in ")
        print("a following example: 'A5', 'F3' etc.")
        time.sleep(1)
        separator()
        human_player.graphic_rep()
        separator()
        end_loop = True
        while end_loop:
            end_loop = human_player.arrange_ships_on_board(ship)
            if end_loop:
                print(
                    "You cannot place the ship in this area.")
                print("Try a different one.")
    human_player.graphic_rep()
    print("We are set to start the game!")


def before_players_attack(player, opponent):
    """
    Function that prints message just before an attack.
    """
    new_turn_separator()
    print(f"It's {str(player)}'s turn!")
    time.sleep(1)
    separator()
    opponent.graphic_rep()
    separator()


def result_of_players_attack(opponent, damaged_ship, shipwreck, loser):
    """
    Function that based on the attacks outcome provides a suitable message.
    """
    opponent.graphic_rep()
    if damaged_ship:
        time.sleep(1)
        separator()
        time.sleep(0.5)
        print(f"{str(opponent)}'s ship has been hit!")
        separator()
        if shipwreck:
            time.sleep(1)
            print("You successfully sunk opponent's ship!")
            separator()
            if loser:
                time.sleep(1)
                print(
                    "Hurray! You can proclaim Yourself as a Lord of the Seas!")
                print("You won!")
                return False
    else:
        time.sleep(1)
        print("You missed! Better luck next time!")
        separator()
    return True


def before_enemys_attack(opponent):
    """
    Function that prints message just before an attack.
    """
    separator()
    new_turn_separator()
    print(f"{str(opponent)} prepare Yourself for opponent's attack!")
    separator()


def result_of_enemys_attack(opponent, damaged_ship, shipwreck, loser):
    """
    Function that based on the attacks outcome provides a suitable message.
    """
    if damaged_ship:
        time.sleep(1)
        opponent.graphic_rep()
        separator()
        time.sleep(1)
        print(f"The opponent has hit your {str(damaged_ship)}!")
        separator()
        if shipwreck:
            time.sleep(0.5)
            print(
                f"Houston, we have a problem. Your {str(shipwreck)} has sunk!")
            separator()
            if loser:
                time.sleep(1)
                print(
                    "Oh no! It turns out that... Your opponent defeated You.")
                time.sleep(1)
                print("It's time for Your revenge!")
                return False
    else:
        time.sleep(2)
        print("Phew! Lucky You! Your opponent has missed!")
        separator()
        time.sleep(1)
        opponent.graphic_rep()
        separator()
    return True
