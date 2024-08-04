"""
Helper functions for getting valid user inputs
"""
from app.game import game_constants

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

    while True:
        user_input = input(message)
        try:
            user_int = int(user_input)
            if user_int < prompt_min:
                raise ValueError
            if user_int > prompt_max:
                raise ValueError
            return user_int
        except ValueError:
            print(err_message)
            print(f"Minimum value: {prompt_min} Maximum value: {prompt_max}")

def prompt_difficulty() -> int:
    """
    Prompts for game difficulty, returns difficulty as defined in `constants.py`
    Keeps trying until user gives valid input

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
                return game_constants.DIFFICULTY_EASY
            case "m":
                return game_constants.DIFFICULTY_MEDIUM
            case "h":
                return game_constants.DIFFICULTY_HARD
            case "c":
                return game_constants.DIFFICULTY_CUSTOM
            case _:
                print("\nNot a valid difficulty")

def get_game_properties() -> dict:
    """
    Prompts user for game properties

    returns a dict of properties with the following keys:
    - board-size: tuple[int, int]
    - board-size-px: tuple[int, int]
    - mine-count: int
    - player-name: str
    - difficulty: int
    """
    print("\n-- New Game --")
    player_name = input("  Player name: ")

    game_x_size = prompt_int(
                        "  Give game size X: ",
                        "Not a valid size",
                        game_constants.GAME_BOARD_MIN_X_SIZE,
                        game_constants.GAME_BOARD_MAX_X_SIZE
                    )

    game_y_size = prompt_int(
                        "  Give game size Y: ",
                        "Not a valid size",
                        game_constants.GAME_BOARD_MIN_Y_SIZE,
                        game_constants.GAME_BOARD_MAX_Y_SIZE
                    )

    total_tiles = game_x_size * game_y_size

    difficulty = prompt_difficulty()
    mine_count = 0
    if difficulty == game_constants.DIFFICULTY_CUSTOM:
        mine_count = prompt_int("How many mines?: ",
                                "\nNot a valid value\n",
                                1, game_x_size * game_y_size - 1)
    else:
        match difficulty:
            case game_constants.DIFFICULTY_EASY:
                mine_count = round(total_tiles * 0.10)
            case game_constants.DIFFICULTY_MEDIUM:
                mine_count = round(total_tiles * 0.20)
            case game_constants.DIFFICULTY_HARD:
                mine_count = round(total_tiles * 0.30)

    return {
        "board-size": (game_x_size, game_y_size),
        "board-size-px": (game_x_size * game_constants.TILE_SPRITE_SIZE_PX,
                          game_y_size * game_constants.TILE_SPRITE_SIZE_PX),
        "mine-count": mine_count,
        "player-name": player_name,
        "difficulty": difficulty
    }
