# =============================================================================
# Game Wrapper
# Author: Michael Sumaya
# =============================================================================
import pygame as gm
from pygame.sprite import GroupSingle

# Custom modules
import functions as gfn
from settings import Settings
from paddle import Paddle
from ball import Ball
from score import Scoring
from game_events import GameEvents

class MainGame():

    def __init__(self) -> None:
        gm.init()
        self.game_settings = Settings()
        gfn.block_events()

    def start(self):
        self.screen_width = self.game_settings.screen_width
        self.screen_height = self.game_settings.screen_height
        screen = gm.display.set_mode(
            size=(self.screen_width,
                  self.screen_height),
        )
        gm.display.set_caption(self.game_settings.game_name)
        screen.fill(self.game_settings.screen_bgcolor)

        # FPS control
        clock = gm.time.Clock()
        fps = self.game_settings.game_desiredfps

        # Load Paddle
        paddle = Paddle(screen, self.game_settings)
        paddle.to_center()

        # Load Ball
        ball = GroupSingle(Ball(screen, self.game_settings, paddle))

        # Load Targets
        targets, _ = gfn.create_targets(screen, self.game_settings)

        # Init Scoring system
        scoreboard = Scoring(screen, self.game_settings)

        # Custom event handler
        event_handler = GameEvents(screen)

        while True:
            # Keep at desired FPS
            clock.tick(fps)

            # Check Events
            gfn.check_events(
                screen,
                self.game_settings,
                paddle,
                ball,
                scoreboard,
                event_handler,
            )

            # Update on targets
            gfn.update_targets(
                ball,
                targets,
                scoreboard,
            )

            if len(targets) == 0:
                targets = gfn.new_level(
                    screen,
                    self.game_settings,
                    ball,
                )

            # FPS counter
            current_fps = clock.get_fps()

            # Refresh Loop
            gfn.update_screen(
                screen,
                self.game_settings,
                paddle,
                ball,
                targets,
                current_fps,
                scoreboard,
                event_handler,
            )
