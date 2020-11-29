from constants import Textures
from objects.image import ImageObject


class Seed(ImageObject):
    def __init__(self, game, x, y):
        super().__init__(game, Textures.SEED, x, y)

    def collision_reaction(self):
        self.game.add_scores(1)
        self.die()
