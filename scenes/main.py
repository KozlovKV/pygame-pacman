import pygame

from constants import Color
from objects import ButtonObject
from scenes import BaseScene


class MainScene(BaseScene):
    def __init__(self, game):
        self.level = game.settings['level']
        self.game_mode = game.settings['mode']
        self.coop = game.settings['coop']
        self.cell_width = 0
        self.cell_height = 0
        super().__init__(game)

    def create_objects(self) -> None:
        self.pacmans = []
        self.ghosts = []
        self.seeds = []
        self.super_seeds = []
        self.walls = []
        self.teleports = []
        self.generate_map()
        self.objects.append(ButtonObject(self.game, 10, 600, 200, 40, Color.SOFT_RED,
                                         self.game.exit_game, 'EXIT'))

    def generate_map(self):
        level_strings = []
        with open(f'./resources/levels/level_{self.level}.txt') as fin:
            [level_strings.append(string) for string in fin.readlines()]
        self.cell_width = self.game.FIELD_WIDTH // int(level_strings[0][3:])
        self.cell_height = self.game.FIELD_HEIGHT // int(level_strings[1][3:])
        # TODO: Считывание карты

    def is_win(self):
        pass

    def is_lose(self):
        pass
