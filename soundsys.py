# =============================================================================
# Sound System Class
# Author: Michael Sumaya
# =============================================================================
from pygame import mixer
from settings import Settings


class SoundSystem():
    """Sound System Handler"""

    def __init__(
            self,
            settings: Settings,
    ) -> None:
        """Init settings"""
        self.mixer = mixer
        self.settings = settings.assets
        self.mixer.pre_init(buffer=1024)
        self.mixer.init(buffer=1024)

        # Load sound files
        self.paddle = self.mixer.Sound(self.settings.SOUND_PADDLE)
        self.target = self.mixer.Sound(self.settings.SOUND_TARGET)
        self.bgm = self.mixer.music
        self.bgm.load(self.settings.BG_MUSIC)

    def play_paddle(self):
        self.paddle.play()

    def play_target(self):
        self.target.play()

    def play_bgm(self):
        if not self.bgm.get_busy():
            self.bgm.play(-1)

    def quit(self):
        self.mixer.stop()
        self.mixer.quit()
