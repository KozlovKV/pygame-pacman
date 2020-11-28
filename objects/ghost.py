from objects import ImageObject
from queue import Queue
from enum import Enum
from random import choice as choose_random

WALL_SYMBOL = '#'
MAIN_SCENE = 3


class Status(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2


def is_empty(cell: chr) -> bool:
    return not (cell == WALL_SYMBOL or str.isnumeric(cell))


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
def process_level(level_file_name) -> tuple:
    with open(level_file_name, 'r') as level:
        width = int(level.readline().split(': ')[1])
        height = int(level.readline().split(': ')[1])
        matrix = [line.split() for line in level.readlines()]
    graph = {(i, j): [] for i in range(height) for j in range(width)}
    teleports = dict()  # сопоставляет номеру пару клеток, связанных телепортом
    for cell_row in range(height):
        for cell_column in range(width):
            cell = matrix[cell_row][cell_column]
            if is_empty(cell):
                graph[(cell_row, cell_column)] = find_neighbours(matrix, cell_row, cell_column)
            elif str.isnumeric(cell):
                teleports[int(cell)] = teleports.get(int(cell), list())
                teleports[int(cell)].append((cell_row, cell_column))
    for pair in teleports.values():
        first_neighbours = find_neighbours(matrix, pair[0][0], pair[0][1])
        first_cell = first_neighbours[0] if len(first_neighbours) > 0 else (0, 0)
        second_neighbours = find_neighbours(matrix, pair[-1][0], pair[-1][1])
        second_cell = second_neighbours[0] if len(first_neighbours) > 0 else (0, 0)
        graph[first_cell].append(second_cell)
        graph[second_cell].append(first_cell)
    return matrix, graph


def bfs(graph: list, start: tuple, end: tuple, width: int, height: int) -> tuple:  # Граф - список смежности
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


def find_path(graph: list, start: tuple, end: tuple, width: int, height: int) -> list:  # Граф - список смежности
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

    def __init__(self, game, filename: str, x: int, y: int,  # x и y - номера строки и столбца клетки спавна
                 level: str, speed: int = 1):  # level - имя файла с уровнем
        super().__init__(game, filename)
        self.level, self.graph = process_level(level)
        self.pacmans = game.scenes[MAIN_SCENE].pacmans
        self.spawn = (x if x else 0, y if y else 0)
        self.cell = (x, y)
        self.CELL_SIZE = game.scenes[MAIN_SCENE].CELL_SIZE
        self.FIELD_POINT = game.scenes[MAIN_SCENE].FIELD_POINT
        self.speed = speed  # расстояние, которое проходит призрак за 1 тик
        self.ticks_per_cell = self.CELL_SIZE // speed  # количество тиков на прохождение клетки
        self.current_ticks = 0  # количество тиков, прошедших с начала движения из предыдущей клетки
        self.next_cell = (x, y)
        self.set_position(*self.get_real_position(self.cell))
        self.target = self.cell  # клетка, к которой будет пытаться двигаться призрак
        self.path = [self.target]  # путь до цели, вычисляется с помощью find_path
        self.is_teleporting = False  # телепортируется ли сейчас призрак, нужно для обработки движения
        self.teleport_cells = [(-1, -1), (-1, -1)]  # координаты телепортов для случая is_teleporting == True

    def get_real_position(self, cell):
        x = self.FIELD_POINT[0] + cell[1] * self.CELL_SIZE
        y = self.FIELD_POINT[1] + cell[0] * self.CELL_SIZE
        return x, y

    def check_collision(self):
        for pacman in self.pacmans:
            if self.collision(pacman):
                self.react_to_collision(pacman)

    def react_to_collision(self, pacman):
        if self.status == Status.FRIGHTENED:
            self.die()
        else:
            pacman.die()

    def die(self):
        self.set_position(*self.get_real_position(self.spawn))
        self.alive = False

    # Функция должна быть определена в потомках
    def get_target(self):
        return 0, 0

    def get_next_cell(self):
        height = len(self.level)
        width = len(self.level[0]) if height > 0 else 0
        corners = [(0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)]
        if self.status != Status.CHASE and self.target in corners and len(self.path) > 0:
            self.path = self.path[1:]
            return self.path[0]
        elif self.status != Status.CHASE:
            self.target = choose_random(corners)
        else:
            self.target = self.get_target()
        self.path = find_path(self.graph, self.cell, self.target, width, height)
        return self.path[0]

    # Проверяет, соединены ли текущая и следующая клетки телепортом и если да, то находит каким
    def check_teleport(self):
        if abs(self.cell[0] - self.next_cell[0]) + abs(self.cell[1] - self.next_cell[1]) <= 1:
            self.is_teleporting = False
            return
        self.is_teleporting = True
        into_teleports = find_neighbours(self.level, self.cell[0], self.cell[1], str.isnumeric)
        out_teleports = find_neighbours(self.level, self.next_cell[0], self.next_cell[1], str.isnumeric)
        for into in into_teleports:
            for out in out_teleports:
                if self.level[into[0]][into[1]] == self.level[out[0]][out[1]]:
                    self.teleport_cells = (into, out)
                    return

    def process_teleport(self):
        if self.current_ticks == self.ticks_per_cell // 2:
            out = self.teleport_cells[1]
            out_position = self.get_real_position(out)
            self.set_position(out_position[0] + (self.next_cell[1] - out[1]) * self.current_ticks,
                              out_position[1] + (self.next_cell[0] - out[0]) * self.current_ticks)
        elif self.current_ticks < self.ticks_per_cell // 2:
            self.move((self.teleport_cells[0][1] - self.cell[1]) * self.speed,
                      (self.teleport_cells[0][0] - self.cell[0]) * self.speed)
        else:
            self.move((self.next_cell[1] - self.teleport_cells[1][1]) * self.speed,
                      (self.next_cell[0] - self.teleport_cells[1][0]) * self.speed)

    def process_movement(self):
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

    def process_logic(self):
        if not self.alive:
            # TODO что-то делать с таймером
            return
        self.process_movement()


class Blinky(Ghost):
    """Целевой клеткой всегда является пакман, даже в режиме разбегания.
    Красного цвета."""

    def __init__(self, game, filename: str, x: int, y: int, level):
        super().__init__(game, filename, x, y, level)

    def process_logic(self):
        super().process_logic()
        pass  # TODO


class Pinky(Ghost):
    """Целевой клеткой является позиция на 4 клетки впереди пакмана.
    Розового цввета."""

    def __init__(self, game, filename: str, x: int, y: int, level):
        super().__init__(game, filename, x, y, level)

    def process_logic(self):
        super().process_logic()
        pass  # TODO


class Inky(Ghost):
    """Целевая клетка зависит от положения Блинки и пакмана.
    Начинает погоню только после того, как пакман съест 30 точек.
    Синего цвета."""

    def __init__(self, game, filename: str, x: int, y: int, level, blinky):
        super().__init__(game, filename, x, y, level)
        self.blinky = blinky

    def process_logic(self):
        super().process_logic()
        pass  # TODO


class Clyde(Ghost):
    """Целевой клеткой является пакман, когда Клайд на расстоянии не более 8 клеток от него.
    В остальное время находится в режиме разбегания.
    Начинает погоню только после того, как пакман съест 1/3 всех точек.
    Оранжевого цвета."""

    def __init__(self, game, filename: str, x: int, y: int, level):
        super().__init__(game, filename, x, y, level)

    def process_logic(self):
        super().process_logic()
        pass  # TODO
