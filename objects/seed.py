from constants import Textures, Sounds
from objects.image import ImageObject


class Seed(ImageObject):
    sound_i = 0

    def __init__(self, game, x, y):
        super().__init__(game, Textures.SEED, x, y,
                         hided_sprite_w=10, hided_sprite_h=10)

    def collision_reaction(self):
        Seed.sound_i = (Seed.sound_i + 1) % 2
        Sounds.SIREN.set_volume(0.5)
        Sounds.SEED[Seed.sound_i].play()
        self.game.add_scores(1)
        self.die()
