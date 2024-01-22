# =============================================================================
# Ball Sprite + Physics
# Author: Michael Sumaya
# =============================================================================
import pygame as gm
from pygame.sprite import Group, Sprite
from settings import Settings
from paddle import Paddle
from life import Life


class Ball(Sprite):
    """Ball sprite controls"""

    def __init__(
            self,
            screen: gm.Surface,
            settings: Settings,
            paddle: Paddle,
            *groups: Group,
    ) -> None:
        """Ball Init"""
        super().__init__(*groups)
        self.screen = screen
        self.settings = settings

        # Load Settings
        self.screen_rect = screen.get_rect()
        self.width = self.settings.ball_width
        self.height = self.settings.ball_height
        self.speed = self.settings.ball_speed
        self.color = self.settings.ball_color
        self.rect = gm.Rect(0, 0, self.width, self.height)
        self.centerx = (paddle.rect.centerx - (self.width * 5))
        self.centery = (paddle.rect.centery - (self.height * 5))
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        # Movement flag
        self.isDropped = False
        self.paddle_hit = False
        # 1 = right, -1 = left
        self.dirx = 1
        # -1 = up, 1 = down
        self.diry = 1

    def bounce_x(self) -> None:
        self.dirx *= -1

    def bounce_y(self) -> None:
        self.diry *= -1

    def check_collision(
            self,
            paddle: Paddle,
    ) -> bool:
        HIT_THRESHOLD = self.speed
        paddle_hit = self.rect.colliderect(paddle.rect)
        if not self.isDropped:
            if (self.rect.right >= self.screen_rect.right
                    or self.rect.left <= 0):
                self.bounce_x()
            if (self.rect.top <= self.settings.field_ypos
                    or (abs(self.rect.bottom - paddle.rect.top) <= HIT_THRESHOLD)
                    and paddle_hit):
                self.bounce_y()

            self.centerx += (self.speed * self.dirx)
            self.centery += (self.speed * self.diry)

            self.rect.centerx = self.centerx
            self.rect.centery = self.centery
        else:
            # Move ball back to center of screen, not moving
            self.ball_dropped()
        return paddle_hit

    def ball_dropped(self) -> None:
        """Reset ball position:
        Center of screen,
        Not moving
        """
        self.move(self.screen_rect.centerx, self.screen_rect.centery)

    def draw(self) -> None:
        gm.draw.ellipse(
            self.screen,
            self.color,
            self.rect,
        )

    def move(
            self,
            cx: int,
            cy: int,
    ) -> None:
        self.centerx = cx
        self.centery = cy
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def update(
            self,
            paddle: Paddle,
            life: Life,
    ) -> None:
        # Collisions
        self.paddle_hit = self.check_collision(paddle)

        # Check if ball has dropped below screen
        if (self.rect.bottom >= self.screen_rect.bottom
                and not self.isDropped):
            self.isDropped = True
            life.decrease()

        # Draw new position
        self.draw()

    def __str__(self) -> str:
        stats = f"Ball: Pos({self.centerx}, {self.centery})| Speed({self.speed})"
        return stats
