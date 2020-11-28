from constants import Color
from objects import ButtonObject
from objects.switcher import ArrowSwitcher
from scenes import BaseScene


class SettingsScene(BaseScene):
    def create_objects(self) -> None:
        lvl_count = 10
        enemy_count = 10
        enemy_speed = 10
        pacman_skin = 5
        lvl_skin = 34
        settings_1 = ("lvl: "+str(i) for i in range(lvl_count+1))
        settings_2 = ('Mode: score_cup', 'Mode: survival', 'Mode: hunt')
        settings_3 = ('Coop: False', 'Coop: True')
        settings_4 = ('Ghosts count: '+str(i) for i in range(1, enemy_count+1))
        settings_5 = ('Ghosts speed: '+str(i) for i in range(1, enemy_speed+1))
        settings_6 = ('Pacman skin: ' + str(i) for i in range(pacman_skin + 1))
        settings_7 = ('LvL texture: '+str(i) for i in range(lvl_skin+1))
        self.objects.append(ButtonObject(self.game, 10, 600, 230, 40, Color.SOFT_RED,
                                         self.game.exit_game, 'EXIT'))
        self.objects.append(ArrowSwitcher(self.game,
                                          10, 10, 400, 50,
                                          Color.WHITE, Color.SOFT_RED,
                                          0, *settings_1))
        self.objects.append(ArrowSwitcher(self.game,
                                          10, 70, 400, 50,
                                          Color.WHITE, Color.ORANGE,
                                          0, *settings_2))
        self.objects.append(ArrowSwitcher(self.game,
                                          10, 130, 400, 50,
                                          Color.WHITE, Color.YELLOW,
                                          0, *settings_3))
        self.objects.append(ArrowSwitcher(self.game,
                                          10, 190, 400, 50,
                                          Color.WHITE, Color.GREEN,
                                          0, *settings_4))
        self.objects.append(ArrowSwitcher(self.game,
                                          10, 250, 400, 50,
                                          Color.WHITE, Color.SOFT_BLUE,
                                          3, *settings_5))
        self.objects.append(ArrowSwitcher(self.game,
                                          10, 310, 400, 50,
                                          Color.WHITE, Color.BLUE,
                                          0, *settings_6))
        self.objects.append(ArrowSwitcher(self.game,
                                          10, 370, 400, 50,
                                          Color.WHITE, Color.PURPLE,
                                          0, *settings_7))
        self.objects.append(ButtonObject(self.game, 10, 550, 230, 40, Color.SOFT_RED,
                                         self.game.set_test_scene, 'TO TEST MENU'))

    def process_logic(self) -> None:
        self.game.settings['level'] = int(self.objects[1].get_current_value().split(': ')[1])
        self.game.settings['mode'] = self.objects[2].get_current_value().split(': ')[1]
        self.game.settings['coop'] = self.objects[3].get_current_value().split(': ')[1] == 'True'
        self.game.settings['ghosts_count'] = int(self.objects[4].get_current_value().split(': ')[1])
        self.game.settings['ghosts_speed'] = int(self.objects[5].get_current_value().split(': ')[1])
        self.game.settings['pacman_texture'] = int(self.objects[6].get_current_value().split(': ')[1])
        self.game.settings['lvl_texture'] = int(self.objects[7].get_current_value().split(': ')[1])
