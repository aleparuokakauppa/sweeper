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

    def __init__(self, grid_x_max = 0, grid_y_max = 0):
        """
        Initializes the game field with blank tiles
        """
        self.grid_x_size = grid_x_max
        self.grid_y_size = grid_y_max
        self.max_x_index = grid_x_max - 1
        self.max_y_index = grid_y_max - 1

        self.game_field = np.full((grid_x_max, grid_y_max), ' ', '<U1')

    def init_mines(self, n_mines: int):
        """
        Places `n_mines` amount of mines randomly on the game_field
        """
        # Keep track of this in the front end
        if n_mines <= 0:
            print("Not enough mines provided")
            return

        allocated_mines: list[tuple[(int, int)]] = []
        while len(allocated_mines) <= n_mines:
            rand_x = random.randint(0, self.grid_y_size)
            rand_y = random.randint(0, self.grid_x_size)
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
        tile_x_pos = tile[0]
        tile_y_pos = tile[1]

        # Check if the given tile is within boundaries
        if tile_x_pos < 0 or tile_y_pos < 0 or tile_x_pos >= self.grid_x_size or tile_y_pos >= self.grid_y_size:
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
            sel_tile = self.game_field[(x_index, y_index)]
            if sel_tile != 'x':
                drawn_key = str(self.count_surroundings(sel_tile))
            sweeperlib.prepare_sprite(
                        drawn_key,
                        x_index * TILE_SPRITE_SIZE,
                        y_index * TILE_SPRITE_SIZE)
        sweeperlib.draw_sprites()

    def handle_mouse(self, x_pos: int, y_pos: int, m_button: int, mod: int):
        # Check if the click is in the game-area
        # if is, check what position the player clicked
        # then attempt a guess
        # then draw the new screen with updated information
        pass

def main():
    game = Game()
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(600, 400)
    sweeperlib.set_draw_handler(game.draw_field)
    sweeperlib.set_mouse_handler(game.handle_mouse)
    sweeperlib.start()

if __name__ == "__main__":
    main()
