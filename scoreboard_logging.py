"""
Handles all interactions with the scoreboard DB

Includes helper functions for reading and writing
"""

import datetime
import json
import constants

class ScoreboardLogger:
    """
    Reader and writer for scoreboard logging of the minesweeper game

    Uses a JSON file as a db for simplicity
    """
    DB_FILENAME = "game_scores.json"

    def get_scoreboard_data(self):
        """
        Used in the tkinter application to get printable
        scoreboard data.
        """
        try:
            with open(self.DB_FILENAME, 'r', encoding="UTF-8") as db_file:
                return json.load(db_file)
        except FileNotFoundError:
            return []

    def write_scoreboard_data(
        self,
        player_name: str,
        difficulty: int,
        turns_used: int,
        time_spent: int,
        mines_left: int,
        game_size: tuple[int, int]
        ):
        """
        Used in the pyglet application to write
        scoreboard data.

        :params str player_name: Player name
        :params int difficulty: Difficulty identifier found in`constants.py`
        :params int turns_used: How many turns were played before game ended
        :params int time_spent: How much time was spent during a game
        :params int mines_left: How many mines were left after game ended
        :params tuple[int, int] game_size: Game size in (x_size, y_size) format
        """
        existing_data = self.get_scoreboard_data()

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
            "mines_left": mines_left,
            "time": dt.strftime("%H:%M"),
            "ymd": dt.strftime("%Y/%m/%d"),
            "game_size_x": game_size[0],
            "game_size_y": game_size[1]
        },)

        existing_data.extend(score_data)

        with open(self.DB_FILENAME, 'w', encoding='UTF-8') as db_file:
            json.dump(existing_data, db_file)

    def print_scores(self):
        """
        Prints the scoreboard to stdout
        """
        records: list[dict] = []
        for record in self.get_scoreboard_data():
            records.append(record)
            records = sorted(records, key=lambda record: record["time_spent"])

        if len(records) != 0:
            print("\n--    Scoreboard    --")
            for record in records:
                print(f"{record["player_name"]} @ {record["time"]} {record["ymd"]}\n"
                      f"{record["difficulty"]} {record["game_size_x"]}x{record["game_size_y"]}\n"
                      f"game lasted for {record["time_spent"]}s\n"
                      f"made {record["turns_used"]} turns\n")
        else:
            print("\nNo previous scores\n")
