"""
Handler for starting the graphical game
"""
from math import floor

from app import scoreboard_logging
from app import prompt_helpers
from app.sprite_helper import SpriteHelper
from app.lib import sweeperlib

from .game_constants import TILE_SPRITE_SIZE_PX, STARTING_TIME, GRAY_BG_RGBA
from .game_state import Game

class GameHandler:
    """
    Main sweeper-game object

    Is the owner of game state
    """
    game_properties: dict

    game_state: Game
    sprite_helper: SpriteHelper

    player_name: str
    difficulty: int

    turns_used: int

    def __init__(self):
        """
        Initializes the game properties and initializes game state.

        Asks user for input with `prompt_helpers.get_game_properties`
        """
        self.game_properties = prompt_helpers.get_game_properties()

        self.game_state = Game(self.game_properties["board-size"],
                               self.game_properties["mine-count"])

        self.sprite_helper = SpriteHelper(self.game_state)

        self.player_name = self.game_properties["player-name"]
        self.difficulty = self.game_properties["difficulty"]

        self.turns_used: int = 0

    def start_game(self):
        """
        Creates the pyglet window and starts the event loop
        """
        sweeperlib.load_sprites("resources/sprites")

        sweeperlib.create_window(
                self.game_properties["board-size-px"][0],
                self.game_properties["board-size-px"][1] + 128,
                GRAY_BG_RGBA,
                title="Mine Sweeper"
                )

        # Set pyglet handlers
        sweeperlib.set_mouse_handler(self.handle_mouse)
        sweeperlib.set_interval_handler(self.update_timer, 1)
        sweeperlib.set_draw_handler(self.sprite_helper.draw_screen)
        sweeperlib.start()

    def get_tile_pos_at_coordinates(self, position: tuple[(int, int)]) -> tuple[(int, int)]:
        """
        Approximates which tile the user clicked

        Returns the approximated (x,y) index-coordinates of game tiles
        used in game logic

        :params tuple[(int, int)] position: Mouse coordinates of the clicked window position
        """
        x_index: int = floor(position[0] / TILE_SPRITE_SIZE_PX)
        y_index: int = floor(position[1] / TILE_SPRITE_SIZE_PX)
        return (x_index, y_index)

    def update_timer(self, _):
        """
        Decrements game_state.remaining_time by 1 on each iteration

        Updates game_state.game_over if timer reaches 0

        Set by `sweeperlib.set_interval_handler`
        """
        if self.game_state.remaining_time > 0:
            if not self.game_state.game_over:
                if not self.game_state.win:
                    self.game_state.remaining_time -= 1

        if self.game_state.remaining_time <= 0:
            # Player lost, game is over
            self.game_state.game_over = True

    def handle_mouse(self, x_pos: int, y_pos: int, m_button: int, _: int):
        """
        Pyglet mouse handler for interacting with game UI

        Set by `sweeperlib.set_mouse_handler`

        :params int x_pos: Mouse x-position on the window
        :params int y_pos: Mouse y-position on the window
        :params int m_button: Pyglet mouse button with which the window was clicked
        """
        if self.game_state.game_over:
            board_x_size = self.game_state.board_size[0]
            board_y_size = self.game_state.board_size[1]
            total_tiles = board_x_size * board_y_size

            mine_count = self.game_state.mine_count
            tiles_explored = len(self.game_state.explored_tiles)

            left_to_explore = total_tiles - mine_count - tiles_explored

            scoreboard_logging.write_scoreboard_data(
                self.player_name,
                self.difficulty,
                self.turns_used,
                STARTING_TIME - self.game_state.remaining_time,
                left_to_explore,
                self.game_state.board_size)

            sweeperlib.close()

        max_board_x, max_board_y = self.game_state.board_size_px

        # Check if click was outside of the board
        if x_pos <= 0 or x_pos > max_board_x:
            return
        if y_pos <= 0 or y_pos > max_board_y:
            return

        # Get the approximate clicked tile
        selected_tile = self.get_tile_pos_at_coordinates((x_pos, y_pos))

        # Match the mouse button with an action
        match m_button:
            case sweeperlib.MOUSE_LEFT:
                # Cannot guess a flagged tile
                if selected_tile not in self.game_state.flagged_tiles:
                    self.turns_used += 1
                    self.game_state.guess_tile(selected_tile)

            case sweeperlib.MOUSE_RIGHT:
                if selected_tile in self.game_state.flagged_tiles:
                    self.game_state.flagged_tiles.remove(selected_tile)

                elif selected_tile not in self.game_state.explored_tiles:
                    self.game_state.flagged_tiles.append(selected_tile)
