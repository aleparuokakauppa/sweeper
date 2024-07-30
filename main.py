import sweeperlib
import prompt_helpers
from game_logic import Game

def init_game():
    player_name = input("Player name: ")
    game_x_size = prompt_helpers.prompt_int("Give game size X: ", "Not a valid size")
    game_y_size = prompt_helpers.prompt_int("Give game size Y: ", "Not a valid size")

    game = Game((game_x_size, game_y_size))
    game.player_name = player_name

    n_mines = prompt_helpers.prompt_difficulty(game)
    game.init_tile_contents(n_mines=n_mines)

    game.print_scores()

    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(game.board_size_px[0], game.board_size_px[1]+128, (192, 192, 192, 255), title="Mine Sweeper")

    # Set pyglet handlers
    sweeperlib.set_draw_handler(game.draw_field)
    sweeperlib.set_mouse_handler(game.handle_mouse)
    sweeperlib.set_interval_handler(game.draw_timer, 1)

    sweeperlib.start()
    print("flag")

if __name__ == "__main__":
    try:
        init_game()
    except KeyboardInterrupt:
        print("\nExiting!")
