import sweeperlib
import random

state = {
    "field": []
}

def place_mines(field: list[list[str]],
                valid_tiles: list[tuple[(int, int)]],
                n_mines: int):
    """
    Places N mines to a field in random tiles.
    """
    for _ in range(n_mines):
        (chosen_column, chosen_row) = random.choice(valid_tiles)
        field[chosen_row][chosen_column] = 'x'
        valid_tiles.remove((chosen_column, chosen_row))

def draw_field():
    """
    A handler function that draws a field represented by a two-dimensional list
    into a game window. This function is called whenever the game engine requests
    a screen update.
    """
    sweeperlib.clear_window()
    sweeperlib.begin_sprite_draw()
    for row_index, row in enumerate(state["field"]):
        for col_index, _ in enumerate(row):
            sweeperlib.prepare_sprite(
                    state["field"][row_index][col_index],
                    col_index*40,
                    row_index*40)
    sweeperlib.draw_sprites()


def main():
    """
    Loads the game graphics, creates a game window and sets a draw handler for it.
    """
    
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(600, 400)
    sweeperlib.set_draw_handler(draw_field)
    sweeperlib.start()

if __name__ == "__main__":
    max_x = 15
    max_y = 10
    field = []
    for row in range(max_y):
        field.append([])
        for col in range(max_x):
            field[-1].append(" ")
    state["field"] = field
    available = []
    for x in range(max_x):
        for y in range(max_y):
            available.append((x, y))
    place_mines(state["field"], available, 10)
    main()
