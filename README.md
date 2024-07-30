## Mine sweeper game made with pyglet and sweeperlib helper library
Simple mine sweeper implementation for Elementary Programming class

The program keeps track of previous games and their details with a scoreboard that is printed when the game is started

The game starts with an initial CLI for game initialization and scoreboard logging

The game itself runs in a GUI with pretty sprites sourced from 
`https://www.spriters-resource.com/pc_computer/minesweeper/sheet/19849/`
(Availability checked on 30.07.2024)
resized to 64x64 pixels

The program uses a single JSON file for a database for simplicity

This implementation uses the timer as a countdown, rather than a time counter

The main problem with the game is that it doesn't give a pleasant initial starting position.
One might lose on the first click.

# Usage
- Install dependencies 
    ```bash
    pip install pyglet
    ```
- Start the game
    ```bash
    python main.py
    ```


# External dependencies:
- `pyglet`
- included `sweeperlib.py` library

# Screenshot
![Screenshot](https://raw.githubusercontent.com/aleparuokakauppa/sweeper/master/images/mine_sweeper_screenshot.jpg?raw=true)
