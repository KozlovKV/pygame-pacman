from constants import *
from objects.base import DrawableObject
from objects.ghost import GhostFabric
from objects.image import ImageObject
from objects.pacman import Pacman
from objects.s_seed import SuperSeed
from objects.seed import Seed
from objects.teleport import TeleportObject
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
    x = pacman.x + pacman.obj.vec_x
    y = pacman.y + pacman.obj.vec_y
    if (x == wall.x or y == wall.y) and pacman.obj.collision(wall.obj):
        pacman.obj.vec_x *= -1
        pacman.obj.vec_y *= -1
        pacman.obj.move(pacman.obj.vec_x * PACMAN_SPEED,
                        pacman.obj.vec_y * PACMAN_SPEED)
        pacman.obj.vec_x = 0
        pacman.obj.vec_y = 0


class MatrixMap(BaseScene):
    BORDER_SIZE = 5
    FIELD_POINT = FIELD_X, FIELD_Y = 0, 100  # Координаты отсчёта для обрамления и расположения поля игры
    GHOST_ACTIVATION_CD = 1000

    def __init__(self, game):
        self.first = True
        self.current_ghost_cd = MatrixMap.GHOST_ACTIVATION_CD

        self.level = game.settings['level']
        self.coop = game.settings['coop']
        self.game_mode = game.settings['mode']
        super().__init__(game)

    def create_objects(self) -> None:
        self.pacmans = []
        self.ghosts = []
        self.seeds = []
        self.super_seeds = []
        self.bg_walls = []
        self.walls = []
        self.walls_ghosts_in = []
        self.teleports = []

        level_strings = []
        with open(f'./resources/levels/level_{self.level}.txt') as fin:
            [level_strings.append(string) for string in fin.readlines()]

        self.matrix_width = int(level_strings[0][3:])
        self.matrix_height = int(level_strings[1][3:])

        field_width = self.matrix_width * CELL_SIZE
        width_padding = (self.game.SCREEN_WIDTH - MatrixMap.FIELD_X -
                         field_width) // 2
        field_height = self.matrix_height * CELL_SIZE
        height_padding = (self.game.SCREEN_HEIGHT - MatrixMap.FIELD_Y -
                          field_height) // 2

        # Переменные для рассчёта расположения объектов на игровом поле
        self.game.REAL_FIELD_X = MatrixMap.FIELD_X + width_padding
        self.game.REAL_FIELD_Y = MatrixMap.FIELD_Y + height_padding

        self.matrix_grid = list()
        for my in range(self.matrix_height):
            for mx in range(self.matrix_width):
                self.matrix_grid.append(
                    [my * CELL_SIZE + self.game.REAL_FIELD_Y,
                     mx * CELL_SIZE + self.game.REAL_FIELD_X])

        self.border_field = DrawableObject(self.game,
                                           self.game.REAL_FIELD_X - MatrixMap.BORDER_SIZE,
                                           self.game.REAL_FIELD_Y - MatrixMap.BORDER_SIZE,
                                           field_width + MatrixMap.BORDER_SIZE * 2,
                                           field_height + MatrixMap.BORDER_SIZE * 2,
                                           self.game.settings[
                                               "level_border_color"])
        self.field = DrawableObject(self.game, self.game.REAL_FIELD_X,
                                    self.game.REAL_FIELD_Y,
                                    field_width, field_height, Color.BLACK)

        level_objects_list = [string.split() for string in
                              level_strings[2:2 + self.matrix_height]]
        self.matrix = list()
        self.generate_all_matrix(level_objects_list)
        self.generate_ghosts(level_objects_list)
        self.objects += (self.pacmans + self.ghosts + self.teleports)

    def generate_all_matrix(self, level_objects_list):
        real_field_x = self.game.REAL_FIELD_X
        real_field_y = self.game.REAL_FIELD_Y
        # print("REAL FIELD", real_field_y, real_field_x)  # ////////////////////////////
        teleports_pairs = [list() for _ in range(10)]
        for y in range(self.matrix_height):
            self.matrix.append(list())
            for x in range(self.matrix_width):
                self.matrix[y].append(MatrixMultiPoint(x, y))
                object_char = level_objects_list[y][x]
                if object_char != '#' and object_char != '+':
                    wall = ImageObject(self.game,
                                       x=real_field_x + x * CELL_SIZE,
                                       y=real_field_y + y * CELL_SIZE,
                                       filename=Textures.CELL_BG[self.game.settings['cell_texture']])
                    # Добавление матричной точки стены
                    self.bg_walls.append(wall)
                if object_char == '#':
                    wall = ImageObject(self.game,
                                       x=real_field_x + x * CELL_SIZE,
                                       y=real_field_y + y * CELL_SIZE,
                                       filename=Textures.WALL)
                    # Добавление матричной точки стены
                    wall = SimpleMatrixPoint(x, y, 'wall', wall)
                    self.walls.append(wall)
                    self.matrix[y][x].update_static_object(wall)
                    self.matrix_grid.remove([real_field_y + y * CELL_SIZE,
                                             real_field_x + x * CELL_SIZE])
                elif object_char == '+':
                    wall_ghost_in = ImageObject(self.game,
                                                x=real_field_x + x * CELL_SIZE,
                                                y=real_field_y + y * CELL_SIZE,
                                                filename=Textures.WALL_GHOST_IN)
                    # Добавление матричной точки стены
                    wall_ghost_in = SimpleMatrixPoint(x, y, 'wall_ghost_in',
                                                      wall_ghost_in)
                    self.walls_ghosts_in.append(wall_ghost_in)
                    self.matrix[y][x].update_static_object(wall_ghost_in)
                    self.matrix_grid.remove([real_field_y + y * CELL_SIZE,
                                             real_field_x + x * CELL_SIZE])
                elif object_char == '_' and not self.game_mode == 'survival':
                    seed = Seed(self.game,
                                real_field_x + x * CELL_SIZE,
                                real_field_y + y * CELL_SIZE)
                    # Добавление матричной точки зерна
                    seed = SimpleMatrixPoint(x, y, 'seed', seed)
                    self.seeds.append(seed)
                    self.matrix[y][x].update_static_object(seed)
                elif object_char == 'S':
                    super_seed = SuperSeed(self.game,
                                           real_field_x + x * CELL_SIZE,
                                           real_field_y + y * CELL_SIZE)
                    # Добавление матричной точки супер-зерна
                    super_seed = SimpleMatrixPoint(x, y, 'super_seed',
                                                   super_seed)
                    self.super_seeds.append(super_seed)
                    self.matrix[y][x].update_static_object(super_seed)
                elif object_char == 'P' or (object_char == 'p' and self.coop):
                    pacman = Pacman(self.game,
                                    real_field_x + x * CELL_SIZE,
                                    real_field_y + y * CELL_SIZE,
                                    self.matrix_grid,
                                    1 if object_char == 'P' else 2)
                    # Добавление матричной точки пакмана
                    pacman = SimpleMatrixPoint(x, y, 'pacman', pacman)
                    self.pacmans.append(pacman)
                    self.matrix[y][x].update_moving_object(pacman)
                elif '0' <= object_char <= '3':
                    i = int(object_char)
                    teleports_pairs[i].append((x, y))
                    if len(teleports_pairs[i]) == 2:
                        pair = teleports_pairs[i]
                        x1, y1 = pair[0][0], pair[0][1]
                        x2, y2 = pair[1][0], pair[1][1]
                        teleport = TeleportObject(self.game,
                                                  real_field_x + x1 * CELL_SIZE,
                                                  real_field_y + y1 * CELL_SIZE,
                                                  real_field_x + x2 * CELL_SIZE,
                                                  real_field_y + y2 * CELL_SIZE,
                                                  int(object_char))
                        teleport1 = SimpleMatrixPoint(x1, y1, 'teleport',
                                                      teleport)
                        self.matrix[y1][x1].update_static_object(teleport1)
                        teleport2 = SimpleMatrixPoint(x2, y2, 'teleport',
                                                      teleport)
                        self.matrix[y2][x2].update_static_object(teleport2)
                        self.teleports.append(teleport)
                        teleports_pairs[i] = list()
        for pman in self.pacmans:
            pman.obj.set_grid(self.matrix_grid)

    def generate_ghosts(self, level_objects_list):
        fabric = GhostFabric(self.game, self)
        for y in range(self.matrix_height):
            for x in range(self.matrix_width):
                object_char = level_objects_list[y][x]
                if object_char == 'G':
                    ghost = fabric.get_next(x, y)
                    # Добавление матричной точки призрака
                    ghost = SimpleMatrixPoint(x, y, 'ghost', ghost)
                    self.ghosts.append(ghost)
                    self.matrix[y][x].update_moving_object(ghost)

    def additional_logic(self) -> None:
        self.pacmans_count = len(
            list(filter(lambda x: x.obj.alive, self.pacmans)))
        self.ghosts_count = len(
            list(filter(lambda x: x.obj.alive, self.ghosts)))
        self.seeds_count = len(list(filter(lambda x: x.obj.alive,
                                           self.seeds + self.super_seeds)))

        self.check_ghosts_activity()

        self.check_matrix_positions(self.pacmans)
        self.check_matrix_positions(self.ghosts)

        for pacman in self.pacmans:
            self.check_collisions_with_pacman(pacman)

    def check_ghosts_activity(self):
        for ghost in self.ghosts:
            ghost = ghost.obj
            if not ghost.active:
                if self.current_ghost_cd >= MatrixMap.GHOST_ACTIVATION_CD:
                    self.current_ghost_cd = 0
                    ghost.activate()
                else:
                    self.current_ghost_cd += 1

    def check_collisions_with_pacman(self, pacman: SimpleMatrixPoint):
        x = pacman.x
        y = pacman.y
        m_points = [self.matrix[y][x]]
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
            if m_obj.type == 'ghost':
                if pacman.obj.collision(m_obj.obj):
                    m_obj.obj.collision_reaction(pacman.obj)

    def pacman_collisions_with_static_objects(self, pacman: SimpleMatrixPoint,
                                              m_points):
        self.check_turn_ways(pacman, m_points)
        for m_point in m_points:
            s_obj = m_point.static_obj
            if s_obj.type == 'wall' or s_obj.type == 'wall_ghost_in':
                pass
            elif s_obj.type == 'teleport':
                s_obj.obj.check_collisions_with_entries(pacman.obj)
            elif not s_obj.type == '':
                if pacman.obj.collision_with_small_sprite(s_obj.obj):
                    s_obj.obj.collision_reaction()
                    self.remove_static_object_from_matrix(m_point)

    def check_turn_ways(self, pacman: SimpleMatrixPoint, m_points):
        ways = [0, 0, 0, 0]
        p_obj = pacman.obj
        for m_point in m_points:
            s_obj = m_point.static_obj
            if s_obj.type != 'wall' and s_obj.type != 'wall_ghost_in':
                x = s_obj.x - pacman.x
                y = s_obj.y - pacman.y
                if x >= 1:
                    ways[0] = 1
                if y <= -1:
                    ways[1] = 1
                if x <= -1:
                    ways[2] = 1
                if y >= 1:
                    ways[3] = 1
        pacman.obj.update_turn_ways(ways)

    def check_matrix_positions(self, objects):
        for m_obj in objects:
            field_real_x = m_obj.x * CELL_SIZE + CELL_SIZE // 2
            field_real_y = m_obj.y * CELL_SIZE + CELL_SIZE // 2
            real_x = m_obj.obj.rect.x + CELL_SIZE // 2 - self.game.REAL_FIELD_X
            real_y = m_obj.obj.rect.y + CELL_SIZE // 2 - self.game.REAL_FIELD_Y
            if abs(field_real_x - real_x) >= CELL_SIZE or \
                abs(field_real_y - real_y) >= CELL_SIZE:
                self.change_pos_in_matrix(m_obj, real_x // CELL_SIZE,
                                          real_y // CELL_SIZE)
                if abs(field_real_x - real_x) <= CELL_SIZE and \
                    abs(field_real_y - real_y) <= CELL_SIZE:
                    self.correct_real_pos(m_obj)

    def change_pos_in_matrix(self, m_point: SimpleMatrixPoint, new_x, new_y):
        self.remove_moving_object_from_matrix(m_point)
        if new_x > 0 and new_y > 0 and new_x < self.matrix_width and new_y < self.matrix_height:
            self.matrix[new_y][new_x].update_moving_object(m_point)
            m_point.x = new_x
            m_point.y = new_y

    def get_matrix_pos(self, x=0, y=0):
        x = (x - self.game.REAL_FIELD_X) // CELL_SIZE
        y = (y - self.game.REAL_FIELD_Y) // CELL_SIZE
        return x, y

    def correct_real_pos(self, m_point: SimpleMatrixPoint):
        x, y = self.get_real_pos(m_point.x, m_point.y)
        m_point.obj.set_position(x, y)

    def get_real_pos(self, x=0, y=0):
        x = self.game.REAL_FIELD_X + x * CELL_SIZE
        y = self.game.REAL_FIELD_Y + y * CELL_SIZE
        return x, y

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
            [wall.process_draw() for wall in self.walls_ghosts_in]
            [bg_wall.process_draw() for bg_wall in self.bg_walls]
            [seed.process_draw() for seed in self.seeds]
            [super_seed.process_draw() for super_seed in self.super_seeds]
            # self.first = False
        super(MatrixMap, self).process_draw()
