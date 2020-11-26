from objects import ImageObject


class SuperSeed(ImageObject):
    def __init__(self, game, filename: str, x, y):
        super().__init__(game, filename, x, y)
