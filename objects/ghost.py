from objects import ImageObject
from queue import Queue
from enum import Enum


class Modes(Enum):
    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2


# Преобразовывает игровое поле в граф в формате списка смежности
def process_field(field) -> list:
    return field  # TODO


def bfs(graph: list, start: int, end: int) -> list:
    vertex_number = len(graph)
    queue = Queue()
    queue.put(start)
    used = [0 for i in range(vertex_number)]
    distances = [0 for i in range(vertex_number)]
    parents = [0 for i in range(vertex_number)]
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
    mode = Modes.CHASE

    def __init__(self, game, filename: str, x: int, y: int, field, pacman):
        super().__init__(game, filename, x, y)
        self.game = game
        self.field = process_field(field)
        self.pacman = pacman

    def process_logic(self):
        pass  # TODO


class Blinky(Ghost):
    """Целевой клеткой всегда является пакман, даже в режиме разбегания.
    Красного цвета."""

    def __init__(self, game, filename: str, x: int, y: int, field, pacman):
        super().__init__(game, filename, x, y, field, pacman)

    def process_logic(self):
        super().process_logic()
        pass  # TODO


class Pinky(Ghost):
    """Целевой клеткой является позиция на 4 клетки впереди пакмана.
    Розового цввета."""

    def __init__(self, game, filename: str, x: int, y: int, field, pacman):
        super().__init__(game, filename, x, y, field, pacman)

    def process_logic(self):
        super().process_logic()
        pass  # TODO


class Inky(Ghost):
    """Целевая клетка зависит от положения Блинки и пакмана.
    Начинает погоню только после того, как пакман съест 30 точек.
    Синего цвета."""

    def __init__(self, game, filename: str, x: int, y: int, field, pacman, blinky):
        super().__init__(game, filename, x, y, field, pacman)
        self.blinky = blinky

    def process_logic(self):
        super().process_logic()
        pass  # TODO


class Clyde(Ghost):
    """Целевой клеткой является пакман, когда Клайд на расстоянии не более 8 клеток от него.
    В остальное время находится в режиме разбегания.
    Начинает погоню только после того, как пакман съест 1/3 всех точек.
    Оранжевого цвета."""
    def __init__(self, game, filename: str, x: int, y: int, field, pacman):
        super().__init__(game, filename, x, y, field, pacman)

    def process_logic(self):
        super().process_logic()
        pass  # TODO
