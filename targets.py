# =============================================================================
# Targets
# Author: Michael Sumaya
# =============================================================================
import pygame as gm
from pygame.sprite import Group, Sprite
from random import randint
from settings import Settings


class Target(Sprite):
    """Target Sprites control
    - Non-moving targets
    """

    def __init__(
            self,
            screen: gm.Surface,
            settings: Settings,
            *groups: Group,
    ) -> None:
        super().__init__(*groups)
        self.screen = screen
        self.settings = settings

        # Shape
        self.width = self.settings.target_width
        self.height = self.settings.target_height
        self.rect = gm.Rect(0, 0, self.width, self.height)
        self.color = (randint(1, 255),
                      randint(1, 255),
                      randint(1, 255))

    def move(self, xpos, ypos):
        self.rect.x = xpos
        self.rect.y = ypos

    def update(self, *args: any, **kwargs: any) -> None:
        """Draw on screen"""
        gm.draw.rect(
            self.screen,
            self.color,
            self.rect,
        )
        return super().update(*args, **kwargs)

    def __str__(self) -> str:
        stats = f"Target: {self.rect.top, self.rect.right, self.rect.bottom, self.rect.left}"
        return stats
