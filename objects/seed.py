from objects import ImageObject
class Seed(ImageObject):
    def __init__(self, game, filename,x,y):
        super().__init__(game, filename,x,y)
    def collision_reaction(self):
        self.game.add_scores(1)
        self.die()
