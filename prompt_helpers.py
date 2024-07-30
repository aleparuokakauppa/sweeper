import constants
from game_logic import Game

def prompt_int(message: str, err_message: str) -> int:
    """
    Prompts the user for an integer.
    If an invalid input is given, an error message is shown using
    the error message parameter. A valid input is returned as an
    integer.

    Can raise a KeyboardInterrupt
    """
    user_input: str = ""
    user_int: int = 0
    while True:
        user_input = input(message)
        try:
            user_int = int(user_input)
            if user_int > 100:
                raise ValueError
            return user_int
        except ValueError:
            print(err_message)

def prompt_difficulty(game_instance: Game) -> int:
    """
    Prompts for game difficulty, returns the amount of mines for the game

    Can raise a KeyboardInterrupt
    """
    user_input: str = ""
    mine_multiplier: float = 0.0
    while True:
        user_input = input("Select game difficulty (easy, medium, hard, custom): ")
        match user_input:
            case "easy":
                mine_multiplier = 0.5
                game_instance.difficulty = constants.DIFFICULTY_EASY
                break
            case "medium":
                mine_multiplier = 1.0
                game_instance.difficulty = constants.DIFFICULTY_MEDIUM
                break
            case "hard":
                mine_multiplier = 1.5
                game_instance.difficulty = constants.DIFFICULTY_HARD
                break
            case "custom":
                game_instance.difficulty = constants.DIFFICULTY_CUSTOM
                return prompt_int("How many mines?: ", "Not a valid number")
            case _:
                print("Not a valid difficulty")
    return round((game_instance.board_size[0] + game_instance.board_size[1]) * mine_multiplier)
