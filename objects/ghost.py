from objects import ImageObject
from queue import Queue
from enum import Enum


WALL_SYMBOL = '#'


class Status(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2


def is_empty(cell: chr) -> bool:
    return not (cell == WALL_SYMBOL or str.isnumeric(cell))


def find_neighbours(matrix: list, cell_row: int, cell_column: int, width: int, height: int):
    cell = matrix[cell_row][cell_column]
    if not is_empty(cell):
        return []
    neighbours = []
    if cell_row < height - 1 and is_empty(matrix[cell_row + 1][cell_column]):
        neighbours.append((cell_row + 1) * width + cell_column)
    if cell_row > 0 and is_empty(matrix[cell_row - 1][cell_column]):
        neighbours.append((cell_row - 1) * width + cell_column)
    if cell_column < width - 1 and is_empty(matrix[cell_row][cell_column + 1]):
        neighbours.append(cell_row * width + (cell_column + 1))
    if cell_column > 0 and is_empty(matrix[cell_row][cell_column - 1]):
        neighbours.append(cell_row * width + (cell_column - 1))
    return neighbours


# Преобразовывает игровое поле в граф в формате списка смежности
def process_level(level_file_name) -> list:
    with open(level_file_name, 'r') as level:
        width = int(level.readline().split(': ')[1])
        height = int(level.readline().split(': ')[1])
        matrix = [line.split() for line in level.readlines()]
    graph = [[] for _i in range(width * height)]
    teleports = dict()  # сопоставляет номеру пару клеток, связанных телепортом
    for cell_row in range(height):
        for cell_column in range(width):
            cell = matrix[cell_row][cell_column]
            graph[cell_row * width + cell_column] = find_neighbours(matrix, cell_row, cell_column, width, height)
            if str.isnumeric(cell):
                teleports[int(cell)] = teleports.get(int(cell), list())
                teleports[int(cell)].append((cell_row, cell_column))
    for pair in teleports.values():
        first_neighbours = find_neighbours(matrix, pair[0][0], pair[0][1], width, height)
        first_cell = first_neighbours[0] if len(first_neighbours) > 0 else 0
        second_neighbours = find_neighbours(matrix, pair[-1][0], pair[-1][1], width, height)
        second_cell = second_neighbours[0] if len(first_neighbours) > 0 else 0
        graph[first_cell].append(second_cell)  # FIXME изменить в зависимости от того, как работает телепорт
        graph[second_cell].append(first_cell)  # FIXME
    return graph


def bfs(graph: list, start: int, end: int) -> list:
    vertex_number = len(graph)
    queue = Queue()
    queue.put(start)
    used = [0 for _i in range(vertex_number)]
    distances = [0 for _i in range(vertex_number)]
    parents = [0 for _i in range(vertex_number)]
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
    return parents


def find_path(graph: list, start: int, end: int) -> list:  # Формат графа - список смежности
    parents = bfs(graph, start, end)
    path = [end]
    parent = parents[end]
    while parent != -1:
        path.append(parent)
        parent = parents[parent]
    path.reverse()
    return path


class Ghost(ImageObject):
    status = Status.CHASE

    def __init__(self, game, filename: str, x: int, y: int, level: str):  # level - имя файла с уровнем
        super().__init__(game, filename, x, y)
        self.level = process_level(level)
        self.pacman = game.pacman

    def process_logic(self):
        pass  # TODO


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
