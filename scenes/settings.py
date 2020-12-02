from constants import Color, SETTINGS_PATH
from misc import write_json_to_file, read_json_from_file
from objects.button import ButtonObject
from objects.switcher import ArrowSwitcher
from scenes import BaseScene


class SettingsScene(BaseScene):
    def __init__(self, game):
        self.lvl_config = None
        self.mode_config = None
        self.coop_config = None
        self.pacman_config = None
        self.background_config = None
        self.configs = list()
        self.save_changes = True
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
        self.configs = [
            self.lvl_config,
            self.mode_config,
            self.coop_config,
            self.pacman_config,
            self.background_config,
            self.long_buffer_config,
        ]
        self.objects += self.configs
        self.objects.append(
            ButtonObject(self.game, 100, 370, 600, 40, Color.SOFT_RED,
                         self.game.set_test_scene, 'SAVE AND RETURN'))
        self.objects.append(
            ButtonObject(self.game, 100, 430, 600, 40, Color.SOFT_RED,
                         self.quit_without_saving, 'RETURN'))

    def quit_without_saving(self):
        self.save_changes = False
        self.game.set_test_scene()

    def process_logic(self) -> None:
        pass

    def on_activate(self) -> None:
        self.game.settings = read_json_from_file(SETTINGS_PATH)

        settings_f_list = [
            [item.split(': ')[1] for item in self.settings_1],
            [item.split(': ')[1] for item in self.settings_2],
            [item.split(': ')[1] for item in self.settings_3],
            [item.split(': ')[1] for item in self.settings_4],
            [item.split(': ')[1] for item in self.settings_5],
            [item.split(': ')[1] for item in self.settings_6],
        ]
        settings_names = ['level', 'mode', 'coop',
                          'pacman_texture', 'field_texture', 'long_buffer']
        for conf_i in range(len(settings_f_list)):
            values = settings_f_list[conf_i]
            value_in_game_settings = self.game.settings[settings_names[conf_i]]
            for value_i in range(len(values)):
                if values[value_i] == value_in_game_settings:
                    self.configs[conf_i].switch_to(value_i)

        self.save_settings_to_game_dict()

    def on_deactivate(self) -> None:
        if self.save_changes:
            self.save_settings_to_game_dict()
            write_json_to_file(SETTINGS_PATH, self.game.settings)

    def save_settings_to_game_dict(self):
        self.game.settings['level'] = int(
            self.lvl_config.get_current_value().split(': ')[1])
        self.game.settings['mode'] = \
        self.mode_config.get_current_value().split(': ')[1]
        self.game.settings['coop'] = \
        self.coop_config.get_current_value().split(': ')[1] == 'True'
        self.game.settings['pacman_texture'] = \
        self.pacman_config.get_current_value().split(': ')[1]
        self.game.settings['field_texture'] = int(
            self.background_config.get_current_value().split(': ')[1])
        self.game.settings['long_buffer'] = \
        self.long_buffer_config.get_current_value().split(': ')[1] == 'True'
