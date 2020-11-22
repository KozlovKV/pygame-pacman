import datetime

import pygame

from constants import Color, MAIN_FONT
from objects import ButtonObject, TextObject
from scenes import BaseScene


class MainScene(BaseScene):
    CELL_SIZE = 30

    def __init__(self, game):
        self.level = game.settings['level']
        self.game_mode = game.settings['mode']
        self.coop = game.settings['coop']

        self.begin_time = datetime.datetime.now()
        self.current_time = datetime.datetime.now()

        self.lives = 3

        self.paused = False

        self.field_width = 0
        self.field_height = 0

        self.pacmans = []
        self.ghosts = []
        self.seeds = []
        self.super_seeds = []
        self.walls = []
        self.teleports = []

        self.pacmans_count = len(self.pacmans)
        self.seeds_count = len(self.seeds) + len(self.super_seeds)
        self.ghosts_count = game.settings['ghosts_count']

        super().__init__(game)

    def create_objects(self) -> None:
        tmp_x = 20 + MAIN_FONT.size('SCORE: 0000')[0] // 2
        self.score_bar = TextObject(self.game, text='SCORE: 0', x=tmp_x, y=20)
        tmp_x = self.game.SCREEN_WIDTH - MAIN_FONT.size('TIME: 0000')[0] // 2 \
                - 20
        self.playing_time = TextObject(self.game, text='TIME: 0', x=tmp_x, y=20)
        tmp_x = self.game.SCREEN_WIDTH // 2
        self.lives_bar = TextObject(self.game, text=f'LIVES: {self.lives}',
                                x=tmp_x, y=20)

        self.generate_map()

        self.objects.append(
            ButtonObject(self.game, 10, 600, 200, 40, Color.SOFT_RED,
                         self.game.exit_game, 'EXIT'))
        self.objects.append(self.score_bar)
        self.objects.append(self.playing_time)
        self.objects.append(self.lives_bar)

    def generate_map(self):
        level_strings = []
        with open(f'./resources/levels/level_{self.level}.txt') as fin:
            [level_strings.append(string) for string in fin.readlines()]
        # TODO: Считывание карты

    def additional_logic(self) -> None:
        self.pacmans_count = len(list(filter(lambda x: x.alive, self.pacmans)))
        self.ghosts_count = len(list(filter(lambda x: x.alive, self.ghosts)))
        self.seeds_count = len(list(filter(lambda x: x.alive,
                                           self.seeds + self.super_seeds)))

        self.current_time = datetime.datetime.now()
        time_delta = self.current_time - self.begin_time
        seconds_delta = int(time_delta.total_seconds())
        self.playing_time.update_text(f'TIME: {seconds_delta}')

        self.score_bar.update_text(f'SCORE: {self.game.score}')

        self.lives_bar.update_text(f'LIVES: {self.lives}')

        # if self.is_win():
        #     self.end_game(True)
        # elif self.is_lose():
        #     self.end_game(False)

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
