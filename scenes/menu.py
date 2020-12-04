from constants import Color, Sounds, PACMAN_FONT
from objects.button import ButtonObject
from objects.text import TextObject
from scenes import BaseScene


class MenuScene(BaseScene):
    BTN_WIDTH = 400
    BTN_HEIGHT = 50

    def create_objects(self) -> None:
        y = 140
        self.header = TextObject(self.game, text='',
                                 x=self.game.SCREEN_WIDTH / 2, y=y)
        self.header.font = PACMAN_FONT
        self.header.update_text('PAC - MAN')
        self.objects.append(self.header)

        x = (self.game.SCREEN_WIDTH - self.BTN_WIDTH) / 2

        self.play_btn = ButtonObject(self.game, x, y+160,
                                     self.BTN_WIDTH, self.BTN_HEIGHT,
                                     Color.SOFT_RED,
                                     self.game.set_main_scene, 'PLAY', 'play')
        self.objects.append(self.play_btn)

        self.hs_btn = ButtonObject(self.game, x, y+240,
                                   self.BTN_WIDTH, self.BTN_HEIGHT,
                                   Color.SOFT_RED,
                                   self.game.set_highscores_scene,
                                   'HIGHSCORES', 'multi')
        self.objects.append(self.hs_btn)

        self.settings_btn = ButtonObject(self.game, x, y+320,
                                         self.BTN_WIDTH, self.BTN_HEIGHT,
                                         Color.SOFT_RED,
                                         self.game.set_settings_scene,
                                         'SETTINGS', 'multi')
        self.objects.append(self.settings_btn)

        self.exit_btn = ButtonObject(self.game, x, y+400,
                                     self.BTN_WIDTH, self.BTN_HEIGHT,
                                     Color.SOFT_RED,
                                     self.game.exit_game, 'EXIT', 'exit')
        self.objects.append(self.exit_btn)

    def on_activate(self) -> None:
        Sounds.BEGINING.play()

    def on_deactivate(self) -> None:
        Sounds.BEGINING.stop()
