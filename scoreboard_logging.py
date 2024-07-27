import datetime
import json

class ScoreboardLogger:
    """
    Reader and writer for scoreboard logging of the minesweeper game

    Uses a JSON file as a db, because of simplicity
    """
    DB_FILENAME = "game_scores.json"

    def __init__(self):
        pass

    def get_scoreboard_data(self) -> dict:
        """
        Used in the tkinter application to get printable
        scoreboard data.
        """
        with open(self.DB_FILENAME, 'r') as db_file:
            return json.load(db_file)

    def write_scoreboard_data(
        self,
        time_spent: int,
        difficulty: str,
        player_name: str
        ):
        """
        Used in the pyglet application to write
        scoreboard data.
        """
        score_data = {
            "time_spent": time_spent,
            "difficulty": difficulty,
            "player_name": player_name,
            "date_time": str(datetime.datetime.now())
        },
        with open(self.DB_FILENAME, '+a') as db_file:
            json.dump(score_data, db_file, indent=4)
