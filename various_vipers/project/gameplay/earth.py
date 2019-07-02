import logging
import random
from typing import Any, List, Tuple

import pygame as pg
from pygame.image import load

from project.constants import (
    BG_CLOUDS_SCROLL_SPEED,
    BG_SCROLL_SPEED,
    BIOME_WIDTH,
    CLOUD_LAYERS_BG,
    CLOUD_LAYERS_FG,
    FG_CLOUDS_SCROLL_SPEED,
    HEIGHT,
    TILE_COLS,
    TILE_ROWS,
    TILE_WIDTH,
    WIDTH,
    GameLayer,
)
from .biome import Biome
from .clouds import Clouds, CloudsFarther, CloudsCloser
from .indicator import Indicator
from .tile import Tile


logger = logging.getLogger(__name__)


class Earth(pg.sprite.LayeredDirty):
    """
    Represent Earth class object.

    Includes logic for handling background and game tasks.
    """

    current_cloud_bg_pos: float = 0
    current_cloud_fg_pos: float = 0

    def __init__(self, biomes: List[Biome]):
        super().__init__()

        self.biomes = biomes

        # Calculate max position by added the width of all bg images
        self.max_position = BIOME_WIDTH * len(self.biomes)

        # Add all biomes to the group; set initial x positions
        offset_x = 0
        for biome in self.biomes:
            biome.move(offset_x, True)
            self.add(biome)
            offset_x += BIOME_WIDTH

        # Need to draw one tile row at a time, between all biomes to avoid isometric tile clipping
        # Because the initial map is grouped by biomes, we need to do some magic to group by rows
        tiles = self.remove_sprites_of_layer(GameLayer.LAYER_TILES)
        for y in range(TILE_ROWS):
            for x in range(len(biomes)):
                start = TILE_COLS * TILE_ROWS * x + TILE_COLS * y
                end = start + TILE_COLS
                self.add(tiles[start:end])

    @property
    def clouds(self) -> List[Clouds]:
        """Returns visible clouds."""
        return [c for c in self.sprites() if c == type(Clouds)]

    def update(self) -> None:
        """Update game logic with each game tick."""
        key_pressed = pg.key.get_pressed()

        if key_pressed[pg.K_a] or key_pressed[pg.K_LEFT]:
            self._scroll_left()
        if key_pressed[pg.K_d] or key_pressed[pg.K_RIGHT]:
            self._scroll_right()

        # update biomes - move
        self._update_biomes()
        # update clouds - remove, add
        self._update_clouds()
        # update indicators - remove, move, add
        self._update_indicators()
        super().update()

    def _update_biomes(self) -> None:
        """Move farthest biomes closer to create looping effect."""
        _count = len(self.biomes) - 1
        for biome in self.biomes:
            if biome.position_x >= _count * BIOME_WIDTH:
                # If we don't have any biomes < 0, move there the last biome
                new_x = -BIOME_WIDTH + biome.position_x - (_count * BIOME_WIDTH)
                biome.move(new_x)
            elif biome.position_x <= -BIOME_WIDTH:
                # Prefer to always keep only 1 biome to our left
                new_x = (_count * BIOME_WIDTH) - abs(biome.position_x + BIOME_WIDTH)
                biome.move(new_x)

    def _update_clouds(self) -> None:
        """Add new clouds, remove offscreen clouds."""
        # Check if we need to add new clouds
        new_cloud = None
        if self.current_cloud_bg_pos > 0:
            new_cloud = CloudsFarther()
            self.current_cloud_bg_pos = -new_cloud.image.get_width()
            new_cloud.rect.x = self.current_cloud_bg_pos
        if self.current_cloud_fg_pos > 0:
            new_cloud = CloudsCloser()
            self.current_cloud_fg_pos = -new_cloud.image.get_width()
            new_cloud.rect.x = self.current_cloud_fg_pos

        if new_cloud:
            self.add(new_cloud)

        # Remove clouds that scrolled out of screen to the right
        for cloud in self.clouds:
            if cloud.rect.x >= WIDTH:
                self.remove(cloud)

    def _update_indicators(self) -> None:
        """Add new indicators, move existing indicators."""
        pass

    def _scroll_left(self) -> None:
        logger.debug("Scrolling LEFT.")
        for biome in self.biomes:
            biome.move(biome.position_x + BG_SCROLL_SPEED)
        for cloud in self.clouds:
            cloud.move(1)

    def _scroll_right(self) -> None:
        logger.debug("Scrolling RIGHT.")
        for biome in self.biomes:
            biome.move(biome.position_x - BG_SCROLL_SPEED)
        for cloud in self.clouds:
            cloud.move(-2)


#    def fix_indicators(self) -> None:
#        """Will add missing indicators. Should be called when indicator could appear."""
#        # Loop through all tiles. If tile has task, but no indicator - add it
#        for biome_idx, biome in enumerate(self.biomes):
#            for tile in biome.tiles:
#                if tile.task is None:
#                    continue
#
#                indicator = next(
#                    (i for i in self.indicators if i.tile == tile), None
#                )
#
#                # If tile is visible - dont need indicator
#                if tile in self.visible_tiles:
#                    if indicator:
#                        self.indicators.remove(indicator)
#                    continue
#
#                if indicator is None:
#                    indicator = Indicator(tile)
#                    self.indicators.append(indicator)
#
#                # Calculate if the tile is to the left or right of the screen
#                biome_pos = biome_idx * BIOME_WIDTH
#                if self.current_biome_pos < biome_pos:
#                    distance_left = (
#                        self.max_position - biome_pos + self.current_biome_pos
#                    )
#                    distance_right = biome_pos - self.current_biome_pos
#                else:
#                    distance_left = self.current_biome_pos - biome_pos
#                    distance_right = (
#                        self.max_position - self.current_biome_pos + biome_pos
#                    )
#                indicator.flip(distance_left <= distance_right)
#
#    def __prepare_draw_clouds(
#        self,
#        pool: List[pg.Surface],
#        current_list: List[pg.Surface],
#        x_pos: int,
#        y_pos: int = 0,
#    ) -> List[Any]:
#        """
#        Logic to handle drawing a single cloud plane.
#
#        Returns a list of Surface draw arguments to draw later.
#        """
#        draw_args = []
#        offset = x_pos
#
#        for i, cloud in enumerate(current_list):
#            draw_args.append([cloud, (offset, y_pos)])
#            offset += cloud.get_width()
#
#            # Remove clouds that are offscreen to the right
#            if offset > WIDTH:
#                current_list = current_list[:i]
#                break
#
#        # Add new clouds to fill the rest of the screen
#        while offset < WIDTH:
#            new_cloud = random.choice(pool)
#            current_list.append(new_cloud)
#            draw_args.append([new_cloud, (offset, y_pos)])
#            offset += new_cloud.get_width()
#
#        return draw_args
#
#    def __draw_biomes(self) -> None:
#        """Draw biomes related images - will only draw objects that are visible."""
#        # Get first biome to draw from
#        i, biome_x = self.__find_first_biome()
#        # From the first BG image, draw new images to the right, until whole screen is filled
#        while True:
#            if i > len(self.biomes) - 1:
#                # Loop images
#                i = 0
#
#            biome = self.biomes[i]
#            biome.move(biome_x)
#            biome.draw(self.screen)
#
#            biome_x += BIOME_WIDTH
#            if biome_x > WIDTH:
#                break
#
#            i += 1
#
#    def __find_first_biome(self) -> Tuple[int, float]:
#        """
#        Function returns index, and position of first biome that should be drawn on the left.
#
#        Screen and individual images widths are taken into account when finding the first biome.
#        """
#        _position = 0
#        i = 0
#        while i < len(self.biomes):
#            if _position - self.current_biome_pos + BIOME_WIDTH > 0:
#                break
#
#            _position += BIOME_WIDTH
#            i += 1
#
#        return (i, _position - self.current_biome_pos)
#
#    def __update_positions(self) -> None:
#        """Correct current position based on min and max values."""
#        if self.current_biome_pos > self.max_position:
#            self.current_biome_pos = 0
#        elif self.current_biome_pos < 0:
#            self.current_biome_pos = self.max_position
#
#        # Cloud position will always be the position of first cloud (offscreen to the left)
#        if self.current_cloud_bg_pos > 0:
#            self.cloud_layers_bg = [
#                random.choice(self.cloud_layers_bg_pool)
#            ] + self.cloud_layers_bg
#            self.current_cloud_bg_pos = -self.cloud_layers_bg[0].get_width()
#        if self.current_cloud_fg_pos > 0:
#            self.cloud_layers_fg = [
#                random.choice(self.cloud_layers_fg_pool)
#            ] + self.cloud_layers_fg
#            self.current_cloud_fg_pos = -self.cloud_layers_fg[0].get_width()
#
