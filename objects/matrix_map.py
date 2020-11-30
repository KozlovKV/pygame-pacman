from constants import Color
from objects.base import DrawableObject
from objects.s_seed import SuperSeed
from objects.seed import Seed
from scenes import BaseScene


class SimpleMatrixPoint:
    def __init__(self, x, y, type='', obj=0):
        self.x = x
        self.y = y
        self.type = type
        self.obj = obj

    def process_event(self, event):
        if self.obj != 0:
            self.obj.process_event(event)

    def process_logic(self):
        if self.obj != 0:
            self.obj.process_logic()

    def process_draw(self):
        if self.obj != 0:
            self.obj.process_draw()


class MatrixMultiPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.static_obj = SimpleMatrixPoint(x, y)
        self.moving_obj = SimpleMatrixPoint(x, y)

    def update_static_object(self, obj: SimpleMatrixPoint):
        self.static_obj = obj

    def update_moving_object(self, obj: SimpleMatrixPoint):
        self.moving_obj = obj

    def process_event(self, event):
        self.moving_obj.process_event(event)

    def process_logic(self):
        self.moving_obj.process_logic()

    def process_draw(self):
        self.static_obj.process_draw()
        self.moving_obj.process_draw()


def wall_collision_check(pacman: SimpleMatrixPoint, wall: SimpleMatrixPoint):
    vec_x = wall.x - pacman.x
    vec_y = wall.y - pacman.y
    # TODO: Раскоментировать, когда будет готов пакман
    # if vec_x == pacman.obj.vec_x or vec_y == pacman.obj.vec_y:
    #     pacman.obj.vec_x = 0
    #     pacman.obj.vec_y = 0


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
                self.matrix[y].append(MatrixMultiPoint(x, y))
                object_char = level_objects_list[y][x]
                if object_char == '#':
                    wall = DrawableObject(self.game,
                                          real_field_x + x * MatrixMap.CELL_SIZE,
                                          real_field_y + y * MatrixMap.CELL_SIZE,
                                          MatrixMap.CELL_SIZE,
                                          MatrixMap.CELL_SIZE,
                                          Color.BLUE)
                    # Добавление матричной точки стены
                    wall = SimpleMatrixPoint(x, y, 'wall', wall)
                    self.walls.append(wall)
                    self.matrix[y][x].update_static_object(wall)
                elif object_char == '_' and not self.game_mode == 'survival':
                    seed = Seed(self.game,
                                './resources/images/Seed/Seed.png',
                                real_field_x + x * MatrixMap.CELL_SIZE,
                                real_field_y + y * MatrixMap.CELL_SIZE)
                    # Добавление матричной точки зерна
                    seed = SimpleMatrixPoint(x, y, 'seed', seed)
                    self.seeds.append(seed)
                    self.matrix[y][x].update_static_object(seed)
                elif object_char == 'S':
                    super_seed = SuperSeed(self.game,
                                                './resources/images/Таблетка/Стандарт/Powerpill.png',
                                                real_field_x + x * MatrixMap.CELL_SIZE,
                                                real_field_y + y * MatrixMap.CELL_SIZE)
                    # Добавление матричной точки супер-зерна
                    super_seed = SimpleMatrixPoint(x, y, 'super_seed',
                                                   super_seed)
                    self.super_seeds.append(super_seed)
                    self.matrix[y][x].update_static_object(super_seed)

                elif object_char == 'G':
                    ghost = DrawableObject(self.game,
                                           real_field_x + x * MatrixMap.CELL_SIZE,
                                           real_field_y + y * MatrixMap.CELL_SIZE,
                                           MatrixMap.CELL_SIZE,
                                           MatrixMap.CELL_SIZE,
                                           Color.SOFT_BLUE)
                    # Добавление матричной точки призрака
                    ghost = SimpleMatrixPoint(x, y, 'ghost', ghost)
                    self.ghosts.append(ghost)
                    self.matrix[y][x].update_moving_object(ghost)
                elif object_char == 'P' or (object_char == 'p' and self.coop):
                    pacman = DrawableObject(self.game,
                                            real_field_x + x * MatrixMap.CELL_SIZE,
                                            real_field_y + y * MatrixMap.CELL_SIZE,
                                            MatrixMap.CELL_SIZE,
                                            MatrixMap.CELL_SIZE,
                                            Color.YELLOW)
                    # Добавление матричной точки пакмана
                    pacman = SimpleMatrixPoint(x, y, 'pacman', pacman)
                    self.pacmans.append(pacman)
                    self.matrix[y][x].update_moving_object(pacman)
                # TODO: Прописать алгоритм телепортов
                self.objects += (self.pacmans + self.ghosts)

    def additional_logic(self) -> None:
        self.pacmans_count = len(
            list(filter(lambda x: x.obj.alive, self.pacmans)))
        self.ghosts_count = len(
            list(filter(lambda x: x.obj.alive, self.ghosts)))
        self.seeds_count = len(list(filter(lambda x: x.obj.alive,
                                           self.seeds + self.super_seeds)))

        self.check_matrix_positions(self.pacmans)
        self.check_matrix_positions(self.ghosts)

        for pacman in self.pacmans:
            self.check_collisions_with_pacman(pacman)

    def check_collisions_with_pacman(self, pacman: SimpleMatrixPoint):
        m_points = []
        x = pacman.x
        y = pacman.y
        if not x == 0:
            m_points.append(self.matrix[y][x - 1])
        if not x == self.matrix_width - 1:
            m_points.append(self.matrix[y][x + 1])
        if not y == 0:
            m_points.append(self.matrix[y - 1][x])
        if not y == self.matrix_height - 1:
            m_points.append(self.matrix[y + 1][x])
        self.pacman_collisions_with_moving_objects(pacman, m_points)
        self.pacman_collisions_with_static_objects(pacman, m_points)

    def pacman_collisions_with_moving_objects(self, pacman: SimpleMatrixPoint,
                                              m_points):
        for m_point in m_points:
            m_obj = m_point.moving_obj
            if m_obj.type == 'ghost' and pacman.obj.collision(m_obj.obj):
                m_obj.obj.collision_reaction(pacman.obj)

    def pacman_collisions_with_static_objects(self, pacman: SimpleMatrixPoint,
                                              m_points):
        for m_point in m_points:
            s_obj = m_point.static_obj
            if s_obj.type == 'wall':
                wall_collision_check(pacman, s_obj)
            elif s_obj.type == 'teleport':
                s_obj.check_collisions_with_entries(pacman.obj)
            elif not s_obj.type == '':
                s_obj.obj.collision_reaction()
                self.remove_static_object_from_matrix(m_point)

    def check_matrix_positions(self, objects):
        for m_obj in objects:
            if (m_obj.obj.rect.x // MatrixMap.CELL_SIZE != m_obj.x or
                m_obj.obj.rect.y // MatrixMap.CELL_SIZE != m_obj.y) and \
                    m_obj.obj.rect.x > 0 and m_obj.obj.rect.y > 0:
                self.change_pos_in_matrix(m_obj,
                                          m_obj.obj.rect.x // MatrixMap.CELL_SIZE,
                                          m_obj.obj.rect.x // MatrixMap.CELL_SIZE)

    def change_pos_in_matrix(self, m_point: SimpleMatrixPoint, new_x, new_y):
        self.remove_moving_object_from_matrix(m_point)
        self.matrix[new_y][new_x].update_moving_object(m_point)
        m_point.x = new_x
        m_point.y = new_y

    def remove_static_object_from_matrix(self, m_point: SimpleMatrixPoint):
        self.matrix[m_point.y][m_point.x].update_static_object(
            SimpleMatrixPoint(m_point.x, m_point.y)
        )

    def remove_moving_object_from_matrix(self, m_point: SimpleMatrixPoint):
        self.matrix[m_point.y][m_point.x].update_moving_object(
            SimpleMatrixPoint(m_point.x, m_point.y)
        )

    def process_draw(self) -> None:
        if self.first:
            self.border_field.process_draw()
            self.field.process_draw()
            [wall.process_draw() for wall in self.walls]
            [seed.process_draw() for seed in self.seeds]
            [super_seed.process_draw() for super_seed in self.super_seeds]
            self.first = False
        super(MatrixMap, self).process_draw()
