import sweeperlib
from mine_game import Game

def prompt_input(message: str, err_message: str) -> int:
    """
    Prompts the user for an integer using the prompt parameter.
    If an invalid input is given, an error message is shown using
    the error message parameter. A valid input is returned as an
    integer.
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


def prompt_difficulty(game_size: tuple[(int, int)]) -> int:
    """
    Prompts for game difficulty, returns the amount of mines for the game
    """
    user_input: str = ""
    mine_multiplier: float = 0.0
    while True:
        user_input = input("Select game difficulty (easy, medium, hard): ")
        match user_input:
            case "easy":
                mine_multiplier = 0.6
                break
            case "medium":
                mine_multiplier = 1.0
                break
            case "hard":
                mine_multiplier = 1.4
                break
            case _:
                print("Not a valid difficulty")
    return round((game_size[0] + game_size[1]) * mine_multiplier)


def init_game():
    game_x_size = prompt_input("Give game size X: ", "Not a valid size")
    game_y_size = prompt_input("Give game size Y: ", "Not a valid size")
    user_n_mines = prompt_difficulty((game_x_size, game_y_size))

    game = Game((game_x_size, game_y_size))
    game.init_tile_contents(n_mines=user_n_mines)


    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(*game.board_size_px)

    # Set handlers
    sweeperlib.set_draw_handler(game.draw_field)
    sweeperlib.set_mouse_handler(game.handle_mouse)

    # Start the main-game
    sweeperlib.start()

def main_menu() -> str:
    """
    Main menu 
    """
    return ""

if __name__ == "__main__":
    main_menu()
    init_game()
