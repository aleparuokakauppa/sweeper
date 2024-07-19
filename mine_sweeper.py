import random

class GameState:
    game_field: list[list[str]] = []

    def __init__(self, grid_x_max = 0, grid_y_max = 0):
        for _ in range(grid_y_max):
            row: list[str] = []
            for _ in range(grid_x_max):
                # Initialize game with empty tiles
                row.append(' ')
            self.game_field.append(row)

    def init_mines(self, n_mines: int):
        if n_mines <= 0:
            # TODO more mines needed
            pass

        for _ in range(n_mines):
            (chosen_column, chosen_row) = random.choice(valid_tiles)
            field[chosen_row][chosen_column] = 'x'
            valid_tiles.remove((chosen_column, chosen_row))


def main():
    pass

if __name__ == "__main__":
    main()
