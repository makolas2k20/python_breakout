# =============================================================================
# Python Breakout Game Clone using PyGame
# Author: Michael Sumaya
# =============================================================================
from game import MainGame

breakoutgame = MainGame()

if __name__ == "__main__":
    # Update settings file dynamically by changing - breakoutgame.game_settings
    breakoutgame.start()
