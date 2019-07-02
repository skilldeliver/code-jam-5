from __future__ import annotations

import logging
from typing import Optional, TYPE_CHECKING

import pygame as pg
from pygame.image import load
from pygame.transform import scale

from project.constants import GameLayer, TILE_WIDTH

if TYPE_CHECKING:
    # Avoid cyclic imports
    # https://stackoverflow.com/a/39757388
    from .task import Task


logger = logging.getLogger(__name__)


class Tile(pg.sprite.DirtySprite):
    """
    Generic class for Earth tiles.

    Class holds information about tile type, its image, and available actions.
    """

    _layer: int = GameLayer.LAYER_TILES

    # Current task associated with this tile
    # Tiles with tasks have different appearance
    task: Optional[Task] = None

    # Variables to handle tile transformation
    max_scale: float = 1.5
    current_scale: float = 1
    breathing_speed: float = 0.025  # how much to scale on each game tick
    breathing_direction: int = 1  # 1 -> outwards, -1 -> inwards

    def __init__(self, image: str):
        super().__init__()
        self.dirty = 2

        self.image = load(image).convert_alpha()

        scale_percent = TILE_WIDTH / self.image.get_width()
        new_height = int(self.image.get_height() * scale_percent)

        # scale image based on game screen size
        self.image = scale(self.image, (TILE_WIDTH, new_height))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self) -> None:
        """Update is called every game tick."""
        self.__breathe()

    @property
    def image(self) -> pg.Surface:
        """
        Returns image of this tile.

        Method transforms the image based on if it is a task or not.
        """
        transformed_image = self._image

        if self.task is not None:
            # Scaled based on original image
            new_width = int(self._image.get_width() * self.current_scale)
            new_height = int(self._image.get_height() * self.current_scale)
            transformed_image = scale(transformed_image, (new_width, new_height))
            # Add colored tint
            transformed_image.fill((255, 0, 0, 150), special_flags=pg.BLEND_MULT)

        return transformed_image

    @image.setter
    def image(self, value: pg.Surface) -> None:
        """Custom setter for image field."""
        self._image = value

    def __breathe(self) -> None:
        """Will add "breathing" effect to the tile if it has a task active."""
        if self.task is not None:
            # Limit scale
            if self.current_scale >= self.max_scale:
                self.breathing_direction = -1
            elif self.current_scale <= 1:
                self.breathing_direction = 1

            self.current_scale += self.breathing_speed * self.breathing_direction
