import sweeperlib
import prompt_helpers
from game_logic import Game
from scoreboard_logging import ScoreboardLogger

def main_menu():
    """
    Main menu loop for the UI

    Launches the user-selected action
    """
    while True:
        print("===  Minesweeper  ===")
        print("Type an action and press enter")
        print("  Play a new game -> n")
        print("  View scoreboard -> s")
        print("  Quit game       -> q")
        match input("> ").lower():
            case 'n':
                init_game()
            case 's':
                ScoreboardLogger().print_scores()
            case 'q':
                print("Goodbye...")
                break
            case _:
                print("Not a valid action. Try again.")

def init_game():
    player_name = input("Player name: ")
    game_x_size = prompt_helpers.prompt_int("Give game size X: ", "Not a valid size")
    game_y_size = prompt_helpers.prompt_int("Give game size Y: ", "Not a valid size")

    game_object = Game((game_x_size, game_y_size))

    game_object.player_name = player_name
    game_object.init_tile_contents(n_mines=prompt_helpers.prompt_difficulty(game_object))

    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(game_object.board_size_px[0],
                             game_object.board_size_px[1]+128,
                             (192, 192, 192, 255),
                             title="Mine Sweeper")

    # Set pyglet handlers
    sweeperlib.set_draw_handler(game_object.draw_field)
    sweeperlib.set_mouse_handler(game_object.handle_mouse)
    sweeperlib.set_interval_handler(game_object.draw_timer, 1)

    sweeperlib.start()

if __name__ == "__main__":
    try:
        main_menu()
    # Catch ^C
    except KeyboardInterrupt:
        print("\nExiting!")
    # Catch ^D
    except EOFError:
        print("\nExiting!")
