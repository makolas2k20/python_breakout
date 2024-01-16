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


class MainGame():

    def __init__(self) -> None:
        pass

    def start(self):
        gm.init()
        game_settings = Settings()
        self.screen_width = game_settings.screen_width
        self.screen_height = game_settings.screen_height
        screen = gm.display.set_mode(
            size=(self.screen_width,
                  self.screen_height),
        )
        gm.display.set_caption(game_settings.game_name)
        screen.fill(game_settings.screen_bgcolor)

        # FPS control
        clock = gm.time.Clock()
        fps = game_settings.game_desiredfps

        # Load Paddle
        paddle = Paddle(screen, game_settings)
        paddle.to_center()

        # Load Ball
        ball = GroupSingle(Ball(screen, game_settings, paddle))

        # Load Targets
        targets, _ = gfn.create_targets(screen, game_settings)

        while True:
            # Keep at desired FPS
            clock.tick(fps)

            # Check Events
            gfn.check_events(
                screen,
                game_settings,
                paddle,
                ball,
            )

            # Update on targets
            gfn.update_targets(
                ball,
                targets,
            )

            if len(targets) == 0:
                targets, bottom_y = gfn.create_targets(screen, game_settings)
                ball.sprite.move(ball.sprite.rect.centerx, bottom_y)

            # FPS counter
            current_fps = clock.get_fps()

            # Refresh Loop
            gfn.update_screen(
                screen,
                game_settings,
                paddle,
                ball,
                targets,
                current_fps,
            )
