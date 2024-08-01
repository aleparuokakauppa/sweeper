"""
Main game logic object for:
- Drawing on the pyglet screen
- Checking clicks
- Updating sprites to match game state
- Game logic
"""
from math import floor
import sweeperlib
import game_constants
import scoreboard_logging
from game_state import Game
from sprite_helper import Sprites

class GameHandler:
    """
    Main sweeper-game object

    Is the owner of game state
    """
    player_name: str
    difficulty: int
    turns_used: int

    game_state: Game
    sprite_handlers: Sprites

    def __init__(self, board_size: tuple[(int, int)], n_mines: int):
        """
        Initializes the Game object

        Is the owner of game state

        :params tuple[(int, int)] board_size: (x,y) format board max size
        """
        self.game_state = Game(board_size, n_mines)
        self.sprite_handlers = Sprites(self.game_state)

    def get_tile_index_at_coordinates(self, position: tuple[(int, int)]) -> tuple[(int, int)]:
        """
        Approximates which tile the user clicked

        Returns the approximated (x,y) index-coordinates of game tiles
        used in game logic

        :params tuple[(int, int)] position: Mouse coordinates of the clicked window position
        """
        x_index: int = floor(position[0] / game_constants.TILE_SPRITE_SIZE_PX)
        y_index: int = floor(position[1] / game_constants.TILE_SPRITE_SIZE_PX)
        return (x_index, y_index)

    def handle_mouse(self, x_pos: int, y_pos: int, m_button: int, _: int):
        """
        Pyglet mouse handler for interacting with game UI

        :params int x_pos: Mouse x-position on the window
        :params int y_pos: Mouse y-position on the window
        :params int m_button: Pyglet mouse button with which the window was clicked
        """
        if self.game_state.win or self.game_state.game_over:
            target_explored_tile_count = self.game_state.board_size[0] * self.game_state.board_size[1] - self.game_state.n_mines

            scoreboard_logging.write_scoreboard_data(
                self.player_name,
                self.difficulty,
                self.turns_used,
                game_constants.STARTING_TIME - self.game_state.remaining_time,
                target_explored_tile_count - len(self.game_state.explored_tiles),
                self.game_state.board_size)

            sweeperlib.close()
            return

        max_board_x, max_board_y = self.game_state.board_size_px

        # Check if click was within the board
        if x_pos <= 0 or x_pos > max_board_x or y_pos <= 0 or y_pos > max_board_y:
            return

        # Get the approximate clicked tile
        selected_tile = self.get_tile_index_at_coordinates((x_pos, y_pos))

        # Match the mouse button with an action
        match m_button:
            case sweeperlib.MOUSE_LEFT:
                self.turns_used += 1
                self.game_state.guess_tile(selected_tile)

            case sweeperlib.MOUSE_RIGHT:
                if selected_tile in self.game_state.flagged_tiles:
                    self.game_state.flagged_tiles.remove(selected_tile)

                elif selected_tile not in self.game_state.explored_tiles:
                    self.game_state.flagged_tiles.append(selected_tile)
