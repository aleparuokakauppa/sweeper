import sweeperlib
import constants
from mine_game import Game

def prompt_int(message: str, err_message: str) -> int:
    """
    Prompts the user for an integer.
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

def prompt_difficulty(game_instance: Game) -> int:
    """
    Prompts for game difficulty, returns the amount of mines for the game
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


def init_game():
    player_name = input("Player name: ")
    game_x_size = prompt_int("Give game size X: ", "Not a valid size")
    game_y_size = prompt_int("Give game size Y: ", "Not a valid size")

    game = Game((game_x_size, game_y_size))
    game.player_name = player_name

    n_mines = prompt_difficulty(game)
    game.init_tile_contents(n_mines=n_mines)

    game.print_scores()

    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(game.board_size_px[0], game.board_size_px[1]+128, (192, 192, 192, 255))

    # Set handlers
    sweeperlib.set_draw_handler(game.draw_field)
    sweeperlib.set_mouse_handler(game.handle_mouse)
    sweeperlib.set_interval_handler(game.draw_timer, 1)

    # Start the main-game
    sweeperlib.start()

if __name__ == "__main__":
    init_game()
