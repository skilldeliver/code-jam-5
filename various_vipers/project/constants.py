"""All game contstants."""
import logging

from pathlib import PurePath


FPS = 60

WIDTH = 1200
HEIGHT = 700

LOG_LEVEL = logging.DEBUG


class Color:
    """Represent RGB color value."""

    black = (0, 0, 0)

    white = (255, 255, 255)

    red = (255, 0, 0)


PATH_PROJECT = PurePath(__file__).parent

PATH_BACKGROUNDS = PurePath(PATH_PROJECT).joinpath("assets/images/background")

# Game assets

# Background images
GAME_BG_DESERT = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorDesert.png")
GAME_BG_FALL = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorFall.png")
GAME_BG_FOREST = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorForest.png")
GAME_BG_GRASS = PurePath(PATH_BACKGROUNDS).joinpath("backgroundColorGrass.png")
