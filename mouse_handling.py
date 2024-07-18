import sweeperlib

mouse_buttons = {
    1: "left",
    2: "middle",
    4: "right",
}

def handle_mouse(x_pos: int, y_pos: int, m_button: int, mod: int):
    """
    This function is called when a mouse button is clicked inside the game window.
    Prints the position and clicked button of the mouse to the terminal.
    """
    print(f"The {mouse_buttons[m_button]} mouse button was pressed at {x_pos}, {y_pos}")

def main():
    """
    Creates a game window and sets a handler for mouse clicks.
    Starts the game.
    """
    sweeperlib.create_window()
    sweeperlib.set_mouse_handler(handle_mouse)
    sweeperlib.start()

if __name__ == "__main__":
    main()
