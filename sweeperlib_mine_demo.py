from typing import List
import random
import sweeperlib

TILE_SIZE = 64

field = list[list[str]]

state = {
    "field": [],
}

state_visible = {
    "field": [],
}

mouse_buttons = {
    1: "left",
    2: "middle",
    4: "right",
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
    #state_visible["field"][row_index][col_index],
    item = field[0][1]
    for row_index, row in enumerate(state_visible["field"]):
        for col_index, _ in enumerate(row):
            sweeperlib.prepare_sprite(
                    field[row_index][col_index],
                    col_index*TILE_SIZE,
                    row_index*TILE_SIZE)
    sweeperlib.draw_sprites()


def handle_mouse(x_pos: int, y_pos: int, m_button: int, mod: int):
    """
    This function is called when a mouse button is clicked inside the game window.
    Prints the position and clicked button of the mouse to the terminal.
    """
    print(f"The {mouse_buttons[m_button]} mouse button was pressed at {x_pos}, {y_pos}")


def define_game_props():
    pass


def main():
    """
    Loads the game graphics, creates a game window and sets a draw handler for it.
    """
    sweeperlib.load_sprites("sprites")
    sweeperlib.create_window(600, 400)
    sweeperlib.set_draw_handler(draw_field)
    sweeperlib.set_mouse_handler(handle_mouse)
    sweeperlib.start()


if __name__ == "__main__":
    MAX_X = 15
    MAX_Y = 10
    field_local: List[List[str]] = [[' ' for _ in range(MAX_X)] for _ in range(MAX_Y)]
    #field_local: list[list[str]] = []
    #for row in range(MAX_Y):
        #for col in range(MAX_X):
            #field_local[row][col] = ' '
            #field_local[-1].append(" ")
    #state["field"] = field_local
    #state_visible["field"] = field_local
    field = field_local
    available = []
    for x in range(MAX_X):
        for y in range(MAX_Y):
            available.append((x, y))
    place_mines(field, available, 10)
    main()
