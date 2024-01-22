# =============================================================================
# Scoring System
# Author: Michael Sumaya
# =============================================================================
import pygame as gm
import pygame.freetype as ftype
import pickle

# Custom modules
from settings import Settings


class Scoring():
    """Scoring system"""

    FILE_HIGHSCORE = "highscore.pickle"
    WRITE_TYPE = "wb"
    READ_TYPE = "rb"

    def __init__(
        self,
        screen: gm.Surface,
        settings: Settings,
    ) -> None:
        self.screen = screen
        self.settings = settings.Scoreboard()

        # Initial Values
        self.score_current = 0
        self.file_high = self._get_highscore()
        self.score_high = self.file_high
        self.reset_combo_point()

    def _get_highscore(self) -> int:
        try:
            with open(self.FILE_HIGHSCORE, self.READ_TYPE, -1) as savefile:
                highscore = pickle.load(savefile)
        except:
            highscore = 0
        return highscore

    def _save_highscore(self) -> bool:
        self.update_filehigh()
        try:
            with open(self.FILE_HIGHSCORE, self.WRITE_TYPE, -1) as savefile:
                pickle.dump(self.file_high, savefile, -1)
            return True
        except:
            return False

    def _display_score(
        self,
        score: str,
        pos: tuple,
        color: any,
    ) -> None:
        scoreboard_font = ftype.Font(self.settings.Font.path,
                                     self.settings.Font.size,)
        scoreboard_font.render_to(
            self.screen,
            pos,
            score,
            fgcolor=color,
        )

    def update(self) -> None:
        """Refresh scoreboard"""
        # Current Score
        self._display_score(
            "Current Score:",
            self.settings.pos_current_label,
            self.settings.Font.color_current,
        )
        self._display_score(
            f"{self.score_current}",
            self.settings.pos_current_value,
            self.settings.Font.color_current,
        )
        # High Score
        self._display_score(
            "High Score:",
            self.settings.pos_highscore_label,
            self.settings.Font.color_high,
        )
        self._display_score(
            f"{self.score_high}",
            self.settings.pos_highscore_value,
            self.settings.Font.color_high,
        )

    def add_normal(self) -> None:
        """Add normal point to current score"""
        self.score_current += self.settings.point_normal

    def add_combo(self) -> None:
        """Add combo point to current score"""
        self.score_current += self.increase_combo_point()

    def increase_combo_point(self) -> int:
        """Increase combo point if more boxes hit"""
        self.point_combo += self.settings.point_combo
        return self.point_combo

    def reset_score(self) -> None:
        """Reset current score on game over"""
        self.score_current = 0

    def reset_combo_point(self) -> None:
        """Reset combo point when ball hits paddle"""
        self.point_combo = 0

    def update_filehigh(self) -> None:
        """Store high score for saving"""
        if self.score_current > self.file_high:
            self.file_high = self.score_current

    def update_scoreboardhigh(self) -> bool:
        """Update high score in scoreboard"""
        if self.score_current > self.score_high:
            self.score_high = self.score_current
            return True
        else:
            return False
