from objects import ImageObject


class TeleportObject:
    def __init__(self, game, x1, y1, x2, y2):
        self.game = game
        self.points = [
            ImageObject(self.game, './resources/images/teleport/teleport_0.png',
                        x1, y1, 2, './resources/images/teleport/teleport_[F].png'),
            ImageObject(self.game, './resources/images/teleport/teleport_0.png',
                        x2, y2, 2, './resources/images/teleport/teleport_[F].png'),
        ]

        self.time_from_teleported = 0
        self.last_teleported_object = None

    def process_event(self, event):
        pass

    def process_logic(self):
        [p.next_frame() for p in self.points]
        if self.last_teleported_object is not None:
            self.time_from_teleported += self.game.TICK
        if self.time_from_teleported >= self.game.TICK*30:
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

    def process_draw(self):
        [p.process_draw() for p in self.points]
