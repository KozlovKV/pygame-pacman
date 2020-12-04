from constants import Color, Sounds
from objects.button import ButtonObject
from objects.text import TextObject
from objects.highscore import HighScoresTable
from objects.switcher import ArrowSwitcher
from scenes import BaseScene


class FinalSceneName(BaseScene):
    SWITCHER_WIDTH = 300
    SWITCHER_HEIGHT = 40

    def __init__(self, game):
        self.label = None
        self.name_label = None
        self.enter_name_label = None
        self.first_letter = None
        self.second_letter = None
        self.third_letter = None
        self.enter_button = None
        self.letters = list()
        super().__init__(game)

    def create_objects(self) -> None:
        alphabet0 = (chr(i) for i in range(65, 91))
        alphabet1 = (chr(i) for i in range(65, 91))
        alphabet2 = (chr(i) for i in range(65, 91))
        x = (self.game.SCREEN_WIDTH - self.SWITCHER_WIDTH) / 2

        self.label = (TextObject(self.game, text='GAME OVER',
                                 x=self.game.SCREEN_WIDTH / 2, y=50,
                                 font_size=50))
        self.name_label = (TextObject(self.game, text='AAA', font_size=40,
                                      x=self.game.SCREEN_WIDTH / 2 + 130,
                                      y=100))
        self.enter_name_label = (TextObject(self.game, text='ENTER NICKNAME: ',
                                            x=self.game.SCREEN_WIDTH / 2 - 40,
                                            y=100))
        self.first_letter = (ArrowSwitcher(self.game,
                                           x, 150,
                                           self.SWITCHER_WIDTH,
                                           self.SWITCHER_HEIGHT,
                                           Color.WHITE, Color.SOFT_RED,
                                           0, *alphabet0))
        self.second_letter = (ArrowSwitcher(self.game,
                                            x, 200,
                                            self.SWITCHER_WIDTH,
                                            self.SWITCHER_HEIGHT,
                                            Color.WHITE, Color.SOFT_RED,
                                            0, *alphabet1))
        self.third_letter = (ArrowSwitcher(self.game,
                                           x, 250,
                                           self.SWITCHER_WIDTH,
                                           self.SWITCHER_HEIGHT,
                                           Color.WHITE, Color.SOFT_RED,
                                           0, *alphabet2))
        self.enter_button = (ButtonObject(self.game,
                                          x, 350,
                                          self.SWITCHER_WIDTH,
                                          self.SWITCHER_HEIGHT, Color.GREEN,
                                          self.go_to_game_over_scene_2, 'ENTER',
                                          'play'))
        self.letters = [
            self.first_letter,
            self.second_letter,
            self.third_letter,
        ]
        self.objects.append(self.label)
        self.objects.append(self.enter_name_label)
        self.objects.append(self.name_label)
        self.objects += self.letters
        self.objects.append(self.enter_button)

    def process_logic(self) -> None:
        self.name = ''
        self.name += self.first_letter.get_current_value()
        self.name += self.second_letter.get_current_value()
        self.name += self.third_letter.get_current_value()
        self.name_label.update_text(self.name)

    def on_activate(self) -> None:
        Sounds.BEGINING.play()

    def on_deactivate(self) -> None:
        Sounds.BEGINING.stop()

    def go_to_game_over_scene_2(self):
        HighScoresTable(self.game).add_new_score(
            self.name + ' ' + str(self.game.score))
        self.game.set_scene(6)


class FinalSceneScores(BaseScene):
    BUTTON_WIDTH = 500
    BUTTON_HEIGHT = 40

    def __init__(self, game):
        self.highscore_table = None
        self.label = None
        self.result_label = None
        self.return_button = None
        self.exit_button = None
        super().__init__(game)

    def create_objects(self) -> None:
        x = (self.game.SCREEN_WIDTH - self.BUTTON_WIDTH) / 2
        self.highscore_table = HighScoresTable(self.game,
                                               x=self.game.SCREEN_WIDTH / 2,
                                               y=150)
        self.label = TextObject(self.game,
                                text='GAME OVER',
                                x=self.game.SCREEN_WIDTH / 2, y=50,
                                font_size=50)
        self.result_label = TextObject(self.game,
                                       text='',
                                       color=Color.GREEN,
                                       x=self.game.SCREEN_WIDTH / 2, y=100,
                                       font_size=45)
        self.return_button = ButtonObject(self.game,
                                          x, 600,
                                          self.BUTTON_WIDTH,
                                          self.BUTTON_HEIGHT, Color.BLUE,
                                          self.game.set_test_scene,
                                          'TO TEST MENU')
        self.exit_button = ButtonObject(self.game,
                                        x, 650,
                                        self.BUTTON_WIDTH,
                                        self.BUTTON_HEIGHT, Color.SOFT_RED,
                                        self.game.exit_game, 'EXIT', 'exit')
        self.objects.append(self.highscore_table)
        self.objects.append(self.label)
        self.objects.append(self.result_label)
        self.objects.append(self.return_button)
        self.objects.append(self.exit_button)

    def on_activate(self) -> None:
        if self.game.is_win:
            Sounds.WIN.play()
        else:
            Sounds.LOSE.play()
        self.result_label.update_text('WIN' if self.game.is_win else 'LOSE')
        self.result_label.color = Color.GREEN if self.game.is_win else Color.SOFT_RED
        self.highscore_table.read_scores()
