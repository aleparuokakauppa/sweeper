import datetime
import constants
import json

class ScoreboardLogger:
    """
    Reader and writer for scoreboard logging of the minesweeper game

    Uses a JSON file as a db, because of simplicity
    """
    DB_FILENAME = "game_scores.json"

    def __init__(self):
        pass

    def get_scoreboard_data(self):
        """
        Used in the tkinter application to get printable
        scoreboard data.
        """
        try:
            with open(self.DB_FILENAME, 'r') as db_file:
                return json.load(db_file)
        except FileNotFoundError:
            # File not initialized
            return []

    def write_scoreboard_data(
        self,
        player_name: str,
        difficulty: int,
        time_spent: int,
        game_size_x: int,
        game_size_y: int
        ):
        """
        Used in the pyglet application to write
        scoreboard data.

        :params str player_name: Player name
        :params int difficulty: Difficulty identifier according to `constants.py` (easy 1, medium 2, or hard 3)
        :params int time_spent: How much time was spent during a game
        :params int game_size_x: Size of game x-axis
        :params int game_size_y: Size of game y-axis
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

        score_data = {
            "player_name": player_name,
            "difficulty": difficulty_str,
            "time_spent": time_spent,
            "date_time": dt.strftime("%H:%M %Y/%m/%d"),
            "game_size_x": game_size_x,
            "game_size_y": game_size_y
        },
        
        existing_data.extend(score_data)

        with open(self.DB_FILENAME, 'w') as db_file:
            json.dump(existing_data, db_file)
