import sweeperlib
from mine_game import Game
from scoreboard_logging import ScoreboardLogger

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
    user_n_mines = prompt_input("How many mines?: ", "Not a valid number")
    

    game = Game((game_x_size, game_y_size))
    game.init_tile_contents(n_mines=user_n_mines)


    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(game.board_size_px[0], game.board_size_px[1]+128, (192, 192, 192, 255))

    # Set handlers
    sweeperlib.set_draw_handler(game.draw_field)
    sweeperlib.set_mouse_handler(game.handle_mouse)
    sweeperlib.set_interval_handler(game.draw_timer, 1)

    # Start the main-game
    sweeperlib.start()

if __name__ == "__main__":
    dt = ScoreboardLogger()
    dt.write_scoreboard_data(15, "Easy", "Alepa")
    #data = dt.get_scoreboard_data()
    #for value in data:
        #print(value)
    init_game()
