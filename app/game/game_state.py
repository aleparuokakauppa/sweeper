"""
Module that includes the game-object

The game object is the representation of game state

Includes methods to manipulate state and act game logic
"""

import random
from .game_constants import TILE_SPRITE_SIZE_PX, DIRECTIONS, STARTING_TIME

class Game:
    """
    Class to hold the game's state

    Includes methods for game logic
    """
    explored_tiles: list[tuple[int, int]]
    flagged_tiles: list[tuple[int, int]]
    mine_count: int
    turns_used: int
    remaining_time: int
    game_over: bool
    win: bool
    board_size: tuple[int, int]
    board_size_px: tuple[int, int]

    def __init__(self, board_size: tuple[int, int], mine_count: int):
        """
        Initialize the object attributes
        Places `n_mines` amount of mines randomly on the `game_board`

        :params int board_size: board size in (x-size, y-size) format
        :params int n_mines: number of mines to be placed
        """
        # Init instance attributes
        self.explored_tiles: list[tuple[int, int]] = []
        self.flagged_tiles: list[tuple[int, int]] = []
        self.mine_count: int = mine_count
        self.turns_used: int = 0
        self.remaining_time: int = STARTING_TIME
        self.game_over = False
        self.win = False
        self.board_size = board_size
        self.board_size_px = (self.board_size[0] * TILE_SPRITE_SIZE_PX,
                              self.board_size[1] * TILE_SPRITE_SIZE_PX)

        # Initialize board
        self.game_board: list[list[str]]  = []
        for _ in range(self.board_size[1]):
            row: list[str] = []
            for _ in range(self.board_size[0]):
                row.append(' ')
            self.game_board.append(row)

        # Initialize mines on the game board
        allocated_mines: list[tuple[(int, int)]] = []
        while len(allocated_mines) < mine_count:
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
        # Check if the given tile is within boundaries
        try:
            self.get_tile_content(tile)
        except IndexError:
            return 0

        count = 0
        for dir_x, dir_y in DIRECTIONS:
            new_x, new_y = tile[0] + dir_x, tile[1] + dir_y
            try:
                if self.get_tile_content((new_x, new_y)) == 'x':
                    count += 1
            except IndexError:
                # Tile was outside
                # Don't increment
                pass
        return count

    def guess_tile(self, tile: tuple[(int, int)]) -> None:
        """
        Updates the game board according to floodfill logic by
        adding visited tiles into the `explored_fields` attribute
        if the clicked tile is a mine, only the mine is marked
        as explored

        As a side effect updates game_state.win according to game state

        :params tuple[(int, int)] tile: starting tile for guess algorithm
        """
        # Check if the given tile is within boundaries
        try:
            self.get_tile_content(tile)
        except IndexError:
            return

        if self.get_tile_content(tile) == 'x':
            self.explored_tiles.append(tile)
            # 'X' is the exploded marker for a tile
            self.set_tile_content(tile, 'X')
            self.game_over = True
            return

        to_explore: list[tuple[(int, int)]] = [tile]
        while len(to_explore) > 0:
            tile_to_explore = to_explore.pop()

            if tile_to_explore not in self.explored_tiles:
                self.explored_tiles.append(tile_to_explore)

            surrounding_tiles: list[tuple[(int, int)]] = []
            no_surrounding_mines = True
            # Add surroundings into to_explore if unexplored
            for dir_x, dir_y in DIRECTIONS:
                new_x = tile_to_explore[0] + dir_x
                new_y = tile_to_explore[1] + dir_y
                try:
                    # Check if a neighbor is a mine
                    if self.get_tile_content((new_x, new_y)) == 'x':
                        no_surrounding_mines = False
                        break
                    # Check if the neighbor hasn't been explored
                    if (new_x, new_y) not in self.explored_tiles:
                        surrounding_tiles.append((new_x, new_y))
                except IndexError:
                    # New tile was outside
                    # Ignore tile
                    pass
            if no_surrounding_mines:
                to_explore.extend(surrounding_tiles)
        self.update_win()

    def get_tile_content(self, tile: tuple[(int, int)]) -> str:
        """
        Helper function for coordinate-like indexing
        Returns the contents of the tile given in (x,y) format
        as a string

        Raises an `IndexError` if invalid tile or outside game-board

        :params tuple[(int, int)] tile: tile that content is stored in
        """
        if 0 <= tile[0] < self.board_size[0]:
            if 0 <= tile[1] < self.board_size[1]:
                return self.game_board[tile[1]][tile[0]]
        #print(f"No tile content. Position {tile} was outside of board")
        raise IndexError

    def set_tile_content(self, tile: tuple[(int, int)], content: str):
        """
        Helper function for coordinate-like indexing
        Sets the string content into the given (x,y) position

        Raises an `IndexError` if invalid tile

        :params tuple[(int, int)] tile: tile that content is stored in
        :params str content: string content to be stored in tile
        """
        if 0 <= tile[1] < len(self.game_board):
            if 0 <= tile[0] < len(self.game_board[0]):
                self.game_board[tile[1]][tile[0]] = content
                return

        #print(f"Cannot set content at {tile} "
        #        "is outside of game board")
        raise IndexError

    def update_win(self):
        """
        Updates the win and game_over attribute according to
        the amount of explored tiles
        """
        target_explored_tile_count = self.board_size[0] * self.board_size[1] - self.mine_count
        if len(self.explored_tiles) == target_explored_tile_count:
            self.win, self.game_over = True, True
