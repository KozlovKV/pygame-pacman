from constants import Color, SETTINGS_PATH
from misc import write_json_to_file, read_json_from_file
from objects.button import ButtonObject
from objects.switcher import ArrowSwitcher
from objects.text import TextObject
from scenes import BaseScene


class SettingsScene(BaseScene):
    SWITCHER_WIDTH = 700
    SWITCHER_HEIGHT = 50

    def __init__(self, game):
        self.lvl_config = None
        self.mode_config = None
        self.coop_config = None
        self.pacman1_config = None
        self.pacman2_config = None
        self.background_config = None
        self.long_buffer_config = None
        self.configs = list()
        self.save_changes = True
        super().__init__(game)

    def create_objects(self) -> None:
        self.game.settings = read_json_from_file(SETTINGS_PATH)

        self.lvl_count = int(self.game.settings['lvl_count'])
        self.lvl_skin = int(self.game.settings['lvl_skin'])
        self.settings_1 = ["Level: " + (str(i) + "/" + str(self.lvl_count-1)) for i in range(self.lvl_count)]
        self.settings_2 = ['Mode: score_cup', 'Mode: survival', 'Mode: hunt']
        self.settings_3 = ['Coop: False', 'Coop: True']
        self.settings_4 = ['First Pacman skin: classic',
                           'First Pacman skin: bordered',
                           'First Pacman skin: inverted',
                           'First Pacman skin: ghost', ]
        self.settings_5 = ['Second Pacman skin: classic',
                           'Second Pacman skin: bordered',
                           'Second Pacman skin: inverted',
                           'Second Pacman skin: ghost', ]
        self.settings_6 = ['Level texture: ' + (str(i) + "/" + str(self.lvl_skin-1)) for i in range(self.lvl_skin)]
        self.settings_7 = ['Long turn buffer: True', 'Long turn buffer: False']

        x = (self.game.SCREEN_WIDTH - self.SWITCHER_WIDTH) / 2
        self.lvl_config = (ArrowSwitcher(self.game,
                                         x, 70,
                                         self.SWITCHER_WIDTH,
                                         self.SWITCHER_HEIGHT,
                                         Color.WHITE, Color.SOFT_RED,
                                         0, *self.settings_1))
        self.mode_config = (ArrowSwitcher(self.game,
                                          x, 130,
                                          self.SWITCHER_WIDTH,
                                          self.SWITCHER_HEIGHT,
                                          Color.WHITE, Color.ORANGE,
                                          0, *self.settings_2))
        self.coop_config = (ArrowSwitcher(self.game,
                                          x, 190,
                                          self.SWITCHER_WIDTH,
                                          self.SWITCHER_HEIGHT,
                                          Color.WHITE, Color.YELLOW,
                                          0, *self.settings_3))
        self.pacman1_config = (ArrowSwitcher(self.game,
                                             x, 250,
                                             self.SWITCHER_WIDTH,
                                             self.SWITCHER_HEIGHT,
                                             Color.WHITE, Color.GREEN,
                                             0, *self.settings_4))
        self.pacman2_config = (ArrowSwitcher(self.game,
                                             x, 310,
                                             self.SWITCHER_WIDTH,
                                             self.SWITCHER_HEIGHT,
                                             Color.WHITE, Color.SOFT_BLUE,
                                             0, *self.settings_5))
        self.background_config = (ArrowSwitcher(self.game,
                                                x, 370,
                                                self.SWITCHER_WIDTH,
                                                self.SWITCHER_HEIGHT,
                                                Color.WHITE, Color.BLUE,
                                                0, *self.settings_6))
        self.long_buffer_config = (ArrowSwitcher(self.game,
                                                 x, 430,
                                                 self.SWITCHER_WIDTH,
                                                 self.SWITCHER_HEIGHT,
                                                 Color.WHITE, Color.PURPLE,
                                                 0, *self.settings_7))
        self.configs = [
            self.lvl_config,
            self.mode_config,
            self.coop_config,
            self.pacman1_config,
            self.pacman2_config,
            self.background_config,
            self.long_buffer_config,
        ]
        self.objects += self.configs
        self.objects.append(
            ButtonObject(self.game, x, 490, self.SWITCHER_WIDTH, 40,
                         Color.SOFT_RED,
                         self.game.set_test_scene, 'SAVE AND RETURN', 'exit'))
        self.objects.append(
            ButtonObject(self.game, x, 550, self.SWITCHER_WIDTH, 40,
                         Color.SOFT_RED,
                         self.quit_without_saving, 'RETURN', 'exit'))
        self.objects.append(TextObject(self.game, text='SETTINGS',
                                       font_size=50,
                                       x=self.game.SCREEN_WIDTH / 2, y=30))

    def quit_without_saving(self):
        self.save_changes = False
        self.game.set_test_scene()

    def process_logic(self) -> None:
        pass

    def on_activate(self) -> None:
        self.game.settings = read_json_from_file(SETTINGS_PATH)

        settings_f_list = [
            [item.split(': ')[1].split('/')[0] for item in self.settings_1],
            [item.split(': ')[1] for item in self.settings_2],
            [item.split(': ')[1] for item in self.settings_3],
            [item.split(': ')[1] for item in self.settings_4],
            [item.split(': ')[1] for item in self.settings_5],
            [item.split(': ')[1].split('/')[0] for item in self.settings_6],
            [item.split(': ')[1] for item in self.settings_7],
        ]
        settings_names = ['level', 'mode', 'coop',
                          '1_pacman_texture', '2_pacman_texture',
                          'field_texture', 'long_buffer']
        for conf_i in range(len(settings_f_list)):
            values = settings_f_list[conf_i]
            value_in_game_settings = self.game.settings[settings_names[conf_i]]
            for value_i in range(len(values)):
                if values[value_i] == str(value_in_game_settings):
                    self.configs[conf_i].switch_to(value_i)

        self.save_settings_to_game_dict()

    def on_deactivate(self) -> None:
        if self.save_changes:
            self.save_settings_to_game_dict()
            write_json_to_file(SETTINGS_PATH, self.game.settings)

    def save_settings_to_game_dict(self):
        self.game.settings['level'] = int(
            self.lvl_config.get_current_value().split(': ')[1].split('/')[0])
        self.game.settings['mode'] = \
            self.mode_config.get_current_value().split(': ')[1]
        self.game.settings['coop'] = \
            self.coop_config.get_current_value().split(': ')[1] == 'True'
        self.game.settings['1_pacman_texture'] = \
            self.pacman1_config.get_current_value().split(': ')[1]
        self.game.settings['2_pacman_texture'] = \
            self.pacman2_config.get_current_value().split(': ')[1]
        self.game.settings['field_texture'] = int(
            self.background_config.get_current_value().split(': ')[1].split('/')[0])
        self.game.settings['long_buffer'] = \
            self.long_buffer_config.get_current_value().split(': ')[1] == 'True'
