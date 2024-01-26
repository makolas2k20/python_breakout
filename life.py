# =============================================================================
# Life Class
# Author: Michael Sumaya
# =============================================================================
import pygame as gm
import pygame.freetype as ftype
from settings import Settings


class Life():
    """Life handler"""

    def __init__(
            self,
            screen: gm.Surface,
            settings: Settings,
    ) -> None:
        """Initialize class"""
        self.screen = screen
        self.settings = settings.life

        # Init values
        self.reset()

    def __str__(self) -> str:
        """Return current life as string"""
        return f"Life remaining: {self.count}"

    def reset(self) -> None:
        """Reset current value to initial value"""
        self.count = self.settings.max_life

    def decrease(self) -> int:
        """Decrease life by 1 and return current value"""
        self.count -= 1
        return self.count

    def update(self) -> None:
        """Update screen details"""
        life_label = ftype.Font(self.settings.font,
                                self.settings.font_size,)

        life_label.render_to(
            self.screen,
            self.settings.pos_label,
            "Life: ",
            fgcolor=self.settings.color,
        )

        if self.settings.use_image:
            # Use image to display life
            heart_rect = self.settings.life_rect
            heart_rect.topleft = self.settings.pos_value
            for _ in range(self.count):
                self.screen.blit(
                    self.settings.life_img,
                    heart_rect,
                )
                heart_rect.left += heart_rect.width
        else:
            # Use text to display life
            life_txt = ftype.SysFont(None,
                                     self.settings.font_size,)
            current_life = ""
            for _ in range(self.count):
                current_life += self.settings.symbol
            life_txt.render_to(
                self.screen,
                self.settings.pos_value,
                current_life,
                fgcolor=self.settings.color,
            )
