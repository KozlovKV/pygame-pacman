from constants import Color
from objects.button import ButtonObject
from objects.highscore import HighScoresTable
from scenes import BaseScene


class HighScoresScene(BaseScene):
    def create_objects(self) -> None:
        button = ButtonObject(self.game, 300, 600, 200, 40, Color.SOFT_RED, self.game.set_menu_scene, 'RETURN')
        table = HighScoresTable(self.game, 400, 100)
        self.objects.append(button)
        self.objects.append(table)
