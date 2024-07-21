import random
import sweeperlib
from math import floor

# Constant size for sprite size in pixels
TILE_SPRITE_SIZE_PX = 64

class Game:
    """
    Main sweeper-game object with state and
    methods for interacting with game state
    """

    # TODO win condition
    game_over: bool = False

    game_board: list[list[str]]

    board_x_size: int
    board_y_size: int

    explored_tiles: list[tuple[(int,int)]] = []
    flagged_tiles: list[tuple[(int, int)]] = []

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
        print(f"Board sizes: x={self.board_x_size} y={self.board_y_size}")
        for y_index in range(self.board_y_size):
            for x_index in range(self.board_x_size):
                if self.get_tile_content((x_index, y_index)) != 'x':
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
            raise IndexError


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
            raise IndexError


    def set_board_size(self, width: int, height: int):
        self.board_size_px = (width, height)


    def guess_tile(self, tile: tuple[(int, int)]) -> None:
        """
        Updates the game board according to floodfill logic by
        adding visited tiles into the `explored_fields` attribute
        if the clicked tile is a mine, only the mine is marked
        as explored
        """

        # If starting position has a mine, TODO EXPLODE!!!!!
        if self.get_tile_content(tile) == 'x':
            self.explored_tiles.append(tile)
            self.set_tile_content(tile, 'X')
            self.game_over = True
            return

        directions = [(-1, -1), (-1, 0), (-1, 1),
                      ( 0, -1),          ( 0, 1),
                      ( 1, -1), ( 1, 0), ( 1, 1)]

        to_explore: list[tuple[(int, int)]] = [tile]

        while len(to_explore) > 0:
            # Get position and removes the last element of the list
            (tile_x, tile_y) = to_explore.pop()

            # Mark tile as explored
            self.explored_tiles.append((tile_x, tile_y))

            # Add surroundings into to_explore if unexplored
            surrounding_tiles: list[tuple[(int, int)]] = []
            add_to_fill = True
            for dir_x, dir_y in directions:
                new_x, new_y = tile_x + dir_x, tile_y + dir_y
                # Check if new tile is inside
                if 0 <= new_x and new_x < self.board_x_size and 0 <= new_y and new_y < self.board_y_size:
                    # Check if a neighbor is a mine
                    if self.get_tile_content((new_x, new_y)) == 'x':
                        add_to_fill = False
                        break
                    # Check if the neighbor hasn't been explored
                    if (new_x, new_y) not in self.explored_tiles:
                        surrounding_tiles.append((new_x, new_y))
            if add_to_fill:
                to_explore.extend(surrounding_tiles)


    def count_surroundings(self, tile: tuple[(int, int)]) -> int:
        """
        Counts the amount of mines around the given tile
        """
        tile_x_pos, tile_y_pos = tile

        # Check if the given tile is within boundaries
        if not (0 <= tile_x_pos and tile_x_pos < self.board_x_size and 0 <= tile_y_pos and tile_y_pos < self.board_y_size):
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
                            x_index * TILE_SPRITE_SIZE_PX,
                            y_index * TILE_SPRITE_SIZE_PX)
        sweeperlib.draw_sprites()


    def get_tile_index_at_coordinates(self, x_pos: int, y_pos: int) -> tuple[(int, int)]:
        x_index: int = floor(x_pos / TILE_SPRITE_SIZE_PX)
        y_index: int = floor(y_pos / TILE_SPRITE_SIZE_PX)
        return (x_index, y_index)


    def handle_mouse(self, x_pos: int, y_pos: int, m_button: int, mod: int):
        if self.game_over:
            # Exits the program
            sweeperlib.close()
            return

        # Check if click was within the board
        max_board_x, max_board_y = self.board_size_px

        if x_pos <= 0 or x_pos > max_board_x or y_pos <= 0 or y_pos > max_board_y:
            return

        # Get the approximate clicked tile
        selected_tile: tuple[(int, int)] = self.get_tile_index_at_coordinates(x_pos, y_pos)

        # Match the mouse button with an action
        match m_button:
            case sweeperlib.MOUSE_LEFT:
                self.guess_tile(selected_tile)

            case sweeperlib.MOUSE_RIGHT:
                if selected_tile not in self.flagged_tiles:
                    self.flagged_tiles.append(selected_tile)
                else:
                    self.flagged_tiles.remove(selected_tile)


    def print_board(self) -> None:
        """
        Prints the board given grid to stdout
        """
        print(" ", "- " * self.board_x_size)
        for y_index in range(self.board_y_size - 1, -1, -1):
            row = []
            for x_index in range(self.board_x_size):
                row.append(self.get_tile_content((x_index, y_index)))
            print("|", " ".join(row), "|")
        print(" ", "- " * self.board_x_size)


def prompt_input(message: str, err_message: str) -> int:
    """
    Prompts the user for an integer using the prompt parameter.
    If an invalid input is given, an error message is shown using
    the error message parameter. A valid input is returned as an
    integer.
    """
    user_input: str = ""
    user_int: int = 0
    while True:
        user_input = input(message)
        try:
            user_int = int(user_input)
            if user_int > 100:
                raise ValueError
            return user_int
        except ValueError:
            print(err_message)


def prompt_difficulty(game_size: tuple[(int, int)]) -> int:
    """
    Prompts for game difficulty, returns the amount of mines for the game
    """
    user_input: str = ""
    mine_multiplier: float = 0.0
    while True:
        user_input = input("Select game difficulty (easy, medium, hard): ")
        match user_input:
            case "easy":
                mine_multiplier = 0.6
                break
            case "medium":
                mine_multiplier = 1.0
                break
            case "hard":
                mine_multiplier = 1.4
                break
            case _:
                print("Not a valid difficulty")
    return round((game_size[0] + game_size[1]) * mine_multiplier)


def main(sweeper_game: Game):
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(*sweeper_game.board_size_px)
    sweeperlib.set_draw_handler(sweeper_game.draw_field)
    sweeperlib.set_mouse_handler(sweeper_game.handle_mouse)
    sweeperlib.start()

if __name__ == "__main__":
    game_x_size = prompt_input("Give game size X: ", "Not a valid size")
    game_y_size = prompt_input("Give game size Y: ", "Not a valid size")
    user_n_mines = prompt_difficulty((game_x_size, game_y_size))

    game = Game(game_x_size, game_y_size)
    game.set_board_size(game.board_x_size*TILE_SPRITE_SIZE_PX, game.board_y_size*TILE_SPRITE_SIZE_PX)
    game.init_field_contents(n_mines=user_n_mines)
    main(game)
