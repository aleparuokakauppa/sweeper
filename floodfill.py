def floodfill(planet: list[list[str]], x_pos: int, y_pos: int) -> None:
    """
    Marks previously unknown connected areas as safe, starting from the given
    x, y coordinates.
    """
    # If starting position has a mine, do nothing
    if planet[y_pos][x_pos] == 'x':
        return

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),         (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    to_explore: list[tuple[(int, int)]] = [(x_pos, y_pos)]

    while len(to_explore) > 0:
        # Get position and removes the last element of the list
        (tile_x, tile_y) = to_explore.pop()

        # Mark tile as safe
        planet[tile_y][tile_x] = '0'

        # Add surroundings into to_explore if unexplored
        surrounding_tiles: list[tuple[(int, int)]] = []
        for dir_row, dir_col in directions:
            new_row, new_col = tile_y + dir_row, tile_x + dir_col
            # Check if new tile is inside
            if 0 <= new_row < len(planet) and 0 <= new_col < len(planet[0]):
                # Check if the neighbor hasn't been explored and is safe
                if planet[new_row][new_col] == ' ':
                    surrounding_tiles.append((new_col, new_row))
        to_explore.extend(surrounding_tiles)

def print_grid(grid: list[list[str]]) -> None:
    """
    Prints the grid given grid to stdout
    """
    print(" ", "- " * len(grid[0]))
    for row in grid:
        print("|", " ".join(row), "|")
    print(" ", "- " * len(grid[0]))

def main(planet_input: list[list[str]]):
    """
    Loads the game graphics, creates a game window, and sets a draw handler
    """
    print_grid(planet_input)
    floodfill(planet_input, 0, 4)
    print_grid(planet_input)

planet_in = [
    [' ', ' ', ' ', ' ', 'x', 'x'],
    [' ', 'x', ' ', 'x', ' ', ' '],
    [' ', 'x', ' ', ' ', ' ', 'x'],
    [' ', ' ', 'x', 'x', ' ', ' '],
    ['x', 'x', 'x', 'x', ' ', ' '],
    ['x', ' ', 'x', ' ', 'x', 'x'],
    ['x', 'x', ' ', ' ', ' ', ' ']
]

main(planet_in)
