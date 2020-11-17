from constants import Color
from objects import ButtonObject
from scenes import BaseScene


class SettingsScene(BaseScene):
    def create_objects(self) -> None:
        self.objects.append(ButtonObject(self.game, 10, 600, 200, 40, Color.RED,
                                         self.game.exit_game, 'EXIT'))
