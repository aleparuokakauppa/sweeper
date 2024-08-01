"""
Main program script

The user interface and the game is started from here
"""
import sweeperlib
import prompt_helpers
from game_logic import Game
import scoreboard_logging

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
                start_game()
            case 's':
                scoreboard_logging.print_scores()
            case 'q':
                print("Goodbye...")
                break
            case _:
                print("\nNot a valid action. Try again.\n")

def start_game():
    """
    Gets user input for game properties and
    starts the game.
    """
    print("\n-- New Game --")
    player_name = input("  Player name: ")

    game_x_size = prompt_helpers.prompt_int(
                                "  Give game size X: ",
                                "Not a valid size",
                                8,
                                30)
    game_y_size = prompt_helpers.prompt_int(
                                "  Give game size Y: ",
                                "Not a valid size",
                                8,
                                30)

    game_object = Game((game_x_size, game_y_size))

    game_object.player_name = player_name
    game_object.init_tile_contents(n_mines=prompt_helpers.prompt_difficulty(game_object))

    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(game_object.board_size_px[0],
                             game_object.board_size_px[1]+128,
                             (192, 192, 192, 255),
                             title="Mine Sweeper")

    # Set pyglet handlers
    sweeperlib.set_mouse_handler(game_object.handle_mouse)
    sweeperlib.set_draw_handler(game_object.sprite_handler.draw_screen)
    sweeperlib.set_interval_handler(game_object.sprite_handler.update_timer, 1)

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
