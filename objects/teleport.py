from objects import ImageObject


class TeleportObject:
    def __init__(self, game, x1, y1, x2, y2):
        self.game = game
        self.points = [
            ImageObject(game, './resources/teleport/teleport_0.png',
                        x1, y1, 2, './resources/teleport/teleport_[F].png'),
            ImageObject(game, './resources/teleport/teleport_0.png',
                        x2, y2, 2, './resources/teleport/teleport_[F].png'),
        ]
        self.last_teleported_object = None

    def check_collisions_with_entries(self, obj: ImageObject):
        if self.last_teleported_object != obj:
            if self.points[0].collision(obj):
                self.teleport_object(1, obj)
            elif self.points[1].collision(obj):
                self.teleport_object(0, obj)

    def teleport_object(self, point_index, obj: ImageObject):
        self.last_teleported_object = obj
        obj.set_position(self.points[point_index].rect.x,
                         self.points[point_index].rect.y)
