from constants import Color
from objects import ButtonObject
from objects.switcher import ArrowSwitcher
from scenes import BaseScene


class SettingsScene(BaseScene):
    def create_objects(self) -> None:
        self.objects.append(ButtonObject(self.game, 10, 600, 200, 40, Color.SOFT_RED,
                                         self.game.exit_game, 'EXIT'))
        self.objects.append(ArrowSwitcher(self.game, 10, 10, 200, 50, Color.SOFT_RED, 0,
                                          'Var1', 'Var2', 'Var3'))
        self.objects.append(ArrowSwitcher(self.game, 10, 70, 200, 50, Color.GREEN, 1,
                                          'Var1', 'Var2', 'Var3'))
        self.objects.append(ArrowSwitcher(self.game, 10, 130, 200, 50, Color.BLUE, 2,
                                          'Var1', 'Var2', 'Var3'))
