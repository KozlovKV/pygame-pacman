from constants import Color, SETTINGS_PATH
from misc import write_json_to_file, read_json_from_file
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
        self.settings_strings = list()
        self.save_changes = True
        self.origins = False
        super().__init__(game)

    def create_objects(self) -> None:
        self.game.settings = read_json_from_file(SETTINGS_PATH)

        lvl_count = int(self.game.settings['lvl_count'])
        lvl_skin = int(self.game.settings['lvl_skin'])
        self.settings_1 = ["lvl: " + str(i) for i in range(lvl_count)]
        self.settings_2 = ['Mode: score_cup', 'Mode: survival', 'Mode: hunt']
        self.settings_3 = ['Coop: False', 'Coop: True']
        self.settings_4 = ['Pacman skin: classic',
                           'Pacman skin: bordered',
                           'Pacman skin: inverted',
                           'Pacman skin: ghost', ]
        self.settings_5 = ['LvL texture: ' + str(i) for i in range(lvl_skin)]
        self.settings_6 = ['Long turn buffer: True', 'Long turn buffer: False']

        self.lvl_config = (ArrowSwitcher(self.game,
                                         100, 10, 600, 50,
                                         Color.WHITE, Color.SOFT_RED,
                                         0, *self.settings_1))
        self.mode_config = (ArrowSwitcher(self.game,
                                          100, 70, 600, 50,
                                          Color.WHITE, Color.ORANGE,
                                          0, *self.settings_2))
        self.coop_config = (ArrowSwitcher(self.game,
                                          100, 130, 600, 50,
                                          Color.WHITE, Color.YELLOW,
                                          0, *self.settings_3))
        self.pacman_config = (ArrowSwitcher(self.game,
                                            100, 190, 600, 50,
                                            Color.WHITE, Color.GREEN,
                                            0, *self.settings_4))
        self.background_config = (ArrowSwitcher(self.game,
                                                100, 250, 600, 50,
                                                Color.WHITE, Color.BLUE,
                                                0, *self.settings_5))
        self.long_buffer_config = (ArrowSwitcher(self.game,
                                                 100, 310, 600, 50,
                                                 Color.WHITE, Color.PURPLE,
                                                 0, *self.settings_6))
        self.objects.append(self.lvl_config)
        self.objects.append(self.mode_config)
        self.objects.append(self.coop_config)
        self.objects.append(self.pacman_config)
        self.objects.append(self.background_config)
        self.objects.append(self.long_buffer_config)
        self.objects.append(ButtonObject(self.game, 100, 370, 600, 40, Color.SOFT_RED,
                                         self.game.set_test_scene, 'SAVE AND RETURN'))
        self.objects.append(ButtonObject(self.game, 100, 430, 600, 40, Color.SOFT_RED,
                                         self.quit_without_saving, 'RETURN'))
        self.objects.append(ButtonObject(self.game, 100, 490, 600, 40, Color.SOFT_RED,
                                         self.quit_and_defaults, 'DEFAULTS AND RETURN'))

    def quit_without_saving(self):
        self.save_changes = False
        self.game.set_test_scene()

    def quit_and_defaults(self):
        self.origins = True
        self.save_changes = False
        self.defaults = [0, 0, 0, 0, 0, 0, ]
        self.game.set_test_scene()

    def process_logic(self) -> None:
        pass
        # self.game.settings['level'] = int(self.lvl_config.get_current_value().split(': ')[1])
        # self.game.settings['mode'] = self.mode_config.get_current_value().split(': ')[1]
        # self.game.settings['coop'] = self.coop_config.get_current_value().split(': ')[1] == 'True'
        # self.game.settings['pacman_texture'] = self.pacman_config.get_current_value().split(': ')[1]
        # self.game.settings['field_texture'] = int(self.background_config.get_current_value().split(': ')[1])

    def on_activate(self) -> None:
        self.game.settings = read_json_from_file(SETTINGS_PATH)

        settings_1_f = [item.split(': ')[1] for item in self.settings_1]
        settings_2_f = [item.split(': ')[1] for item in self.settings_2]
        settings_3_f = [item.split(': ')[1] for item in self.settings_3]
        settings_4_f = [item.split(': ')[1] for item in self.settings_4]
        settings_5_f = [item.split(': ')[1] for item in self.settings_5]
        settings_6_f = [item.split(': ')[1] for item in self.settings_6]
        current_index_1 = 0
        current_index_2 = 0
        current_index_3 = 0
        current_index_4 = 0
        current_index_5 = 0
        current_index_6 = 0
        for value in range(len(settings_1_f)):
            if settings_1_f[value] == self.game.settings['level']:
                current_index_1 = value
        for value in range(len(settings_2_f)):
            if settings_2_f[value] == self.game.settings['mode']:
                current_index_2 = value
        for value in range(len(settings_3_f)):
            if settings_3_f[value] == self.game.settings['coop']:
                current_index_3 = value
        for value in range(len(settings_4_f)):
            if settings_4_f[value] == self.game.settings['pacman_texture']:
                current_index_4 = value
        for value in range(len(settings_5_f)):
            if settings_5_f[value] == self.game.settings['field_texture']:
                current_index_5 = value
        for value in range(len(settings_6_f)):
            if settings_6_f[value] == self.game.settings['long_buffer']:
                current_index_6 = value
        self.lvl_config.switch_to(current_index_1)
        self.mode_config.switch_to(current_index_2)
        self.coop_config.switch_to(current_index_3)
        self.pacman_config.switch_to(current_index_4)
        self.background_config.switch_to(current_index_5)
        self.long_buffer_config.switch_to(current_index_6)
        self.game.settings['level'] = int(self.lvl_config.get_current_value().split(': ')[1])
        self.game.settings['mode'] = self.mode_config.get_current_value().split(': ')[1]
        self.game.settings['coop'] = self.coop_config.get_current_value().split(': ')[1] == 'True'
        self.game.settings['pacman_texture'] = self.pacman_config.get_current_value().split(': ')[1]
        self.game.settings['field_texture'] = int(self.background_config.get_current_value().split(': ')[1])
        self.game.settings['long_buffer'] = self.long_buffer_config.get_current_value().split(': ')[1] == 'True'
        self.defaults = [current_index_1,
                         current_index_2,
                         current_index_3,
                         current_index_4,
                         current_index_5,
                         current_index_6, ]

    def on_deactivate(self) -> None:
        write_json_to_file(SETTINGS_PATH, self.game.settings)
