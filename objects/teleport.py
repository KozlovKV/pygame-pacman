from objects import ImageObject


class TeleportObject:
    def __init__(self, game, x1, y1, x2, y2):
        self.game = game
        self.point1 = ImageObject(game, './resources/teleport/teleport_0.png',
                                  x1, y1, 2,
                                  './resources/teleport/teleport_[F].png')
        self.point2 = ImageObject(game, './resources/teleport/teleport_0.png',
                                  x2, y2, 2,
                                  './resources/teleport/teleport_[F].png')
        self.last_teleported_object = None

    def check_collisions_with_entries(self, obj: ImageObject):
        pass

    def collision_reaction(self, obj: ImageObject):
        pass
