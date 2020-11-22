from objects.base import DrawableObject


class Seed(DrawableObject):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 10, 10, (233, 185, 149))
