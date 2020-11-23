import datetime

import pygame

from constants import Color, MAIN_FONT
from objects import ButtonObject, TextObject
from objects.base import DrawableObject
from objects.seed import Seed
from scenes import BaseScene


class MainScene(BaseScene):
    CELL_SIZE = 30
    BORDER_SIZE = 5
    FIELD_POINT = FIELD_X, FIELD_Y = 0, 100  # Координаты отсчёта для обрамления и расположения поля игры

    def __init__(self, game):

        self.level = game.settings['level']
        self.game_mode = game.settings['mode']
        self.coop = game.settings['coop']

        self.milliseconds = 0

        self.lives = 3

        self.paused = False

        self.border_field = None
        self.field = None

        super().__init__(game)

    def create_objects(self) -> None:
        self.score_bar = None
        self.playing_time = None
        self.lives_bar = None
        self.pause_bar = None
        self.pause_button = None

        tmp_x = 20 + MAIN_FONT.size('SCORE: 0000')[0] // 2
        self.score_bar = TextObject(self.game, text='SCORE: 0', x=tmp_x, y=20)

        tmp_x = self.game.SCREEN_WIDTH - MAIN_FONT.size('TIME: 0000')[
            0] // 2 - 20
        self.playing_time = TextObject(self.game, text='TIME: 0', x=tmp_x, y=20)

        tmp_x = self.game.SCREEN_WIDTH // 2
        self.lives_bar = TextObject(self.game, text=f'LIVES: {self.lives}',
                                    x=tmp_x, y=20)
        self.pause_bar = TextObject(self.game, text='PAUSED',
                                    x=tmp_x, y=-60, color=Color.RED)

        self.pause_button = ButtonObject(self.game,
                                         self.game.SCREEN_WIDTH - 210, 60,
                                         200, 40, Color.SOFT_RED,
                                         self.switch_pause, 'PAUSE')

        self.objects.append(self.score_bar)
        self.objects.append(self.playing_time)
        self.objects.append(self.lives_bar)
        self.objects.append(self.pause_bar)
        self.objects.append(self.pause_button)
        self.objects.append(
            ButtonObject(self.game, 10, 60, 200, 40, Color.SOFT_RED,
                         self.game.exit_game, 'EXIT'))

        self.generate_map()

    def generate_map(self):
        self.pacmans = []
        self.ghosts = []
        self.seeds = []
        self.super_seeds = []
        self.walls = []
        self.teleports = []

        level_strings = []
        with open(f'./resources/levels/level_{self.level}.txt') as fin:
            [level_strings.append(string) for string in fin.readlines()]

        cells_in_row = int(level_strings[0][3:])
        cells_in_col = int(level_strings[1][3:])

        field_width = cells_in_row * MainScene.CELL_SIZE
        width_padding = (self.game.SCREEN_WIDTH - MainScene.FIELD_X -
                         field_width) // 2
        field_height = cells_in_col * MainScene.CELL_SIZE
        height_padding = (self.game.SCREEN_HEIGHT - MainScene.FIELD_Y -
                          field_height) // 2

        # Переменные для рассчёта расположения объектов на игровом поле
        real_field_x = MainScene.FIELD_X + width_padding
        real_field_y = MainScene.FIELD_Y + height_padding

        self.border_field = DrawableObject(self.game,
                                           real_field_x - MainScene.BORDER_SIZE,
                                           real_field_y - MainScene.BORDER_SIZE,
                                           field_width + MainScene.BORDER_SIZE * 2,
                                           field_height + MainScene.BORDER_SIZE * 2,
                                           Color.SOFT_BLUE)
        self.field = DrawableObject(self.game, real_field_x, real_field_y,
                                    field_width, field_height, Color.BLACK)
        self.objects.append(self.border_field)
        self.objects.append(self.field)

        level_objects_list = [string.split() for string in
                              level_strings[2:2 + cells_in_col]]
        for y in range(cells_in_col):
            for x in range(cells_in_row):
                object_char = level_objects_list[y][x]
                if object_char == '#':
                    self.walls.append(
                        # Добавление стены
                        # . . .
                        # Макет стены
                        DrawableObject(self.game,
                                       real_field_x + x * MainScene.CELL_SIZE,
                                       real_field_y + y * MainScene.CELL_SIZE,
                                       MainScene.CELL_SIZE, MainScene.CELL_SIZE,
                                       Color.BLUE)
                    )
                elif object_char == '_' and not self.game_mode == 'survival':
                    self.seeds.append(
                        # Добавление зерна
                        Seed(self.game,
                             real_field_x + x * MainScene.CELL_SIZE + 10,
                             real_field_y + y * MainScene.CELL_SIZE + 10)
                    )
                elif object_char == 'S':
                    self.super_seeds.append(
                        # Добавление супер-зерна
                        # . . .
                        # Макет супер-зерна
                        DrawableObject(self.game,
                                       real_field_x + x * MainScene.CELL_SIZE,
                                       real_field_y + y * MainScene.CELL_SIZE,
                                       MainScene.CELL_SIZE, MainScene.CELL_SIZE,
                                       (233, 185, 149))
                    )
                elif object_char == 'G':
                    self.ghosts.append(
                        # Добавление призраков по кругу
                        # . . .
                        # Макет призрака
                        DrawableObject(self.game,
                                       real_field_x + x * MainScene.CELL_SIZE,
                                       real_field_y + y * MainScene.CELL_SIZE,
                                       MainScene.CELL_SIZE, MainScene.CELL_SIZE,
                                       Color.SOFT_BLUE)
                    )
                elif object_char == 'P':
                    self.pacmans.append(
                        # Добавление Пакмана
                        # . . .
                        # Макет пакмана
                        DrawableObject(self.game,
                                       real_field_x + x * MainScene.CELL_SIZE,
                                       real_field_y + y * MainScene.CELL_SIZE,
                                       MainScene.CELL_SIZE, MainScene.CELL_SIZE,
                                       Color.YELLOW)
                    )
                elif object_char == 'p' and self.coop:
                    self.pacmans.append(
                        # Добавление Пакмана
                        # . . .
                        # Макет пакмана
                        DrawableObject(self.game,
                                       real_field_x + x * MainScene.CELL_SIZE,
                                       real_field_y + y * MainScene.CELL_SIZE,
                                       MainScene.CELL_SIZE, MainScene.CELL_SIZE,
                                       Color.SOFT_YELLOW)
                    )
                # TODO: Прописать алгоритм телепортов
                # TODO: оптимизировать процесс
                self.objects += (self.pacmans + self.ghosts + self.seeds +
                                 self.super_seeds + self.walls)

                self.pacmans_count = len(self.pacmans)
                self.seeds_count = len(self.seeds) + len(self.super_seeds)
                self.ghosts_count = self.game.settings['ghosts_count']

    def additional_logic(self) -> None:
        self.pacmans_count = len(list(filter(lambda x: x.alive, self.pacmans)))
        self.ghosts_count = len(list(filter(lambda x: x.alive, self.ghosts)))
        self.seeds_count = len(list(filter(lambda x: x.alive,
                                           self.seeds + self.super_seeds)))

        self.milliseconds += self.game.TICK
        self.playing_time.update_text(f'TIME: {self.milliseconds // 1000}')

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
        self.pause_bar.rect.y *= -1
        self.paused = not self.paused
