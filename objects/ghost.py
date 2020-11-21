from objects import ImageObject
from queue import Queue


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
    def __init__(self, game, filename: str, x: int, y: int, field):
        super().__init__(game, filename, x, y)
        self.game = game
        self.field = process_field(field)

    def process_draw(self):
        super().process_draw()

    def process_logic(self):
        pass  # TODO
