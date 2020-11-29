from constants import Color
from objects.button import ButtonObject
from objects.switcher import ArrowSwitcher
from scenes import BaseScene


class SettingsScene(BaseScene):
    def create_objects(self) -> None:
        lvl_count = 10
        lvl_skin = 34
        settings_1 = ("lvl: "+str(i) for i in range(lvl_count+1))
        settings_2 = ('Mode: score_cup', 'Mode: survival', 'Mode: hunt')
        settings_3 = ('Coop: False', 'Coop: True')
        settings_6 = ('Pacman skin: classic',
                      'Pacman skin: bordered',
                      'Pacman skin: inverted',
                      'Pacman skin: ghost',
                      )
        settings_7 = ('LvL texture: '+str(i) for i in range(lvl_skin+1))
        self.objects.append(ButtonObject(self.game, 10, 600, 230, 40, Color.SOFT_RED,
                                         self.game.exit_game, 'EXIT'))
        self.objects.append(ArrowSwitcher(self.game,
                                          100, 10, 600, 50,
                                          Color.WHITE, Color.SOFT_RED,
                                          0, *settings_1))
        self.objects.append(ArrowSwitcher(self.game,
                                          100, 70, 600, 50,
                                          Color.WHITE, Color.ORANGE,
                                          0, *settings_2))
        self.objects.append(ArrowSwitcher(self.game,
                                          100, 130, 600, 50,
                                          Color.WHITE, Color.YELLOW,
                                          0, *settings_3))
        self.objects.append(ArrowSwitcher(self.game,
                                          100, 190, 600, 50,
                                          Color.WHITE, Color.BLUE,
                                          0, *settings_6))
        self.objects.append(ArrowSwitcher(self.game,
                                          100, 250, 600, 50,
                                          Color.WHITE, Color.PURPLE,
                                          0, *settings_7))
        self.objects.append(ButtonObject(self.game, 100, 310, 600, 40, Color.SOFT_RED,
                                         self.game.set_test_scene, 'TO TEST MENU'))

    def process_logic(self) -> None:
        self.game.settings['level'] = int(self.objects[1].get_current_value().split(': ')[1])
        self.game.settings['mode'] = self.objects[2].get_current_value().split(': ')[1]
        self.game.settings['coop'] = self.objects[3].get_current_value().split(': ')[1] == 'True'
        self.game.settings['pacman_texture'] = self.objects[4].get_current_value().split(': ')[1]
        self.game.settings['lvl_texture'] = int(self.objects[5].get_current_value().split(': ')[1])
