import random
import numpy as np
import sweeperlib

TILE_SPRITE_SIZE = 64

class Game:
    """
    Main handlers for interaction with the game's tiles
    """

    game_field: np.ndarray
    grid_x_size: int
    grid_y_size: int

    max_x_index: int
    max_y_index: int

    board_size_px: tuple[(int, int)]

    def __init__(self, grid_x_max = 0, grid_y_max = 0):
        """
        Initializes the game field with blank tiles
        """
        self.grid_x_size = grid_x_max
        self.grid_y_size = grid_y_max
        self.max_x_index = grid_x_max - 1
        self.max_y_index = grid_y_max - 1

        self.game_field = np.full((grid_x_max, grid_y_max), ' ', '<U1')

    def set_board_size(self, width: int, height: int):
        self.board_size_px = (width, height)

    def init_mines(self, n_mines: int):
        """
        Places `n_mines` amount of mines randomly on the game_field
        """
        # Keep track of this in the front end
        if n_mines <= 0:
            print("Not enough mines provided")
            return

        max_mines = self.grid_x_size * self.grid_y_size
        if n_mines > max_mines:
            print(f"Too many mines! Using maximun amount ({max_mines}) mines.")
            n_mines = max_mines

        allocated_mines: list[tuple[(int, int)]] = []
        while len(allocated_mines) <= n_mines:
            rand_x = random.randint(0, self.max_x_index)
            rand_y = random.randint(0, self.max_y_index)
            if (rand_x, rand_y) not in allocated_mines:
                self.game_field[(rand_x, rand_y)] = 'x'
                allocated_mines.append((rand_x, rand_y))

    def guess_tile(self, tile: tuple[(int, int)]) -> None:
        """
        TODO
        """

        # If starting position has a mine, TODO EXPLODE!!!!!
        if self.game_field[tile] == 'x':
            # BOOOOOM
            return

        directions = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),         (0, 1),
                    (1, -1), (1, 0), (1, 1)]

        to_explore: list[tuple[(int, int)]] = [tile]

        while len(to_explore) > 0:
            # Get position and removes the last element of the list
            (tile_x, tile_y) = to_explore.pop()

            # Mark tile as safe
            self.game_field[(tile_x, tile_y)] = '0'

            # Add surroundings into to_explore if unexplored
            surrounding_tiles: list[tuple[(int, int)]] = []
            for dir_x, dir_y in directions:
                new_row, new_col = tile_y + dir_x, tile_x + dir_y
                # Check if new tile is inside
                if 0 <= new_row < len(self.game_field) and 0 <= new_col < len(self.game_field[0]):
                    # Check if the neighbor hasn't been explored and is safe
                    if self.game_field[(dir_x, dir_y)] == ' ':
                        surrounding_tiles.append((new_col, new_row))
            to_explore.extend(surrounding_tiles)

    def count_surroundings(self, tile: tuple[(int, int)]) -> int:
        """
        Counts the amount of mines around the given tile
        """
        tile_x_pos, tile_y_pos = tile

        # Check if the given tile is within boundaries
        if not (0 <= tile_x_pos < self.grid_x_size and 0 <= tile_y_pos < self.grid_y_size):
            return 0

        directions = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),         (0, 1),
                    (1, -1), (1, 0), (1, 1)]
        
        count = 0
        for dir_x, dir_y in directions:
            new_x, new_y = tile_x_pos + dir_x, tile_y_pos + dir_y

            if 0 <= new_x < self.grid_y_size and 0 <= new_y < self.grid_x_size:
                if self.game_field[tile] == 'x':
                    count += 1
        
        return count


    def draw_field(self):
        sweeperlib.clear_window()
        sweeperlib.begin_sprite_draw()
        for (x_index, y_index) in np.ndindex(self.game_field.shape):
            drawn_key: str = ' '
            if self.game_field[(x_index, y_index)] != 'x':
                drawn_key = str(self.count_surroundings((x_index, y_index)))
            sweeperlib.prepare_sprite(
                        drawn_key,
                        x_index * TILE_SPRITE_SIZE,
                        y_index * TILE_SPRITE_SIZE)
        sweeperlib.draw_sprites()

    def get_tile_at_coordinates(self, x_pos: int, y_pos: int) -> tuple[(int, int)]:
        x_index: int = round(x_pos / TILE_SPRITE_SIZE)
        y_index: int = round(y_pos / TILE_SPRITE_SIZE)
        return self.game_field[(x_index, y_index)]

    def handle_mouse(self, x_pos: int, y_pos: int, m_button: int, mod: int):
        # Check if click was within the board
        max_board_y, max_board_x = self.board_size_px
        if x_pos <= 0 or x_pos > max_board_x or y_pos <= 0 or y_pos > max_board_y:
            print("Click was outside of game board")
            return

        # Get the approximate clicked tile
        selected_tile: tuple[(int, int)] = self.get_tile_at_coordinates(x_pos, y_pos)

        # Match the mouse button with an action
        match m_button:
            case sweeperlib.MOUSE_LEFT:
                self.guess_tile(selected_tile)
            case sweeperlib.MOUSE_RIGHT:
                # TODO
                # Add a flag to the tile
                pass


def main():
    game = Game(10, 10)
    game.set_board_size(600, 600)
    game.init_mines(20)
    sweeperlib.load_sprites("sprites")
    # Window size and board size exist independently
    print("Sprites loaded")
    sweeperlib.create_window(*game.board_size_px)
    print("Window created")
    sweeperlib.set_draw_handler(game.draw_field)
    print("Draw handler set")
    sweeperlib.set_mouse_handler(game.handle_mouse)
    print("Mouse handler set")
    sweeperlib.start()

if __name__ == "__main__":
    main()
