# Mine sweeper game made with pyglet and sweeperlib helper library
Simple mine sweeper implementation for Elementary Programming class

The program keeps track of previous games and their details with a scoreboard that is printed when the game is started

The game starts with an initial CLI for game initialization and scoreboard logging

The game itself runs in a GUI with pretty sprites sourced from [here](https://www.spriters-resource.com/pc_computer/minesweeper/sheet/19849/)

Included font sourced from [here](https://www.nerdfonts.com/font-downloads)

The program uses a single JSON file for a database for simplicity

This implementation uses the timer as a countdown, rather than a time counter

The main problem with the game is random mine generation.
Mines are initialized completely randomly and can result in
boring games. Also the user can fail on the first click.

Program tested on Arch Linux and MacOS

## Usage
- Install dependencies 
    ```bash
    pip install pyglet
    ```
- Start the game
    ```bash
    python main.py
    ```

## External dependencies:
- `pyglet < v2.0`
  Tested on v1.5.29

## Screenshot
![Screenshot](https://raw.githubusercontent.com/aleparuokakauppa/sweeper/master/resources/images/mine_sweeper_screenshot.jpg?raw=true)
