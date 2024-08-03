"""
Main program script

The user interface and the game is started from here
"""
from scoreboard_logging import print_scores
from game_handler import GameHandler

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
                GameHandler().start_game()
            case 's':
                print_scores()
            case 'q':
                print("Goodbye...")
                break
            case _:
                print("\nNot a valid action. Try again.\n")

if __name__ == "__main__":
    try:
        main_menu()
    # Catch ^C
    except KeyboardInterrupt:
        print("\nExiting!")
    # Catch ^D
    except EOFError:
        print("\nExiting!")
