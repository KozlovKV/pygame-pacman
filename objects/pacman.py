from objects import ImageObject


class Pacman(ImageObject):
    def __init__(self, game, filename: str, x: int, y: int):
        super().__init__(game, filename, x, y)
