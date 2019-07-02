import logging
import random

import pygame as pg
from pygame.image import load
from pygame.transform import flip, scale

from project.constants import HEIGHT, INDICATOR_ARROW, INDICATOR_WIDTH, WIDTH, GameLayer
from .tile import Tile


logger = logging.getLogger(__name__)


class Indicator(pg.sprite.DirtySprite):
    """Indicator to show the way towards task."""

    _layer: int = GameLayer.LAYER_INDICATORS

    # Indicator arrow pulses (moving x coordinates)
    max_x_offset: int = 30  # max x pulse offset from initial position
    current_offset: int = 0
    pulse_speed: int = 3
    pulse_direction: int = 1

    def __init__(self, tile: Tile, is_left: bool = True):
        super().__init__()
        self.dirty = 2

        self.tile = tile
        self.is_left = is_left

        self.image = load(str(INDICATOR_ARROW)).convert_alpha()
        scale_percent = INDICATOR_WIDTH / self.image.get_width()
        new_height = int(self.image.get_height() * scale_percent)
        self.image = scale(self.image, (INDICATOR_WIDTH, new_height))
        self.image = flip(self.image, not self.is_left, False)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        self.pulse_direction = 1

        self.__update_pos()

    def update(self) -> None:
        """Update is called every game tick."""
        self.__pulse()

    def flip(self, to_left: bool) -> None:
        """Set new position (left or right) for the indicator."""
        if self.is_left != to_left:
            self.is_left = to_left
            self.image = flip(self.image, True, False)
            self.__update_pos()

    def __update_pos(self) -> None:
        """
        Update/Set starting x and y positions of indicator.
        
        Should be called when indicator is spawned or is moved to mew position on screen.
        """
        self.x = 0 if self.is_left else WIDTH - self.image.get_width()
        self.rect.y = random.randint(0, int(HEIGHT * 0.5))

    def __pulse(self) -> None:
        """Pulsing effect - moves indicator x position in and out."""
        # Limit pulse offset
        if self.current_offset >= self.max_x_offset:
            self.pulse_direction = -1
        elif self.current_offset <= 0:
            self.pulse_direction = 1

        self.current_offset += self.pulse_speed * self.pulse_direction
        offset = self.current_offset if self.is_left else -self.current_offset
        self.rect.x = self.x + offset
