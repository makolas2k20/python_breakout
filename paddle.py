# =============================================================================
# Paddle + Physics
# Author: Michael Sumaya
# =============================================================================
import pygame as gm
from pygame.sprite import Group, Sprite
from settings import Settings


class Paddle(Sprite):
    """Paddle sprite controls"""

    def __init__(
            self,
            screen: gm.Surface,
            settings: Settings,
            *groups: Group,
    ) -> None:
        super().__init__(*groups)
        self.screen = screen
        self.settings = settings

        # Load settings
        self.width = settings.paddle_width
        self.height = settings.paddle_height
        self.speed = settings.paddle_speed

        # Draw paddle and reposition to center of playing field
        self.screen_rect = self.screen.get_rect()
        self.rect = gm.Rect(0, 0, self.width, self.height)
        self.xpos = self.screen_rect.centerx
        self.ypos = (self.screen_rect.bottom
                     - self.settings.paddle_offset_from_bottom)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.ypos
        self.speed = self.settings.paddle_speed

        # Movement controls
        self.ismoving_left = False
        self.ismoving_right = False

    def to_center(self):
        """Return to center of screen"""
        self.xpos = self.screen_rect.centerx
        self.rect.centerx = self.xpos

    def draw_paddle(self):
        gm.draw.rect(
            self.screen,
            self.settings.paddle_color,
            self.rect,
        )

    def update(self) -> None:
        """Update paddle based on movement flag"""
        if (self.ismoving_right
                and self.rect.right < self.screen_rect.right):
            self.xpos += self.speed
        if (self.ismoving_left
                and self.rect.left > 0):
            self.xpos -= self.speed

        self.rect.centerx = self.xpos

        self.draw_paddle()

    def __str__(self) -> str:
        stats = f"Paddle: {self.xpos, self.ypos}"
        return stats