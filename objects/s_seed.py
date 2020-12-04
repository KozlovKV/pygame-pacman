from constants import Textures, Sounds
from objects.image import ImageObject


class SuperSeed(ImageObject):
    def __init__(self, game, x, y):
        super().__init__(game, Textures.SUPER_SEED, x, y,
                         hided_sprite_w=15, hided_sprite_h=15)

    def collision_reaction(self):
        self.die()
        Sounds.SUPER_SEED.play()
        self.game.add_scores(10)
        scene = self.game.scenes[self.game.current_scene_index]
        scene.scary_mode_on()
