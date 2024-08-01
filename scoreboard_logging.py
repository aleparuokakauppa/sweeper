"""
Reader and writer for scoreboard logging of the minesweeper game

Uses a JSON file as a db for simplicity
"""

import datetime
import json
import constants

DB_FILENAME = "game_scores.json"

def get_scoreboard_data():
    """
    Used in the tkinter application to get printable
    scoreboard data.
    """
    try:
        with open(DB_FILENAME, 'r', encoding="UTF-8") as db_file:
            return json.load(db_file)
    except FileNotFoundError:
        return []

def write_scoreboard_data(
    player_name: str,
    difficulty: int,
    turns_used: int,
    time_spent: int,
    to_reveal: int,
    game_size: tuple[int, int]
    ):
    """
    Used in the pyglet application to write
    scoreboard data.

    :params str player_name: Player name
    :params int difficulty: Difficulty identifier found in`constants.py`
    :params int turns_used: How many turns were played before game ended
    :params int time_spent: How much time was spent during a game
    :params int to_reveal: How many tiles were to be revealed
    :params tuple[int, int] game_size: Game size in (x_size, y_size) format
    """
    existing_data = get_scoreboard_data()

    dt = datetime.datetime.now()

    difficulty_str = ""
    match difficulty:
        case constants.DIFFICULTY_EASY:
            difficulty_str = "Easy"
        case constants.DIFFICULTY_MEDIUM:
            difficulty_str = "Medium"
        case constants.DIFFICULTY_HARD:
            difficulty_str = "Hard"
        case constants.DIFFICULTY_CUSTOM:
            difficulty_str = "Custom"

    score_data = ({
        "player_name": player_name,
        "difficulty": difficulty_str,
        "time_spent": time_spent,
        "turns_used": turns_used,
        "to_reveal": to_reveal,
        "time": dt.strftime("%H:%M"),
        "ymd": dt.strftime("%Y/%m/%d"),
        "game_size_x": game_size[0],
        "game_size_y": game_size[1]
    },)

    existing_data.extend(score_data)

    with open(DB_FILENAME, 'w', encoding='UTF-8') as db_file:
        json.dump(existing_data, db_file)

def print_scores():
    """
    Prints the scoreboard to stdout
    """
    records: list[dict] = []
    for record in get_scoreboard_data():
        records.append(record)
        records = sorted(records, key=lambda record: record["to_reveal"])

    if len(records) != 0:
        print("\n--    Scoreboard    --")
        for record in records:
            win_status = "Win"
            if record["to_reveal"] != 0:
                win_status = f"Loss, {record["to_reveal"]} tiles left unexplored"
            print(f"{record["player_name"]} @ {record["time"]} {record["ymd"]}\n"
                    f"{win_status}\n"
                    f"{record["difficulty"]} {record["game_size_x"]}x{record["game_size_y"]}\n"
                    f"game lasted for {record["time_spent"]}s\n"
                    f"made {record["turns_used"]} turns\n")
    else:
        print("\nNo previous scores\n")
