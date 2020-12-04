from constants import Textures
from objects.image import ImageObject


class TeleportObject:
    KEEP_TELEPORTED_OBJECT = 30

    def __init__(self, game, x1, y1, x2, y2):
        self.game = game
        self.points = [
            ImageObject(self.game, x=x1, y=y1, animation=Textures.TELEPORT),
            ImageObject(self.game, x=x2, y=y2, animation=Textures.TELEPORT),
        ]

        self.time_from_teleported = 0
        self.last_teleported_object = None

    def process_event(self, event):
        pass

    def process_logic(self):
        if self.last_teleported_object is not None:
            self.time_from_teleported += 1
        if self.time_from_teleported >= TeleportObject.KEEP_TELEPORTED_OBJECT:
            self.time_from_teleported = 0
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
