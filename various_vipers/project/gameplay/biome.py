import logging
import random
from typing import List

import pygame as pg
from pygame.image import load
from pygame.transform import scale

from project.constants import (
    BIOME_WIDTH,
    CITY_BGS,
    DESERT_BGS,
    FOREST_BGS,
    GameLayer,
    HEIGHT,
    MOUNTAINS_BGS,
    TILES_GRASS,
    TILES_WATER,
    TILE_COLS,
    TILE_ROWS,
    TILE_WIDTH,
    WIDTH,
)
from .tile import Tile


logger = logging.getLogger(__name__)


class Biome(pg.sprite.LayeredDirty):
    """
    Abstract Biome class for all biome relevant information.
    
    Acts as a LayeredDirty to hold all sprites related to this biome.
    """

    # List of background images for this biome.
    # One will be chosen randomly to be displayed.
    background_images: List[str] = []

    other_tiles: List[str] = TILES_GRASS

    # Unique to theme tiles list
    unique_tiles: List[str] = []
    unique_tiles_chance: float = 0.3

    # Tiles that belong to cities
    city_tiles: List[str] = []
    city_tiles_chance: float = 0.2

    # Tiles that have water sources
    water_tiles: List[str] = TILES_WATER
    water_tiles_chance: float = 0.2

    # Current x position (on screen). Only updates if biome is visible
    position_x: int = 0

    def __init__(self):
        super().__init__()

        self.background = self.BiomeBackground(self.background_images)
        self.tiles = self.__generate_tilemap(TILE_COLS, TILE_ROWS)

        # Add sprites to group
        self.add(self.tiles)
        self.add(self.background)

    def update(self) -> None:
        """Update is called every game tick."""
        pass

    def move(self, pos_x: int, force: bool = False) -> None:
        """Moves biome to new x position (on screen)."""
        self.position_x = pos_x

        if not force and (
            self.position_x < -BIOME_WIDTH - TILE_WIDTH or self.position_x > WIDTH
        ):
            # Biome is not visible - don't look at the code below (I wish)
            return

        self.background.rect.x = self.position_x
        self.background.dirty = max(self.background.dirty, 1)

        for idx, tile in enumerate(self.tiles):
            # Every second row needs x offset to fit isometric tiles
            offset = int(TILE_WIDTH // 2)

            # Calculate tile position offsets
            tile_x = (idx % TILE_COLS) * TILE_WIDTH
            tile_x += offset if (idx // TILE_COLS) % 2 != 0 else 0
            tile_y = (
                HEIGHT
                - int((TILE_WIDTH * TILE_ROWS) // 1.5)
                + offset * (idx // TILE_COLS)
            )

            # Horizontally centered in it's possition
            draw_x = (
                self.position_x + tile_x - (tile.image.get_width() - TILE_WIDTH) // 2
            )
            # Vertical align to bottom - will expand upwards
            draw_y = tile_y - (tile.image.get_height() - TILE_WIDTH)

            tile.rect = pg.Rect(draw_x, draw_y, tile.rect.x, tile.rect.y)
            tile.dirty = max(tile.dirty, 1)

    def __generate_tilemap(self, width: int = 10, height: int = 4) -> List[List[Tile]]:
        """Generates random tiles based on set tile sprites and weights to spawn."""
        other_tiles_chance = max(
            1
            - self.water_tiles_chance
            + self.city_tiles_chance
            + self.unique_tiles_chance,
            0,
        )

        # Group all tiles lists with their chances to spawn
        tiles_lists = [
            (self.other_tiles, other_tiles_chance),
            (self.unique_tiles, self.unique_tiles_chance),
            (self.city_tiles, self.city_tiles_chance),
            (self.water_tiles, self.water_tiles_chance),
        ]
        # Remove empty lists
        tiles_lists = [l for l in tiles_lists if len(l[0]) > 0]

        # width*height number of non-empty styled tiles
        chosen_tile_lists = random.choices(
            [l[0] for l in tiles_lists],
            weights=[l[1] for l in tiles_lists],
            k=width * height,
        )

        tiles = []
        for tiles_list in chosen_tile_lists:
            tiles.append(Tile(str(random.choice(tiles_list))))
        return tiles

    class BiomeBackground(pg.sprite.DirtySprite):
        """Sprite for background of this biome."""

        _layer: int = GameLayer.LAYER_BIOME_BG

        def __init__(self, image_pool: List[str]):
            super().__init__()
            self.dirty = 1

            self.image = load(str(random.choice(image_pool))).convert_alpha()
            self.image = scale(self.image, (BIOME_WIDTH, BIOME_WIDTH))
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.y = HEIGHT // 5


class BiomeDesert(Biome):
    """
    Desert themed biome.

    Desert theme biomes have a lower chance to spawn a city or water tiles.
    """

    background_images: List[str] = DESERT_BGS

    unique_tiles: List[str] = []

    def __init__(
        self,
        unique_chance: float = 0.6,
        city_chance: float = 0.05,
        water_chance: float = 0.05,
    ):
        self.unique_tiles_chance = unique_chance
        self.city_tiles_chance = city_chance
        self.water_tiles_chance = water_chance

        super().__init__()


class BiomeCity(Biome):
    """City themed biome."""

    background_images: List[str] = CITY_BGS

    unique_tiles: List[str] = []

    def __init__(
        self,
        unique_chance: float = 0.3,
        city_chance: float = 0.5,
        water_chance: float = 0.05,
    ):
        self.unique_tiles_chance = unique_chance
        self.city_tiles_chance = city_chance
        self.water_tiles_chance = water_chance

        super().__init__()


class BiomeForest(Biome):
    """Foresty biome."""

    background_images: List[str] = FOREST_BGS

    unique_tiles: List[str] = []

    def __init__(
        self,
        unique_chance: float = 0.6,
        city_chance: float = 0.2,
        water_chance: float = 0.1,
    ):
        self.unique_tiles_chance = unique_chance
        self.city_tiles_chance = city_chance
        self.water_tiles_chance = water_chance

        super().__init__()


class BiomeMountains(Biome):
    """Mountain themed biome."""

    background_images: List[str] = MOUNTAINS_BGS

    unique_tiles: List[str] = []

    def __init__(
        self,
        unique_chance: float = 0.8,
        city_chance: float = 0.1,
        water_chance: float = 0.1,
    ):
        self.unique_tiles_chance = unique_chance
        self.city_tiles_chance = city_chance
        self.water_tiles_chance = water_chance

        super().__init__()
