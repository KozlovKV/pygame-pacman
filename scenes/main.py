import datetime

import pygame

from constants import Color, MAIN_FONT
from objects import ButtonObject, TextObject
from objects.base import DrawableObject
from objects.seed import Seed
from scenes import BaseScene


class MainScene(BaseScene):
    def __init__(self, game):

        self.game_mode = game.settings['mode']

        self.milliseconds = 0

        self.lives = 3

        self.paused = False

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

        self.matrix = MatrixMap(self.game)
        self.objects.append(self.matrix)

    def additional_logic(self) -> None:

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
            return self.matrix.seeds_count <= 0
        elif self.game_mode == 'hunt':
            return self.matrix.ghosts_count <= 0
        return False

    def is_lose(self):
        if self.matrix.pacmans_count <= 0:
            return True
        return False

    def end_game(self, win=False):
        self.game.is_win = win
        self.game.set_scene(self.game.GAMEOVER_SCENE_INDEX)

    def additional_event_check(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.switch_pause()

    # TODO: реализовать логику остановки
    def switch_pause(self):
        self.pause_bar.rect.y *= -1
        self.paused = not self.paused

    def process_draw(self) -> None:
        pygame.draw.rect(self.game.screen, Color.BLACK,
                         (0, 0, self.game.SCREEN_WIDTH, MatrixMap.FIELD_Y))
        super(MainScene, self).process_draw()


class MatrixPoint:
    def __init__(self, x, y, type, obj):
        self.x = x
        self.y = y
        self.type = type
        self.obj = obj

    def process_event(self, event):
        self.obj.process_event(event)

    def process_logic(self):
        self.obj.process_logic()

    def process_draw(self):
        self.obj.process_draw()


class MatrixMap(BaseScene):
    CELL_SIZE = 30
    BORDER_SIZE = 5
    FIELD_POINT = FIELD_X, FIELD_Y = 0, 100  # Координаты отсчёта для обрамления и расположения поля игры

    def __init__(self, game):
        self.first = True
        self.level = game.settings['level']
        self.coop = game.settings['coop']
        self.game_mode = game.settings['mode']
        super().__init__(game)

    def create_objects(self) -> None:
        self.pacmans = []
        self.ghosts = []
        self.seeds = []
        self.super_seeds = []
        self.walls = []
        self.teleports = []

        level_strings = []
        with open(f'./resources/levels/level_{self.level}.txt') as fin:
            [level_strings.append(string) for string in fin.readlines()]

        self.matrix_width = int(level_strings[0][3:])
        self.matrix_height = int(level_strings[1][3:])

        field_width = self.matrix_width * MatrixMap.CELL_SIZE
        width_padding = (self.game.SCREEN_WIDTH - MatrixMap.FIELD_X -
                         field_width) // 2
        field_height = self.matrix_height * MatrixMap.CELL_SIZE
        height_padding = (self.game.SCREEN_HEIGHT - MatrixMap.FIELD_Y -
                          field_height) // 2

        # Переменные для рассчёта расположения объектов на игровом поле
        real_field_x = MatrixMap.FIELD_X + width_padding
        real_field_y = MatrixMap.FIELD_Y + height_padding

        self.border_field = DrawableObject(self.game,
                                           real_field_x - MatrixMap.BORDER_SIZE,
                                           real_field_y - MatrixMap.BORDER_SIZE,
                                           field_width + MatrixMap.BORDER_SIZE * 2,
                                           field_height + MatrixMap.BORDER_SIZE * 2,
                                           Color.SOFT_BLUE)
        self.field = DrawableObject(self.game, real_field_x, real_field_y,
                                    field_width, field_height, Color.BLACK)

        level_objects_list = [string.split() for string in
                              level_strings[2:2 + self.matrix_height]]
        self.matrix = list()
        for y in range(self.matrix_height):
            self.matrix.append(list())
            for x in range(self.matrix_width):
                self.matrix[y].append(0)
                object_char = level_objects_list[y][x]
                if object_char == '#':
                    wall = DrawableObject(self.game,
                                          real_field_x + x * MatrixMap.CELL_SIZE,
                                          real_field_y + y * MatrixMap.CELL_SIZE,
                                          MatrixMap.CELL_SIZE,
                                          MatrixMap.CELL_SIZE,
                                          Color.BLUE)
                    # Добавление матричной точки стены
                    wall = MatrixPoint(x, y, 'wall', wall)
                    self.walls.append(wall)
                    self.matrix[y][x] = wall
                elif object_char == '_' and not self.game_mode == 'survival':
                    seed = Seed(self.game,
                                real_field_x + x * MatrixMap.CELL_SIZE + 10,
                                real_field_y + y * MatrixMap.CELL_SIZE + 10)
                    # Добавление матричной точки зерна
                    seed = MatrixPoint(x, y, 'seed', seed)
                    self.seeds.append(seed)
                    self.matrix[y][x] = seed
                elif object_char == 'S':
                    super_seed = DrawableObject(self.game,
                                                real_field_x + x * MatrixMap.CELL_SIZE,
                                                real_field_y + y * MatrixMap.CELL_SIZE,
                                                MatrixMap.CELL_SIZE,
                                                MatrixMap.CELL_SIZE,
                                                (233, 185, 149))
                    # Добавление матричной точки супер-зерна
                    super_seed = MatrixPoint(x, y, 'super_seed', super_seed)
                    self.super_seeds.append(super_seed)
                    self.matrix[y][x] = super_seed

                elif object_char == 'G':
                    ghost = DrawableObject(self.game,
                                           real_field_x + x * MatrixMap.CELL_SIZE,
                                           real_field_y + y * MatrixMap.CELL_SIZE,
                                           MatrixMap.CELL_SIZE,
                                           MatrixMap.CELL_SIZE,
                                           Color.SOFT_BLUE)
                    # Добавление матричной точки призрака
                    ghost = MatrixPoint(x, y, 'ghost', ghost)
                    self.ghosts.append(ghost)
                    self.matrix[y][x] = ghost
                elif object_char == 'P' or (object_char == 'p' and self.coop):
                    pacman = DrawableObject(self.game,
                                            real_field_x + x * MatrixMap.CELL_SIZE,
                                            real_field_y + y * MatrixMap.CELL_SIZE,
                                            MatrixMap.CELL_SIZE,
                                            MatrixMap.CELL_SIZE,
                                            Color.YELLOW)
                    # Добавление матричной точки пакмана
                    pacman = MatrixPoint(x, y, 'pacman', pacman)
                    self.pacmans.append(pacman)
                    self.matrix[y][x] = pacman
                # TODO: Прописать алгоритм телепортов
                self.objects += (self.pacmans + self.ghosts)

    def additional_logic(self) -> None:
        # TODO: Работает, но лучше переделать
        self.pacmans_count = len(list(filter(lambda x: x.obj.alive, self.pacmans)))
        self.ghosts_count = len(list(filter(lambda x: x.obj.alive, self.ghosts)))
        self.seeds_count = len(list(filter(lambda x: x.obj.alive,
                                           self.seeds + self.super_seeds)))

        self.check_matrix_positions(self.pacmans)
        self.check_matrix_positions(self.ghosts)

        for pacman in self.pacmans:
            self.check_collisions_with_pacman(pacman)

    def check_collisions_with_pacman(self, pacman):
        m_points = []
        x = pacman.x
        y = pacman.y
        if not x == 0:
            m_points.append(self.matrix[y][x-1])
        if not x == self.matrix_width-1:
            m_points.append(self.matrix[y][x+1])
        if not y == 0:
            m_points.append(self.matrix[y-1][x])
        if not y == self.matrix_height-1:
            m_points.append(self.matrix[y+1][x])
        for m_point in m_points:
            if pacman.obj.collision(m_point.obj):
                if m_point.type == 'wall':
                    pacman.wall_collision_reaction()
                else:
                    m_point.obj.collision_reaction()

    def check_matrix_positions(self, objects):
        for obj in objects:
            if obj.obj.rect.x // MatrixMap.CELL_SIZE != obj.x or \
               obj.obj.rect.y // MatrixMap.CELL_SIZE != obj.y:
                self.change_pos_in_matrix(obj,
                                          obj.obj.rect.x // MatrixMap.CELL_SIZE,
                                          obj.obj.rect.x // MatrixMap.CELL_SIZE)

    def change_pos_in_matrix(self, obj: MatrixPoint, new_x, new_y):
        self.matrix[obj.y][obj.x] = 0
        self.matrix[new_y][new_x] = obj
        obj.x = new_x
        obj.y = new_y

    def remove_object_from_matrix(self, x, y):
        pass

    def process_draw(self) -> None:
        if self.first:
            self.border_field.process_draw()
            self.field.process_draw()
            [wall.process_draw() for wall in self.walls]
            [seed.process_draw() for seed in self.seeds]
            [super_seed.process_draw() for super_seed in self.super_seeds]
            self.first = False
        super(MatrixMap, self).process_draw()
