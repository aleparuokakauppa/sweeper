import random
import sweeperlib
from math import floor

class Game:
    """
    Main sweeper-game object with state and
    methods for interacting with game state
    """
    # Constant size for sprite size in pixels
    TILE_SPRITE_SIZE_PX = 64

    # TODO win condition
    game_over: bool = False
    win: bool = False

    game_board: list[list[str]]

    board_x_size: int
    board_y_size: int
    n_mines: int

    explored_tiles: list[tuple[(int,int)]] = []

    flagged_tiles: list[tuple[(int, int)]] = []

    board_size_px: tuple[(int, int)]


    def __init__(self, board_size: tuple[(int, int)]):
        """
        Initializes the `game_board` with blank tiles at the specified
        board size

        :params tuple[(int, int)] board_size: (x,y) represented board maximum size
        """
        self.board_x_size, self.board_y_size = board_size

        if self.board_x_size < 2 or self.board_y_size < 2:
            print("Invalid board size. minimum size is 2x2")
            print("Using 2x2")
            self.board_x_size = 2
            self.board_y_size = 2

        # Initialize board
        self.game_board = []
        for _ in range(self.board_y_size):
            row: list[str] = []
            for _ in range(self.board_x_size):
                row.append(' ')
            self.game_board.append(row)

        # Set the board size in px
        # used in capturing clicked tile
        self.board_size_px = (self.board_x_size * self.TILE_SPRITE_SIZE_PX,
                              self.board_y_size * self.TILE_SPRITE_SIZE_PX)


    def init_tile_contents(self, n_mines: int):
        """
        Places `n_mines` amount of mines randomly on the `game_board`

        :params int n_mines: number of mines to be placed
        """
        self.n_mines = n_mines

        if n_mines <= 0:
            print("Minimum mine count is 1")
            print("Using mine count 1")
            n_mines = 1

        max_mines = self.board_x_size * self.board_y_size - 1
        if n_mines > max_mines:
            print(f"Too many mines! Using maximum amount ({max_mines}) mines.")
            n_mines = max_mines

        allocated_mines: list[tuple[(int, int)]] = []
        while len(allocated_mines) <= n_mines:
            rand_y = random.randint(0, self.board_y_size - 1)
            rand_x = random.randint(0, self.board_x_size - 1)
            if (rand_x, rand_y) not in allocated_mines:
                self.set_tile_content((rand_x, rand_y), 'x')
                allocated_mines.append((rand_x, rand_y))

        # Sets the tile contents for each `game_tile` according to
        # the amount of surrounding mines each has
        for y_index in range(self.board_y_size):
            for x_index in range(self.board_x_size):
                if self.get_tile_content((x_index, y_index)) != 'x':
                    surrounding_mines_n = self.count_surroundings((x_index, y_index))
                    self.set_tile_content((x_index, y_index), str(surrounding_mines_n))


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
        else:
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


    def guess_tile(self, tile: tuple[(int, int)]) -> None:
        """
        Updates the game board according to floodfill logic by
        adding visited tiles into the `explored_fields` attribute
        if the clicked tile is a mine, only the mine is marked
        as explored

        :params tuple[(int, int)] tile: starting tile for guess algorithm
        """

        # If tile is a bomb
        if self.get_tile_content(tile) == 'x':
            self.explored_tiles.append(tile)
            # 'X' is the exploded marker for a tile
            self.set_tile_content(tile, 'X')
            self.game_over = True
            return

        directions = [(-1, -1), (-1, 0), (-1, 1),
                      ( 0, -1),          ( 0, 1),
                      ( 1, -1), ( 1, 0), ( 1, 1)]

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
            for dir_x, dir_y in directions:
                new_x, new_y = tile_x + dir_x, tile_y + dir_y
                # Check if new tile is inside
                if 0 <= new_x and new_x < self.board_x_size:
                    if 0 <= new_y and new_y < self.board_y_size:
                        # Check if a neighbor is a mine
                        if self.get_tile_content((new_x, new_y)) == 'x':
                            no_surrounding_mines = False
                            break
                        # Check if the neighbor hasn't been explored
                        if (new_x, new_y) not in self.explored_tiles:
                            surrounding_tiles.append((new_x, new_y))

            if no_surrounding_mines:
                to_explore.extend(surrounding_tiles)


    def count_surroundings(self, tile: tuple[(int, int)]) -> int:
        """
        Returns the amount of mines around the given tile.
        If the given tile is outside of the board, returns 0

        :params tuple[(int, int)] tile: tile (x,y) index-coordinates of the target tile
        """
        tile_x_pos, tile_y_pos = tile

        # Check if the given tile is within boundaries
        if not (0 <= tile_y_pos and tile_y_pos < self.board_y_size):
            if not (0 <= tile_x_pos and tile_x_pos < self.board_x_size):
                return 0

        directions = [(-1, -1), (-1, 0), (-1, 1),
                      ( 0, -1),          ( 0, 1),
                      ( 1, -1), ( 1, 0), ( 1, 1)]
        
        count = 0
        for dir_x, dir_y in directions:
            new_x, new_y = tile_x_pos + dir_x, tile_y_pos + dir_y
            # Check if tile is inside
            if 0 <= new_x and new_x < self.board_x_size:
                if 0 <= new_y and new_y < self.board_y_size:
                    if self.get_tile_content((new_x, new_y)) == 'x':
                        count += 1
        return count


    def draw_field(self):
        """
        Main-game draw field handler for the pyglet program.
        Draws sprites based on the `game_board` string contents
        of each tile with additional draw logic
        """
        sweeperlib.clear_window()
        sweeperlib.begin_sprite_draw()
        for y_index, row in enumerate(self.game_board):
            for x_index, tile_content in enumerate(row):
                draw_key = " "
                if (x_index, y_index) in self.explored_tiles:
                    draw_key = tile_content

                if (x_index, y_index) in self.flagged_tiles:
                    draw_key = 'f'
                    if self.game_over and tile_content != 'x':
                        draw_key = 'F'

                if self.game_over and tile_content == 'x':
                    draw_key = 'x'
                    if (x_index, y_index) in self.flagged_tiles:
                        draw_key = 'f'

                sweeperlib.prepare_sprite(
                            draw_key,
                            x_index * self.TILE_SPRITE_SIZE_PX,
                            y_index * self.TILE_SPRITE_SIZE_PX)
        sweeperlib.draw_sprites()


    def get_tile_index_at_coordinates(self, position: tuple[(int, int)]) -> tuple[(int, int)]:
        """
        Approximates which tile the user clicked

        Returns the approximated (x,y) index-coordinates of game tiles
        used in game logic

        :params tuple[(int, int)] position: Mouse coordinates of the clicked window position
        """
        x_index: int = floor(position[0] / self.TILE_SPRITE_SIZE_PX)
        y_index: int = floor(position[1] / self.TILE_SPRITE_SIZE_PX)
        return (x_index, y_index)


    def handle_mouse(self, x_pos: int, y_pos: int, m_button: int, mod: int):
        """
        Pyglet mouse handler for interacting with game UI

        :params int x_pos: Mouse x-position on the window
        :params int y_pos: Mouse y-position on the window
        :params int m_button: Pyglet mouse button with which the window was clicked
        :params int mod: Binary representation of applied keyboard modifiers (not used)
        """
        if self.game_over:
            # Exits the program
            print("You lost!")
            sweeperlib.close()
            return

        # Check if click was within the board
        max_board_x, max_board_y = self.board_size_px

        if x_pos <= 0 or x_pos > max_board_x or y_pos <= 0 or y_pos > max_board_y:
            return

        # Get the approximate clicked tile
        selected_tile: tuple[(int, int)] = self.get_tile_index_at_coordinates((x_pos, y_pos))

        # Match the mouse button with an action
        match m_button:
            case sweeperlib.MOUSE_LEFT:
                self.guess_tile(selected_tile)
                self.update_win()

            case sweeperlib.MOUSE_RIGHT:
                if selected_tile not in self.flagged_tiles:
                    self.flagged_tiles.append(selected_tile)
                else:
                    self.flagged_tiles.remove(selected_tile)


    def print_board(self) -> None:
        """
        Prints the `game_board` to stdout.
        Used in development
        """
        print(" ", "- " * self.board_x_size)
        for y_index in range(self.board_y_size - 1, -1, -1):
            row = []
            for x_index in range(self.board_x_size):
                row.append(self.get_tile_content((x_index, y_index)))
            print("|", " ".join(row), "|")
        print(" ", "- " * self.board_x_size)


    def update_win(self):
        print(f"n_explored_tiles: {len(self.explored_tiles)}")
        print(f"board_size: {self.board_x_size * self.board_y_size}")
        win = len(self.explored_tiles) == self.board_x_size * self.board_y_size - self.n_mines
        if win:
            sweeperlib.close()
            print("You win!")
