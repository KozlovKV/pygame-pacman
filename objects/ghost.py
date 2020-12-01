from objects.image import ImageObject
from queue import Queue
from enum import Enum
from random import choice as choose_random
from constants import *
from objects.matrix_map import MatrixMap

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
def process_level(level: MatrixMap, field_point: tuple) -> dict:
    matrix = level.matrix
    graph = dict()
    for row in matrix:
        for column in row:
            cell = matrix[row][column]
            if is_empty(cell):
                graph[(row, column)] = find_neighbours(matrix, row, column)
    for teleport in level.teleports:
        cell_1 = ((teleport.points[0][1] - field_point[1]) // CELL_SIZE,
                  (teleport.points[0][0] - field_point[0]) // CELL_SIZE)
        cell_2 = ((teleport.points[1][1] - field_point[1]) // CELL_SIZE,
                  (teleport.points[1][0] - field_point[0]) // CELL_SIZE)
        neighbours_1 = find_neighbours(matrix, *cell_1)
        neighbours_2 = find_neighbours(matrix, *cell_2)
        for cell in neighbours_1:
            graph[cell].append(neighbours_2)
        for cell in neighbours_2:
            graph[cell].append(neighbours_1)
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
    CHASE_TIME = 300  # время в тиках
    chase_timer = 0
    SCATTER_TIME = 500
    scatter_timer = 0
    FRIGHTENED_TIME = 100
    frightened_timer = 0
    PACMAN_CHOICE_TIME = 200
    pacman_choice_timer = 0
    speed = GHOST_SPEED  # расстояние, которое проходит призрак за 1 тик
    ticks_per_cell = CELL_SIZE // GHOST_SPEED  # количество тиков на прохождение клетки
    current_ticks = 0  # количество тиков, прошедших с начала движения из предыдущей клетки
    is_teleporting = False  # телепортируется ли сейчас призрак, нужно для обработки движения
    teleport_cells = [(-1, -1), (-1, -1)]  # координаты телепортов для случая is_teleporting == True

    def __init__(self, game, filename: str, x: int, y: int,  # x и y - номера строки и столбца клетки спавна
                 level: MatrixMap, respawn: bool = True):
        super().__init__(game, filename)
        self.FIELD_POINT = (game.REAL_FIELD_X, game.REAL_FIELD_Y)
        self.level = level
        self.matrix = level.matrix
        self.graph = process_level(self.level, self.FIELD_POINT)
        self.pacmans = level.pacmans
        self.current_pacman = choose_random(self.pacmans)
        self.spawn = (x, y)
        self.cell = (x, y)
        self.respawn = respawn
        self.next_cell = (x, y)
        self.set_position(*self.get_real_position(self.cell))
        self.target = self.cell  # клетка, к которой будет пытаться двигаться призрак
        self.path = [self.target]  # путь до цели, вычисляется с помощью find_path

    @classmethod
    def scary_mode_on(cls):
        cls.status = Status.FRIGHTENED

    def get_cell(self, position: tuple) -> tuple:
        x = (position[1] - self.FIELD_POINT[1]) // CELL_SIZE
        y = (position[0] - self.FIELD_POINT[0]) // CELL_SIZE
        return x, y

    def get_real_position(self, cell: tuple) -> tuple:
        x = self.FIELD_POINT[0] + cell[1] * CELL_SIZE
        y = self.FIELD_POINT[1] + cell[0] * CELL_SIZE
        return x, y

    def collision_reaction(self, pacman) -> None:
        if self.status == Status.FRIGHTENED:
            self.die()
        else:
            pacman.die()

    def pacman_position(self) -> tuple:
        return self.current_pacman.y, self.current_pacman.x

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
        corners = [(0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)]
        if not self.alive:
            self.target = self.spawn
        elif self.status != Status.CHASE and self.target in corners and len(self.path) > 0:
            self.path = self.path[1:]
            return self.path[0]
        elif self.status != Status.CHASE:
            self.target = choose_random(corners)
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
                if self.matrix[into[0]][into[1]].obj == self.matrix[out[0]][out[1]].obj:
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

    @classmethod
    def process_statuses(cls):
        if cls.status == Status.CHASE:
            cls.chase_timer += 1
            if cls.chase_timer >= cls.CHASE_TIME:
                cls.status = Status.SCATTER
                cls.chase_timer = 0
        elif cls.status == Status.SCATTER:
            cls.scatter_timer += 1
            if cls.scatter_timer >= cls.SCATTER_TIME:
                cls.status = Status.CHASE
                cls.scatter_timer = 0
        else:
            cls.frightened_timer += 1
            if cls.frightened_timer >= cls.FRIGHTENED_TIME:
                cls.status = Status.CHASE
                cls.scatter_timer = 0
                cls.chase_timer = 0
                cls.scatter_timer = 0

    def process_logic(self) -> None:
        if not self.alive and self.cell == self.spawn:
            self.alive = True
        Ghost.process_statuses()
        self.pacman_choice_timer += 1
        if self.pacman_choice_timer >= self.PACMAN_CHOICE_TIME:
            self.current_pacman = choose_random(self.pacmans)
        self.process_movement()


class Blinky(Ghost):
    """Целевой клеткой всегда является пакман, даже в режиме разбегания.
    Красного цвета."""

    def __init__(self, game, filename: str, x: int, y: int, level: MatrixMap, respawn: bool):
        super().__init__(game, filename, x, y, level, respawn)

    def process_logic(self):
        super().process_logic()
        pass  # TODO


class Pinky(Ghost):
    """Целевой клеткой является позиция на 4 клетки впереди пакмана.
    Розового цввета."""

    def __init__(self, game, filename: str, x: int, y: int, level: MatrixMap, respawn: bool):
        super().__init__(game, filename, x, y, level, respawn)

    def process_logic(self):
        super().process_logic()
        pass  # TODO


class Inky(Ghost):
    """Целевая клетка зависит от положения Блинки и пакмана.
    Начинает погоню только после того, как пакман съест 30 точек.
    Синего цвета."""

    def __init__(self, game, filename: str, x: int, y: int, level: MatrixMap, respawn: bool, blinky: Ghost):
        super().__init__(game, filename, x, y, level, respawn)
        self.blinky = blinky

    def process_logic(self):
        super().process_logic()
        pass  # TODO


class Clyde(Ghost):
    """Целевой клеткой является пакман, когда Клайд на расстоянии не более 8 клеток от него.
    В остальное время находится в режиме разбегания.
    Начинает погоню только после того, как пакман съест 1/3 всех точек.
    Оранжевого цвета."""

    def __init__(self, game, filename: str, x: int, y: int, level: MatrixMap, respawn: bool):
        super().__init__(game, filename, x, y, level, respawn)

    def process_logic(self):
        super().process_logic()
        pass  # TODO
