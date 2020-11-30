from objects import ImageObject


class SuperSeed(ImageObject):
    def __init__(self, game, filename, x, y):
        super().__init__(game, filename, x, y)

    def collision_reaction(self):
        self.die()
        self.game.add_scores(10)
        self.scary_mode_on()
