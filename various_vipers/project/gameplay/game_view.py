import logging

import pygame as pg

from project.constants import Color, GameLayer, HEIGHT, WIDTH
from .period import PeriodFuture, PeriodMedieval, PeriodModern


logger = logging.getLogger(__name__)


class GameView(pg.sprite.LayeredDirty):
    """GameView hold the information about all things related to the main game."""

    def __init__(self, difficulty: int = 0):
        """
        Initializer for GameView class.

        difficulty - 0, 1, 2. Difficulty increases with number.
        """

        super().__init__()

        if difficulty == 0:
            self.period = PeriodMedieval()
        elif difficulty == 1:
            self.period = PeriodModern()
        elif difficulty == 2:
            self.period = PeriodFuture()
        else:
            raise TypeError(f"Unknown difficulty level passed: {difficulty}")

        self.add(self.GameBackground())

    def update(self) -> None:
        """Update gets called every game tick."""
        self.add(self.period)
        self.period.update()
        super().update()

    class GameBackground(pg.sprite.DirtySprite):
        """Background filling whole game screen."""

        _layer: int = GameLayer.LAYER_BACKGROUND

        def __init__(self):
            super().__init__()
            self.dirty = 1

            self.image = pg.Surface((WIDTH, HEIGHT))
            self.image.fill(Color.sky)
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = 0
