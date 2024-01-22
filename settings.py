# =============================================================================
# Settings
# Author: Michael Sumaya
# =============================================================================
import pygame as gm
from pathlib import Path


class Settings():
    """Game Configurations"""

    def __init__(self) -> None:
        # Game details
        self.game_name = 'Breakout Clone by Michael Sumaya'
        self.game_desiredfps = 60
        self.show_fps = True
        self.save_screenshot = False
        self.game_on = False

        # Screen
        self.screen_width = 600
        self.screen_height = 800
        self.screen_bgcolor = 'black'

        # Playing field
        self.field_xpos = 0
        self.field_ypos = 100
        self.field_width = self.screen_width
        self.field_height = self.screen_height - self.field_ypos
        self.field_rect = (self.field_xpos,
                           self.field_ypos,
                           self.field_width,
                           self.field_height)
        self.field_border_color = 'white'
        self.field_border_width = 1

        # Paddle
        self.paddle_width = 100
        self.paddle_height = 10
        self.paddle_speed = 10
        self.paddle_color = 'white'
        self.paddle_offset_from_bottom = 150

        # Ball
        self.ball_width = 20
        self.ball_height = 20
        self.ball_speed = 8
        self.ball_color = 'white'
        self.ball_copy_target_color = True

        # Targets
        self.target_rows = 5
        self.target_width = 50
        self.target_height = 20

        # Key Events
        self.event_key_left = (
            gm.K_LEFT,
            gm.K_a,
        )
        self.event_key_right = (
            gm.K_RIGHT,
            gm.K_d,
        )

    class Scoreboard():
        """Scoreboard settings"""
        pos_current_label = (310, 10)
        pos_current_value = (310, 40)
        pos_highscore_label = (10, 10)
        pos_highscore_value = (10, 40)
        point_normal = 1
        point_combo = 1

        class Font():
            """Scoreboard - Font settings"""
            path = str(Path.absolute(
                Path(".", "fonts", "courier10pitch.pfb")).resolve())
            size = 24
            color_current = 'gray'
            color_high = 'yellow'

    class Prompt():
        """Prompt message settings"""
        COLOR_WARNING = 'yellow'
        COLOR_ERROR = 'red'
        COLOR_NORMAL = 'white'
        font = str(Path.absolute(
            Path(".", "fonts", "courier10pitch.pfb")).resolve())
        size = 18

    class Life():
        """Life settings"""
        pos_label = (10, 70)
        pos_value = (100, 70)
        font = str(Path.absolute(
            Path(".", "fonts", "courier10pitch.pfb")).resolve())
        font_size = 24
        color = 'red'
        max_life = 5
        symbol = '§'