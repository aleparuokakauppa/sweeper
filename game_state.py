import random
import game_constants

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              ( 0, -1),          ( 0, 1),
              ( 1, -1), ( 1, 0), ( 1, 1)]

class Game:
    """
    Class to hold the game's state

    Includes methods to manipulate the state
    """
    def __init__(self, board_size: tuple[int, int], n_mines: int):
        """
        Initialize the object attributes
        Places `n_mines` amount of mines randomly on the `game_board`

        :params int board_size: board size in (x-size, y-size) format
        :params int n_mines: number of mines to be placed
        """
        # Keeps track of revealed tiles to the player
        self.explored_tiles: list[tuple[int, int]] = []

        self.flagged_tiles: list[tuple[int, int]] = []
        self.n_mines: int = 0
        self.turns_used: int = 0
        self.remaining_time: int = game_constants.STARTING_TIME
        self.n_mines: int = n_mines

        self.board_size = board_size
        self.board_size_px = (self.board_size[0] * game_constants.TILE_SPRITE_SIZE_PX,
                              self.board_size[1] * game_constants.TILE_SPRITE_SIZE_PX)

        # Initialize board
        self.game_board: list[list[str]]  = []
        for _ in range(self.board_size[1]):
            row: list[str] = []
            for _ in range(self.board_size[0]):
                row.append(' ')
            self.game_board.append(row)

        # Initialize mines on the game board
        allocated_mines: list[tuple[(int, int)]] = []
        while len(allocated_mines) < n_mines:
            rand_y = random.randint(0, self.board_size[1] - 1)
            rand_x = random.randint(0, self.board_size[0] - 1)
            if (rand_x, rand_y) not in allocated_mines:
                self.set_tile_content((rand_x, rand_y), 'x')
                allocated_mines.append((rand_x, rand_y))

        # Sets the tile contents for each `game_tile` according to
        # the amount of surrounding mines each has
        for y_index in range(self.board_size[1]):
            for x_index in range(self.board_size[0]):
                if self.get_tile_content((x_index, y_index)) != 'x':
                    surrounding_mines_n = self.count_tile_surroundings((x_index, y_index))
                    self.set_tile_content((x_index, y_index), str(surrounding_mines_n))

    def count_tile_surroundings(self, tile: tuple[(int, int)]) -> int:
        """
        Returns the amount of mines around the given tile.
        If the given tile is outside of the board, returns 0

        :params tuple[(int, int)] tile: tile (x,y) index-coordinates of the target tile
        """
        tile_x_pos, tile_y_pos = tile

        # Check if the given tile is within boundaries
        if not 0 <= tile_y_pos < self.board_size[1]:
            if not 0 <= tile_x_pos < self.board_size[0]:
                return 0

        count = 0
        for dir_x, dir_y in DIRECTIONS:
            new_x, new_y = tile_x_pos + dir_x, tile_y_pos + dir_y
            # Check if tile is inside
            if 0 <= new_x < self.board_size[0]:
                if 0 <= new_y < self.board_size[1]:
                    if self.get_tile_content((new_x, new_y)) == 'x':
                        count += 1
        return count

    def guess_tile(self, tile: tuple[(int, int)]) -> None:
        """
        Updates the game board according to floodfill logic by
        adding visited tiles into the `explored_fields` attribute
        if the clicked tile is a mine, only the mine is marked
        as explored

        :params tuple[(int, int)] tile: starting tile for guess algorithm
        """
        if self.get_tile_content(tile) == 'x':
            self.explored_tiles.append(tile)
            # 'X' is the exploded marker for a tile
            self.set_tile_content(tile, 'X')
            self.game_over = True
            return

        to_explore: list[tuple[(int, int)]] = [tile]
        while len(to_explore) > 0:
            # Get position and remove the last element of the list
            (tile_x, tile_y) = to_explore.pop()

            # Mark tile as explored and revealed
            if (tile_x, tile_y) not in self.explored_tiles:
                self.explored_tiles.append((tile_x, tile_y))

            surrounding_tiles: list[tuple[(int, int)]] = []

            no_surrounding_mines = True

            # Add surroundings into to_explore if unexplored
            for dir_x, dir_y in DIRECTIONS:
                new_x, new_y = tile_x + dir_x, tile_y + dir_y
                # Check if new tile is inside
                if 0 <= new_x < self.board_size[0]:
                    if 0 <= new_y < self.board_size[1]:
                        # Check if a neighbor is a mine
                        if self.get_tile_content((new_x, new_y)) == 'x':
                            no_surrounding_mines = False
                            break
                        # Check if the neighbor hasn't been explored
                        if (new_x, new_y) not in self.explored_tiles:
                            surrounding_tiles.append((new_x, new_y))
            if no_surrounding_mines:
                to_explore.extend(surrounding_tiles)
        self.update_win()

    def get_tile_content(self, tile: tuple[(int, int)]) -> str:
        """
        Helper function for coordinate-like indexing
        Returns the contents of the tile given in (x,y) format
        as a string

        Raises an `IndexError` if invalid tile

        :params tuple[(int, int)] tile: tile that content is stored in
        """
        if 0 <= tile[1] < len(self.game_board) and 0 <= tile[0] < len(self.game_board[0]):
            return self.game_board[tile[1]][tile[0]]
        print(f"No tile content. Position {tile} was outside of board")
        raise IndexError

    def set_tile_content(self, tile: tuple[(int, int)], content: str):
        """
        Helper function for coordinate-like indexing
        Sets the string content into the given (x,y) position

        Raises an `IndexError` if invalid tile

        :params tuple[(int, int)] tile: tile that content is stored in
        :params str content: string content to be stored in tile
        """
        if 0 <= tile[1] < len(self.game_board) and 0 <= tile[0] < len(self.game_board[0]):
            self.game_board[tile[1]][tile[0]] = content
        else:
            print(f"Cannot set content at {tile} "
                  "is outside of game board")
            raise IndexError

    def update_win(self):
        """
        Updates the objects `win` attribute according to
        the amount of explored tiles
        """
        target_explored_tile_count = self.board_size[0] * self.board_size[1] - self.n_mines
        self.win = len(self.explored_tiles) == target_explored_tile_count
