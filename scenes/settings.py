from constants import Color
from objects.button import ButtonObject
from objects.switcher import ArrowSwitcher
from scenes import BaseScene


class SettingsScene(BaseScene):
    def __int__(self, game):
        self.lvl_config = None
        self.mode_config = None
        self.coop_config = None
        self.pacman_config = None
        self.background_config = None
        super().__init__(game)

    def create_objects(self) -> None:
        lvl_count = 10
        lvl_skin = 34
        settings_1 = ("lvl: " + str(i) for i in range(lvl_count + 1))
        settings_2 = ('Mode: score_cup', 'Mode: survival', 'Mode: hunt')
        settings_3 = ('Coop: False', 'Coop: True')
        settings_6 = ('Pacman skin: classic',
                      'Pacman skin: bordered',
                      'Pacman skin: inverted',
                      'Pacman skin: ghost',
                      )
        settings_7 = ('LvL texture: ' + str(i) for i in range(lvl_skin + 1))
        self.objects.append(ButtonObject(self.game, 10, 600, 230, 40, Color.SOFT_RED,
                                         self.game.exit_game, 'EXIT'))
        self.lvl_config = (ArrowSwitcher(self.game,
                                         100, 10, 600, 50,
                                         Color.WHITE, Color.SOFT_RED,
                                         0, *settings_1))
        self.mode_config = (ArrowSwitcher(self.game,
                                          100, 70, 600, 50,
                                          Color.WHITE, Color.ORANGE,
                                          0, *settings_2))
        self.coop_config = (ArrowSwitcher(self.game,
                                          100, 130, 600, 50,
                                          Color.WHITE, Color.YELLOW,
                                          0, *settings_3))
        self.pacman_config = (ArrowSwitcher(self.game,
                                            100, 190, 600, 50,
                                            Color.WHITE, Color.BLUE,
                                            0, *settings_6))
        self.background_config = (ArrowSwitcher(self.game,
                                                100, 250, 600, 50,
                                                Color.WHITE, Color.PURPLE,
                                                0, *settings_7))
        self.objects.append(self.lvl_config)
        self.objects.append(self.mode_config)
        self.objects.append(self.coop_config)
        self.objects.append(self.pacman_config)
        self.objects.append(self.background_config)
        self.objects.append(ButtonObject(self.game, 100, 310, 600, 40, Color.SOFT_RED,
                                         self.game.set_test_scene, 'TO TEST MENU'))

    def process_logic(self) -> None:
        self.game.settings['level'] = int(self.lvl_config.get_current_value().split(': ')[1])
        self.game.settings['mode'] = self.mode_config.get_current_value().split(': ')[1]
        self.game.settings['coop'] = self.coop_config.get_current_value().split(': ')[1] == 'True'
        self.game.settings['pacman_texture'] = self.pacman_config.get_current_value().split(': ')[1]
        self.game.settings['lvl_texture'] = int(self.background_config.get_current_value().split(': ')[1])
