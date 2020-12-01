from objects.image import ImageObject
from queue import Queue
from enum import Enum
from random import choice as choose_random
from constants import *

MAIN_SCENE = 3


class Status(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2


def is_empty(cell) -> bool:
    cell_type = cell.static_obj.type
    return not (cell_type == 'wall' or cell_type == 'teleport')


def is_teleport(cell) -> bool:
    return cell.static_obj.type == 'teleport'


def find_neighbours(matrix: list, cell_row: int, cell_column: int, checker=is_empty) -> list:
    height = len(matrix)
    width = len(matrix[0]) if height > 0 else 0
    neighbours = []
    if cell_row < height - 1 and checker(matrix[cell_row + 1][cell_column]):
        neighbours.append((cell_row + 1, cell_column))
    if cell_row > 0 and checker(matrix[cell_row - 1][cell_column]):
        neighbours.append((cell_row - 1, cell_column))
    if cell_column < width - 1 and checker(matrix[cell_row][cell_column + 1]):
        neighbours.append((cell_row, cell_column + 1))
    if cell_column > 0 and checker(matrix[cell_row][cell_column - 1]):
        neighbours.append((cell_row, cell_column - 1))
    return neighbours


# Преобразовывает игровое поле в граф в формате списка смежности
def process_level(level, field_point: tuple) -> dict:
    height = level.matrix_height
    width = level.matrix_width
    matrix = level.matrix
    graph = {(i, j): [] for i in range(height) for j in range(width)}
    for row in range(height):
        for column in range(width):
            cell = matrix[row][column]
            if is_empty(cell):
                graph[(row, column)] = find_neighbours(matrix, row, column)
    for teleport in level.teleports:
        cell_1 = ((teleport.points[0].rect.y - field_point[1]) // CELL_SIZE,
                  (teleport.points[0].rect.x - field_point[0]) // CELL_SIZE)
        cell_2 = ((teleport.points[1].rect.y - field_point[1]) // CELL_SIZE,
                  (teleport.points[1].rect.x - field_point[0]) // CELL_SIZE)
        neighbours_1 = find_neighbours(matrix, *cell_1)
        neighbours_2 = find_neighbours(matrix, *cell_2)
        for cell in neighbours_1:
            graph[cell] += neighbours_2
        for cell in neighbours_2:
            graph[cell] += neighbours_1
    return graph


def bfs(graph: dict, start: tuple, end: tuple, width: int, height: int) -> tuple:  # Граф - список смежности
    queue = Queue()
    queue.put(start)
    used = {(x, y): False for x in range(height) for y in range(width)}
    distances = {(x, y): 0 for x in range(height) for y in range(width)}
    parents = dict()
    used[start] = True
    parents[start] = -1
    if start == end:
        found = True
    else:
        found = False
    while not queue.empty() and not found:
        vertex = queue.get()
        for neighbour in graph[vertex]:
            if not used[neighbour]:
                used[neighbour] = True
                queue.put(neighbour)
                distances[neighbour] = distances[vertex] + 1
                parents[neighbour] = vertex
            if neighbour == end:
                found = True
    return parents, found


def find_path(graph: dict, start: tuple, end: tuple, width: int, height: int) -> list:  # Граф - список смежности
    parents, found = bfs(graph, start, end, width, height)
    if not found or start == end:
        return [start]
    path = [end]
    parent = parents[end]
    while parent != -1:
        path.append(parent)
        parent = parents[parent]
    path.reverse()
    return path[1:]


class Ghost(ImageObject):
    status = Status.CHASE
    score_for_kill = 10
    CHASE_TIME = 50  # время в тиках
    chase_timer = 0
    SCATTER_TIME = 50
    scatter_timer = 0
    FRIGHTENED_TIME = 50
    frightened_timer = 0
    PACMAN_CHOICE_TIME = 200
    pacman_choice_timer = 0
    speed = GHOST_SPEED  # расстояние, которое проходит призрак за 1 тик
    ticks_per_cell = CELL_SIZE // GHOST_SPEED  # количество тиков на прохождение клетки
    current_ticks = 0  # количество тиков, прошедших с начала движения из предыдущей клетки
    is_teleporting = False  # телепортируется ли сейчас призрак, нужно для обработки движения
    teleport_cells = [(-1, -1), (-1, -1)]  # координаты телепортов для случая is_teleporting == True
    active = False  # вышел ли призрак из спавна

    def __init__(self, game, y: int, x: int,  # x и y - номера строки и столбца клетки спавна
                 matrix_map, respawn: bool = True):
        self.FIELD_POINT = (game.REAL_FIELD_X, game.REAL_FIELD_Y)
        self.level = matrix_map
        self.matrix = self.level.matrix
        self.graph = process_level(self.level, self.FIELD_POINT)
        self.pacmans = self.level.pacmans
        self.current_pacman = choose_random(self.pacmans)
        self.spawn = (x, y)
        self.cell = (x, y)
        self.respawn = respawn
        self.next_cell = (x, y)
        rx, ry = self.get_real_position(self.cell)
        super().__init__(game, x=rx, y=ry, animation=Textures.GHOST['default'])
        self.target = self.cell  # клетка, к которой будет пытаться двигаться призрак
        self.path = [self.target]  # путь до цели, вычисляется с помощью find_path
        self.corners = self.find_corners()

    @classmethod
    def scary_mode_on(cls) -> None:
        cls.status = Status.FRIGHTENED

    def activate(self):
        self.active = True

    def get_cell(self, position: tuple) -> tuple:
        x = (position[1] - self.FIELD_POINT[1]) // CELL_SIZE
        y = (position[0] - self.FIELD_POINT[0]) // CELL_SIZE
        return x, y

    def get_real_position(self, cell: tuple) -> tuple:
        x = self.FIELD_POINT[0] + cell[1] * CELL_SIZE
        y = self.FIELD_POINT[1] + cell[0] * CELL_SIZE
        return x, y

    def collision_reaction(self, pacman) -> None:
        if Ghost.status == Status.FRIGHTENED:
            self.die()
        else:
            pacman.die()

    def pacman_position(self) -> tuple:
        return self.current_pacman.y, self.current_pacman.x

    def find_corners(self) -> list:
        height = self.level.matrix_height
        width = self.level.matrix_width
        corners = [(0, 0) for _i in range(4)]
        for i in range(width + height - 1):  # i - индекс диагонали
            for j in range(i):
                if corners[0] == (0, 0) and j < height and i - j < width \
                        and is_empty(self.matrix[j][i - j]):
                    corners[0] = j, i - j
                if corners[1] == (0, 0) and j < height and width - i - 1 + j > 0 \
                        and is_empty(self.matrix[j][width - i - 1 + j]):
                    corners[1] = j, width - i - 1 + j
                if corners[2] == (0, 0) and height - j - 1 > 0 and i - j < width \
                        and is_empty(self.matrix[height - j - 1][i - j]):
                    corners[2] = height - j - 1, i - j
                if corners[3] == (0, 0) and height - j - 1 > 0 and width - i - 1 + j > 0 \
                        and is_empty(self.matrix[height - j - 1][width - i - 1 + j]):
                    corners[3] = height - j - 1, width - i - 1 + j
        return corners

    def die(self) -> None:
        self.game.add_scores(self.score_for_kill)
        if not self.respawn:
            del self
            return
        self.set_position(*self.get_real_position(self.spawn))
        self.alive = False

    def get_chase_target(self) -> tuple:
        return self.pacman_position()

    def get_next_cell(self) -> tuple:
        height = self.level.matrix_height
        width = self.level.matrix_width
        if not self.alive:
            self.target = self.spawn
        elif self.status != Status.CHASE and self.target in self.corners and len(self.path) >= 2:
            self.path = self.path[1:]
            return self.path[0]
        elif self.status != Status.CHASE:
            self.target = choose_random(self.corners)
        else:
            self.target = self.get_chase_target()
        self.path = find_path(self.graph, self.cell, self.target, width, height)
        return self.path[0]

    # Проверяет, соединены ли текущая и следующая клетки телепортом и если да, то находит каким
    def check_teleport(self) -> None:
        if abs(self.cell[0] - self.next_cell[0]) + abs(self.cell[1] - self.next_cell[1]) <= 1:
            self.is_teleporting = False
            return
        self.is_teleporting = True
        into_teleports = find_neighbours(self.matrix, self.cell[0], self.cell[1], is_teleport)
        out_teleports = find_neighbours(self.matrix, self.next_cell[0], self.next_cell[1], is_teleport)
        for into in into_teleports:
            for out in out_teleports:
                if self.matrix[into[0]][into[1]].static_obj.obj == self.matrix[out[0]][out[1]].static_obj.obj:
                    self.teleport_cells = (into, out)
                    return

    def process_teleport(self) -> None:
        if self.get_cell((self.rect.centerx, self.rect.centery)) == self.cell:
            self.move((self.teleport_cells[0][1] - self.cell[1]) * self.speed,
                      (self.teleport_cells[0][0] - self.cell[0]) * self.speed)
        else:
            self.cell = self.teleport_cells[1]
            self.is_teleporting = False
            self.current_ticks -= 1

    def process_movement(self) -> None:
        if self.current_ticks == self.ticks_per_cell:
            self.cell = self.next_cell
            self.set_position(*self.get_real_position(self.cell))
            self.next_cell = self.get_next_cell()
            self.check_teleport()
            self.current_ticks = 0
        if self.is_teleporting:
            self.process_teleport()
        else:
            self.move((self.next_cell[1] - self.cell[1]) * self.speed,
                      (self.next_cell[0] - self.cell[0]) * self.speed)
        self.current_ticks += 1

    def process_statuses(self):
        if self.status == Status.CHASE:
            self.chase_timer += 1
            if self.chase_timer >= self.CHASE_TIME:
                self.status = Status.SCATTER
                self.chase_timer = 0
        elif self.status == Status.SCATTER:
            self.scatter_timer += 1
            if self.scatter_timer >= self.SCATTER_TIME:
                self.status = Status.CHASE
                self.scatter_timer = 0
        else:
            self.frightened_timer += 1
            if self.frightened_timer >= self.FRIGHTENED_TIME:
                self.status = Status.CHASE
                self.scatter_timer = 0
                self.chase_timer = 0
                self.scatter_timer = 0

    def process_logic(self) -> None:
        if not self.active:
            return
        if not self.alive and self.cell == self.spawn:
            self.alive = True
        self.process_statuses()
        self.pacman_choice_timer += 1
        if self.pacman_choice_timer >= self.PACMAN_CHOICE_TIME:
            self.current_pacman = choose_random(self.pacmans)
        self.process_movement()


class Blinky(Ghost):
    """Целевой клеткой всегда является пакман, даже в режиме разбегания.
    Красного цвета."""

    def __init__(self, game, x: int, y: int, respawn: bool):
        super().__init__(game, x, y, respawn)
        self.SCATTER_TIME = 0

class Pinky(Ghost):
    """Целевой клеткой является позиция на 4 клетки впереди пакмана.
    Розового цввета."""

    def __init__(self, game, x: int, y: int, respawn: bool):
        super().__init__(game, x, y, respawn)

    def process_logic(self):
        super().process_logic()
        pass  # TODO


class Inky(Ghost):
    """Целевая клетка зависит от положения Блинки и пакмана.
    Начинает погоню только после того, как пакман съест 30 точек.
    Синего цвета."""

    def __init__(self, game, x: int, y: int, respawn: bool, blinky: Ghost):
        super().__init__(game, x, y, respawn)
        self.blinky = blinky

    def process_logic(self):
        super().process_logic()
        pass  # TODO


class Clyde(Ghost):
    """Целевой клеткой является пакман, когда Клайд на расстоянии не более 8 клеток от него.
    В остальное время находится в режиме разбегания.
    Начинает погоню только после того, как пакман съест 1/3 всех точек.
    Оранжевого цвета."""

    def __init__(self, game, x: int, y: int, level, respawn: bool):
        super().__init__(game, x, y, respawn)

    def process_logic(self):
        super().process_logic()
        pass  # TODO
