"""Game model."""
import logging

import pygame as pg

from project.UI.page.credits import Credits
from project.UI.page.main_menu import MainMenu
from project.UI.page.options import Options
from project.constants import (
    Color,
    FPS,
    HEIGHT,
    SHOW_FPS,
    WIDTH,
    WindowState,
    GameLayer,
)
from project.gameplay.game_view import GameView


logger = logging.getLogger(__name__)


class Game:
    """Represents main game class."""

    def __init__(self, start_game=False):
        """Set initial values."""
        pg.init()
        pg.display.set_caption("Various Vipers game in development")

        self.running = True
        self.playing = start_game

        self.mouse_x = self.mouse_y = int()
        self.event = None

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.window_state = WindowState.main_menu

        self.main_menu = MainMenu(self.screen)
        self.options = Options(self.screen)
        self.credits = Credits(self.screen)
        self.game_view = GameView()
        if SHOW_FPS:
            self.game_view.add(self.FpsIndicator(self.clock))

    def run(self):
        """Draw and get events."""
        self.clock.tick(FPS)
        self._get_events()

        if self.playing and self.game_view:
            self.game_view.update()

        self._draw()

    def _get_events(self):
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()

        for event in pg.event.get():
            self.event = event
            if event.type == pg.QUIT:
                self.running = False

    def _draw(self):
        if self.playing and self.game_view:
            self.game_view.draw(self.screen)
        else:
            self.screen.fill(Color.aqua)

            if self.window_state == WindowState.game:
                self.playing = True
            elif self.window_state == WindowState.main_menu:
                self.window_state = self.main_menu.draw(
                    self.mouse_x, self.mouse_y, self.event
                )
            elif self.window_state == WindowState.options:
                self.window_state = self.options.draw(
                    self.mouse_x, self.mouse_y, self.event
                )
            elif self.window_state == WindowState.credit:
                self.window_state = self.credits.draw(
                    self.mouse_x, self.mouse_y, self.event
                )
            elif self.window_state == WindowState.quited:
                self.running = False

        pg.display.flip()

    class FpsIndicator(pg.sprite.DirtySprite):
        """FPS indicator is drawn at the top right of the screen."""

        _layer = GameLayer.LAYER_UI

        def __init__(self, clock):
            super().__init__()
            self.dirty = 2

            self.clock = clock

            self.font = pg.font.Font(None, 50)

        def update(self) -> None:
            self.image = self.font.render(
                str(int(self.clock.get_fps())), True, pg.Color("red")
            )
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH - self.image.get_width()
            self.rect.y = 0
