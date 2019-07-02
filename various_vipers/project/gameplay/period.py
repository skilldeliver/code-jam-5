import logging
import random
from typing import List, Optional

import pygame as pg

from project.constants import TILE_COLS, TILE_ROWS
from .biome import Biome, BiomeCity, BiomeDesert, BiomeForest, BiomeMountains
from .earth import Earth
from .task import TaskCursorMaze, TaskRockPaperScissors, TaskTicTacToe


logger = logging.getLogger(__name__)


class Period(pg.sprite.LayeredDirty):
    """
    This class represents an abstract Time Period Style.

    Game difficulties are split into Time Periods - with each time period having different
      tile styles, tasks, images and chances to spawn cities.
    """

    # List of biomes, that will be looped through
    biomes: List[Biome]

    # Time passed after the last task spawn
    time_of_last_task_spawn: Optional[int] = None
    # How many game ticks between task spawns (will be floored and converted to int)
    task_spawn_freq: float = 600
    # How much to increase task spawn frequency with each game tick
    task_spawn_freq_inc: float = 0.05

    # Chance to spawn certain task types
    maze_chance: float = 1.0
    rps_chance: float = 1.0
    ttt_chance: float = 1.0

    def __init__(self):
        super().__init__()

        self.biomes = [
            BiomeDesert(),
            BiomeDesert(),
            BiomeDesert(),
            BiomeMountains(),
            BiomeMountains(),
            BiomeMountains(),
            BiomeForest(),
            BiomeForest(),
            BiomeForest(),
            BiomeCity(),
            BiomeCity(),
            BiomeCity(),
        ]

        self.earth = Earth(self.biomes)

    def update(self) -> None:
        """Update gets called every game tick."""
        self.add(self.earth)
        self.earth.update()
        self.__handle_task_spawn()

    def __handle_task_spawn(self) -> None:
        if (
            self.time_of_last_task_spawn is None
            or self.time_of_last_task_spawn >= self.task_spawn_freq
        ):
            self.time_of_last_task_spawn = 0
            self.__spawn_task()
        else:
            self.time_of_last_task_spawn += 1
        self.task_spawn_freq = max(self.task_spawn_freq + self.task_spawn_freq_inc, 0)

    def __spawn_task(self) -> None:
        """Spawns a task on a random tile."""
        # TODO :: add check if tile already has a task or not

        # Get number of tiles between all biomes
        tile_count = TILE_COLS * TILE_ROWS * len(self.biomes)
        # Chose a random tile out of all
        random_tile_idx = random.randint(0, tile_count - 1)
        # Calculate biome index from the global tile index
        biome_idx = random_tile_idx // (TILE_COLS * TILE_ROWS)
        # Calculate tile index local to the biome chosen
        tile_in_biome_idx = random_tile_idx - (TILE_COLS * TILE_ROWS * biome_idx)

        biome = self.biomes[biome_idx]
        tile = biome.tiles[tile_in_biome_idx]
        new_task = random.choices(
            [TaskCursorMaze, TaskRockPaperScissors, TaskTicTacToe],
            weights=[self.maze_chance, self.rps_chance, self.ttt_chance],
        )
        tile.task = new_task[0](biome)
        tile.dirty = 2

        # self.earth.fix_indicators()


class PeriodMedieval(Period):
    """Medieval themed Time Period."""

    pass


class PeriodModern(Period):
    """Modern time themed Time Period."""

    pass


class PeriodFuture(Period):
    """Future time themed Time Period."""

    pass
