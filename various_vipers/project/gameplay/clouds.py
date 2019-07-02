import logging
import random
from typing import List

import pygame as pg

from project.constants import (
    BG_CLOUDS_SCROLL_SPEED,
    CLOUD_LAYERS_BG,
    CLOUD_LAYERS_FG,
    FG_CLOUDS_SCROLL_SPEED,
    GameLayer,
    HEIGHT,
)

logger = logging.getLogger(__name__)


class Clouds(pg.sprite.DirtySprite):
    """Moving clouds sprite."""

    _layer: int

    image_pool: List[str]
    scroll_speed: int
    start_x: int
    start_y: int

    def __init__(self):
        super().__init__()
        self.dirty = 2

        self.image = random.choice(self.image_pool)
        self.image = pg.image.load(str(self.image)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.start_x
        self.rect.y = self.start_y

    def update(self) -> None:
        """Update is called every game tick."""
        self.rect.x += self.scroll_speed

    def move(self, vector: int) -> None:
        """Moves clouds by multiplying scroll speed by given vector."""
        self.rect.x += self.scroll_speed * vector


class CloudsFarther(Clouds):
    """Clouds that are farther back."""

    _layer: int = GameLayer.LAYER_CLOUDS_BG

    image_pool: List[str] = CLOUD_LAYERS_BG
    scroll_speed: int = BG_CLOUDS_SCROLL_SPEED
    start_x: int = 0
    start_y: int = int(HEIGHT // 4)


class CloudsCloser(Clouds):
    """Clouds that are closer to the screen."""

    _layer: int = GameLayer.LAYER_BLOUDS_FG

    image_pool: List[str] = CLOUD_LAYERS_FG
    scroll_speed: int = FG_CLOUDS_SCROLL_SPEED
    start_x: int = 0
    start_y: int = int(HEIGHT // 3)
