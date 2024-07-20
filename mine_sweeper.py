import random
import numpy as np
import sweeperlib

TILE_SPRITE_SIZE = 64

class Game:
    """
    Main handlers for interaction with the game's tiles
    """

    game_board: list[list[str]]
    board_x_size: int
    board_y_size: int

    board_size_px: tuple[(int, int)]

    def __init__(self, grid_x_max = 0, grid_y_max = 0):
        """
        Initializes the game field with blank tiles
        """
        self.board_x_size = grid_x_max
        self.board_y_size = grid_y_max
        self.game_board = []
        # TODO check off by 1
        for _ in range(grid_y_max):
            row: list[str] = []
            for _ in range(grid_x_max):
                row.append(' ')
            self.game_board.append(row)

    def init_field_contents(self, n_mines: int):
        """
        Places `n_mines` amount of mines randomly on the game_field
        """
        # Keep track of this in the front end
        if n_mines <= 0:
            print("Not enough mines provided")
            return

        max_mines = self.board_x_size * self.board_y_size
        if n_mines > max_mines:
            print(f"Too many mines! Using maximun amount ({max_mines}) mines.")
            n_mines = max_mines

        allocated_mines: list[tuple[(int, int)]] = []
        while len(allocated_mines) <= n_mines:
            rand_y = random.randint(0, self.board_y_size - 1)
            rand_x = random.randint(0, self.board_x_size - 1)
            if (rand_x, rand_y) not in allocated_mines:
                self.set_tile_content((rand_x, rand_y), 'x')
                allocated_mines.append((rand_x, rand_y))

        # Now go over the field and assign number of mines to each
        # if the tile in question isn't a mine
        for y_index in range(self.board_y_size):
            for x_index in range(self.board_x_size):
                content = self.get_tile_content((x_index, y_index))
                if content != 'x':
                    surrounding_mines_n = self.count_surroundings((x_index, y_index))
                    self.set_tile_content((x_index, y_index), str(surrounding_mines_n))

    def get_tile_content(self, position: tuple[(int, int)]) -> str:
        """
        Helper function for coordinate-like indexing
        Returns the contents of the tile given in (x,y) format
        as a string
        If position is outside of the board, returns '': str
        """
        if 0 <= position[1] < len(self.game_board) and 0 <= position[0] < len(self.game_board[0]):
            return self.game_board[position[1]][position[0]]
        else:
            print(f"No tile content. Position {position} was outside of board")
            return ''

    def set_tile_content(self, position: tuple[(int, int)], content: str):
        """
        Helper function for coordinate-like indexing
        Sets the string content into the given (x,y) position
        """
        if 0 <= position[1] < len(self.game_board) and 0 <= position[0] < len(self.game_board[0]):
            self.game_board[position[1]][position[0]] = content
        else:
            print(f"Cannot set content at {position} "
                  "is outside of game board")

    def set_board_size(self, width: int, height: int):
        self.board_size_px = (width, height)

    def guess_tile(self, tile: tuple[(int, int)]) -> None:
        """
        TODO
        """

        # If starting position has a mine, TODO EXPLODE!!!!!
        if self.get_tile_content(tile) == 'x':
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
            self.set_tile_content((tile_x, tile_y), '0')

            # Add surroundings into to_explore if unexplored
            surrounding_tiles: list[tuple[(int, int)]] = []
            for dir_x, dir_y in directions:
                new_row, new_col = tile_y + dir_x, tile_x + dir_y
                # Check if new tile is inside
                if 0 <= new_row < len(self.game_board) and 0 <= new_col < len(self.game_board[0]):
                    # Check if the neighbor hasn't been explored and is safe
                    if self.get_tile_content((dir_x, dir_y)) == ' ':
                        surrounding_tiles.append((new_col, new_row))
            to_explore.extend(surrounding_tiles)

    def count_surroundings(self, tile: tuple[(int, int)]) -> int:
        """
        Counts the amount of mines around the given tile
        """
        tile_x_pos, tile_y_pos = tile

        # Check if the given tile is within boundaries
        if not (0 <= tile_x_pos < self.board_x_size and 0 <= tile_y_pos < self.board_y_size):
            return 0

        directions = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),         (0, 1),
                    (1, -1), (1, 0), (1, 1)]
        
        count = 0
        for dir_x, dir_y in directions:
            new_x, new_y = tile_x_pos + dir_x, tile_y_pos + dir_y
            # Check if tile is inside
            if 0 <= new_x < self.board_y_size and 0 <= new_y < self.board_x_size:
                if self.get_tile_content((new_x, new_y)) == 'x':
                    count += 1
        
        return count


    def draw_field(self):
        sweeperlib.clear_window()
        sweeperlib.begin_sprite_draw()
        for y_index, row in enumerate(self.game_board):
            for x_index, tile_content in enumerate(row):
                sweeperlib.prepare_sprite(
                            tile_content,
                            x_index * TILE_SPRITE_SIZE,
                            y_index * TILE_SPRITE_SIZE)
        sweeperlib.draw_sprites()

    def get_tile_index_at_coordinates(self, x_pos: int, y_pos: int) -> tuple[(int, int)]:
        x_index: int = round(x_pos / TILE_SPRITE_SIZE)
        y_index: int = round(y_pos / TILE_SPRITE_SIZE)
        return (x_index, y_index)

    def handle_mouse(self, x_pos: int, y_pos: int, m_button: int, mod: int):
        # Check if click was within the board
        max_board_y, max_board_x = self.board_size_px
        if x_pos <= 0 or x_pos > max_board_x or y_pos <= 0 or y_pos > max_board_y:
            print("Click was outside of game board")
            return

        # Get the approximate clicked tile
        selected_tile: tuple[(int, int)] = self.get_tile_index_at_coordinates(x_pos, y_pos)

        # Match the mouse button with an action
        match m_button:
            case sweeperlib.MOUSE_LEFT:
                self.guess_tile(selected_tile)
            case sweeperlib.MOUSE_RIGHT:
                # TODO
                # Add a flag to the tile
                pass

    def print_grid(self) -> None:
        """
        Prints the grid given grid to stdout
        """
        print(" ", "- " * self.board_x_size)
        for y_index in range(self.board_y_size - 1, -1, -1):
            row = []
            for x_index in range(self.board_x_size):
                row.append(self.get_tile_content((x_index, y_index)))
            print("|", " ".join(row), "|")
        print(" ", "- " * self.board_x_size)


def main():
    game = Game(10, 15)
    game.set_board_size(600, 600)
    game.init_field_contents(n_mines=15)
    game.print_grid()
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
