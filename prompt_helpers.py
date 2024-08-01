"""
Helper functions for getting valid user inputs
"""
import constants
from game_logic import Game

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

def prompt_difficulty(game_instance: Game) -> int:
    """
    Prompts for game difficulty, returns the amount of mines for the game

    Can raise a KeyboardInterrupt
    """
    mine_multiplier: float = 0.0
    while True:
        print()
        print("-- Select game difficulty --")
        print("  Easy -> e")
        print("  Medium -> m")
        print("  Hard -> h")
        print("  Custom -> c")

        match input("> ").lower():
            case "e":
                mine_multiplier = 0.5
                game_instance.difficulty = constants.DIFFICULTY_EASY
                break
            case "m":
                mine_multiplier = 1.0
                game_instance.difficulty = constants.DIFFICULTY_MEDIUM
                break
            case "h":
                mine_multiplier = 1.5
                game_instance.difficulty = constants.DIFFICULTY_HARD
                break
            case "c":
                while True:
                    game_instance.difficulty = constants.DIFFICULTY_CUSTOM
                    return prompt_int("How many mines?: ",
                                      "\nNot a valid value\n",
                                      1,
                                      game_instance.board_size[0] * game_instance.board_size[1] - 1)
            case _:
                print("\nNot a valid difficulty")
    return round((game_instance.board_size[0] + game_instance.board_size[1]) * mine_multiplier)
