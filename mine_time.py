import random
import sweeperlib

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
    MAX_X = 15
    MAX_Y = 10
    field_local = []
    for row in range(MAX_Y):
        field_local.append([])
        for col in range(MAX_X):
            field_local[-1].append(" ")
    state["field"] = field_local
    available = []
    for x in range(MAX_X):
        for y in range(MAX_Y):
            available.append((x, y))
    place_mines(state["field"], available, 10)
    main()
