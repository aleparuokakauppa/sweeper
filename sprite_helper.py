import sweeperlib
import game_constants
from game_state import Game

class Sprites:
    game_state: Game

    def __init__(self, game_state_instance: Game):
        self.game_state = game_state_instance

    def draw_screen(self):
        """
        Main-game draw field handler for the pyglet program.
        Draws sprites based on the `game_board` string contents
        of each tile with additional draw logic
        """
        sweeperlib.clear_window()
        sweeperlib.draw_background()
        sweeperlib.begin_sprite_draw()

        # Prepare tile sprites
        for y_index, row in enumerate(self.game_state.game_board):
            for x_index, tile_content in enumerate(row):
                draw_key = " "
                if (x_index, y_index) in self.game_state.explored_tiles:
                    draw_key = tile_content

                if (x_index, y_index) in self.game_state.flagged_tiles:
                    draw_key = 'f'
                    if (self.game_state.game_over or self.game_state.win) and tile_content != 'x':
                        draw_key = 'F'

                if self.game_state.game_over and tile_content == 'x':
                    draw_key = 'x'
                    if (x_index, y_index) in self.game_state.flagged_tiles:
                        draw_key = 'f'

                sweeperlib.prepare_sprite(
                            draw_key,
                            x_index * game_constants.TILE_SPRITE_SIZE_PX,
                            y_index * game_constants.TILE_SPRITE_SIZE_PX)

        # Prepare sprites for timer
        timer_str = f"{self.game_state.remaining_time:03}"
        for pos, timer_char in enumerate(timer_str):
            sweeperlib.prepare_sprite(
                    f"display-{timer_char}",
                    (self.game_state.board_size_px[0] - 3 * game_constants.TILE_SPRITE_SIZE_PX)
                    + pos * game_constants.TILE_SPRITE_SIZE_PX - 4,
                    self.game_state.board_size_px[1] + 11)

        # Prepare sprites for mine counter
        n_mines_left: int = self.game_state.n_mines - len(self.game_state.flagged_tiles)
        n_mines_left_str: str = f"{n_mines_left:03}"
        for pos, n_mines_left_char in enumerate(n_mines_left_str):
            sweeperlib.prepare_sprite(
                    f"display-{n_mines_left_char}",
                    pos * game_constants.TILE_SPRITE_SIZE_PX + 4,
                    self.game_state.board_size_px[1] + 11)

        # Prepare sprite for status face
        face_draw_key = "face-smiley"
        if self.game_state.game_over:
            face_draw_key = "face-lose"
        if self.game_state.win:
            face_draw_key = "face-win"
        sweeperlib.prepare_sprite(
                face_draw_key,
                round(self.game_state.board_size_px[0]/2) - game_constants.FACE_SPRITE_SIZE_PX/2,
                self.game_state.board_size_px[1] + 18
                )
        sweeperlib.draw_sprites()

        if self.game_state.win or self.game_state.game_over:
            sweeperlib.begin_sprite_draw()
            sweeperlib.prepare_sprite(
                    "end-plate",
                    round(self.game_state.board_size_px[0]/2) - 192,
                    round(self.game_state.board_size_px[1]/2)
                    )
            sweeperlib.draw_sprites()

            win_msg = "You lost!"
            msg_color = (255, 0, 0, 255)
            if self.game_state.win:
                win_msg = "You win!"
                msg_color = (0, 255, 0, 255)

            sweeperlib.draw_text(
                    win_msg,
                    (round(self.game_state.board_size_px[0]/2) - 174,
                    round(self.game_state.board_size_px[1]/2) + 82),
                    color=msg_color,
                    size=48
                    )
            sweeperlib.draw_text(
                    "Click to return.",
                    (round(self.game_state.board_size_px[0]/2) - 174,
                    round(self.game_state.board_size_px[1]/2) + 48),
                    size=24
                    )

    def update_timer(self, _):
        """
        Draws the timer sprites onto the game window and updates timer
        in game logic. Updates `game_over` if timer reaches zero.

        Used by `sweeperlib.set_interval_handler`
        """
        if self.game_state.remaining_time > 0:
            if not self.game_state.game_over and not self.game_state.win:
                self.game_state.remaining_time -= 1

        if self.game_state.remaining_time <= 0:
            self.game_state.game_over = True

