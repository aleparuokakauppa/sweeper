"""
Main program script

The user interface and the game is started from here
"""
import sweeperlib
import game_constants
from game_logic import GameHandler
from prompt_helpers import get_game_properties
from scoreboard_logging import print_scores

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
                print_scores()
            case 'q':
                print("Goodbye...")
                break
            case _:
                print("\nNot a valid action. Try again.\n")

def start_game():
    """
    Starts the graphical game
    """
    game_props = get_game_properties()

    game_handler = GameHandler(game_props["game-size"], game_props["mine-count"])

    game_handler.difficulty = game_props["difficulty"]
    game_handler.player_name = game_props["player-name"]

    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(
            game_props["board-size-x"],
            game_props["board-size-y"] + 128,
            game_constants.GRAY_BG_RGB,
            title="Mine Sweeper"
            )
    # Set pyglet handlers
    sweeperlib.set_mouse_handler(game_handler.handle_mouse)
    sweeperlib.set_draw_handler(game_handler.sprite_handlers.draw_screen)
    sweeperlib.set_interval_handler(game_handler.sprite_handlers.update_timer, 1)
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
