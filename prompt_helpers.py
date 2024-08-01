"""
Helper functions for getting valid user inputs
"""
import constants
from game_logic import GameHandler

def prompt_int(message: str, err_message: str, prompt_min: int, prompt_max: int) -> int:
    """
    Prompts the user for an integer.
    If an invalid input is given, an error message is shown using
    the error message parameter. A valid input is returned as an
    integer.

    Can raise a KeyboardInterrupt

    :params str message: Message to prompt the user
    :params str err_message: Message to error user in case of invalid input
    :params int prompt_min: Minimum value to get from user (inclusive)
    :params int prompt_max: Maximum value to get from user (inclusive)
    """
    prompt_min = min(prompt_min, prompt_max)

    user_input: str = ""
    user_int: int = 0
    while True:
        user_input = input(message)
        try:
            user_int = int(user_input)
            if user_int < prompt_min or user_int > prompt_max:
                raise ValueError
            return user_int
        except ValueError:
            print(err_message)
            print(f"Minimum value: {prompt_min} Maximum value: {prompt_max}")

def prompt_difficulty() -> int:
    """
    Prompts for game difficulty, returns difficulty as defined in `constants.py`

    Can raise a KeyboardInterrupt
    """
    while True:
        print()
        print("-- Select game difficulty --")
        print("  Easy -> e")
        print("  Medium -> m")
        print("  Hard -> h")
        print("  Custom -> c")

        match input("> ").lower():
            case "e":
                return constants.DIFFICULTY_EASY
            case "m":
                return constants.DIFFICULTY_MEDIUM
            case "h":
                return constants.DIFFICULTY_HARD
            case "c":
                return constants.DIFFICULTY_CUSTOM
            case _:
                print("\nNot a valid difficulty")

def get_game_properties() -> dict:
    """
    Gets user input for game properties 
    """
    print("\n-- New Game --")
    player_name = input("  Player name: ")

    game_x_size = prompt_int(
                                "  Give game size X: ",
                                "Not a valid size",
                                8,
                                30)
    game_y_size = prompt_int(
                                "  Give game size Y: ",
                                "Not a valid size",
                                8,
                                30)

    difficulty = prompt_difficulty()
    mine_count = 0
    if difficulty == constants.DIFFICULTY_CUSTOM:
        while True:
            mine_count = prompt_int("How many mines?: ", "\nNot a valid value\n", 1, game_x_size * game_y_size - 1)
    else:
        match difficulty:
            case constants.DIFFICULTY_EASY:
                mine_count = 
            case constants.DIFFICULTY_MEDIUM:
                pass
            case constants.DIFFICULTY_HARD:
                pass
