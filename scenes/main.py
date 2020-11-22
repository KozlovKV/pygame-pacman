from functools import reduce

import pygame

from constants import Color
from objects import ButtonObject
from scenes import BaseScene


class MainScene(BaseScene):
    def __init__(self, game):
        self.level = game.settings['level']
        self.game_mode = game.settings['mode']
        self.coop = game.settings['coop']
        self.paused = False
        self.cell_width = 0
        self.cell_height = 0
        super().__init__(game)

        self.pacmans = []
        self.ghosts = []
        self.seeds = []
        self.super_seeds = []
        self.walls = []
        self.teleports = []

        self.pacmans_count = len(self.pacmans)
        self.seeds_count = len(self.seeds) + len(self.super_seeds)
        self.ghosts_count = self.game.settings['ghosts_count']

    def create_objects(self) -> None:
        self.generate_map()
        self.objects.append(
            ButtonObject(self.game, 10, 600, 200, 40, Color.SOFT_RED,
                         self.game.exit_game, 'EXIT'))

    def generate_map(self):
        level_strings = []
        with open(f'./resources/levels/level_{self.level}.txt') as fin:
            [level_strings.append(string) for string in fin.readlines()]
        self.cell_width = self.game.FIELD_WIDTH // int(level_strings[0][3:])
        self.cell_height = self.game.FIELD_HEIGHT // int(level_strings[1][3:])
        # TODO: Считывание карты

    def additional_logic(self) -> None:
        self.pacmans_count = len(list(filter(lambda x: x.alive, self.pacmans)))
        self.ghosts_count = len(list(filter(lambda x: x.alive, self.ghosts)))
        self.seeds_count = len(list(filter(lambda x: x.alive,
                                           self.seeds + self.super_seeds)))

        if self.is_win():
            self.end_game(True)
        elif self.is_lose():
            self.end_game(False)

    def is_win(self):
        if self.game_mode == 'score_cup':
            return self.seeds_count <= 0
        elif self.game_mode == 'hunt':
            return self.ghosts_count <= 0
        return False

    def is_lose(self):
        if self.pacmans_count <= 0:
            return True
        return False

    def end_game(self, win=False):
        self.game.is_win = win
        self.game.set_scene(self.game.GAMEOVER_SCENE_INDEX)

    def additional_event_check(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.switch_pause()

    def switch_pause(self):
        self.paused = not self.paused
