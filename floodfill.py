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
        no_mines = True
        for dir_row, dir_col in directions:
            new_row, new_col = tile_y + dir_row, tile_x + dir_col
            # Check if new tile is inside
            if 0 <= new_row < len(planet) and 0 <= new_col < len(planet[0]):
                # Check if the neighbor hasn't been explored
                if planet[new_row][new_col] == ' ':
                    surrounding_tiles.append((new_col, new_row))
                # Check if the neighbor is a mine
                if planet[new_row][new_col] == 'x':
                    # don't add any neighbors to explore
                    no_mines = False
                    break
        if no_mines:
            to_explore.extend(surrounding_tiles)

def print_grid(grid: list[list[str]]) -> None:
    """
    Prints the grid given grid to stdout
    """
    print(" ", "- " * len(grid[0]))
    for row in grid:
        print("|", " ".join(row), "|")
    print(" ", "- " * len(grid[0]))

def main(planet: list[list[str]]):
    print_grid(planet)
    floodfill(planet, 1, 1)
    print_grid(planet)

planet = [
    [" ", " ", "x", " ", " "], 
    [" ", " ", "x", " ", " "], 
    ["x", "x", "x", "x", "x"], 
    [" ", " ", "x", " ", " "], 
    [" ", " ", "x", " ", " "], 
]

main(planet)
