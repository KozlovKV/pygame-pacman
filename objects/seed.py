from objects import ImageObject
class Seed(ImageObject):
    def __init__(self, game, x, y, filename):
        super().__init__(game, x, y, filename)
    def collision_reaction(self):
        self.game.add_scores(1)
        self.die()
