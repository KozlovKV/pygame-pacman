from constants import Color
from objects.button import ButtonObject
from objects.text import TextObject
from objects.highscore import HighScoresTable
from objects.switcher import ArrowSwitcher
from scenes import BaseScene


class FinalSceneName(BaseScene):
    def create_objects(self) -> None:
        alphabet0 = (chr(i) for i in range(65, 91))
        alphabet1 = (chr(i) for i in range(65, 91))
        alphabet2 = (chr(i) for i in range(65, 91))
        self.first_letter = (ArrowSwitcher(self.game,
                                          80, 100, 150, 40,
                                          Color.WHITE, Color.SOFT_RED,
                                          0, *alphabet0))
        self.second_letter = (ArrowSwitcher(self.game,
                                          80, 150, 150, 40,
                                          Color.WHITE, Color.SOFT_RED,
                                          0, *alphabet1))
        self.third_letter = (ArrowSwitcher(self.game,
                                          80, 200, 150, 40,
                                          Color.WHITE, Color.SOFT_RED,
                                          0, *alphabet2))
        self.objects.append(ButtonObject(self.game, 60, 300, 200, 40, Color.GREEN,
                                         self.go_to_game_over_scene_2, 'ENTER'))
        self.objects.append(self.first_letter)
        self.objects.append(self.second_letter)
        self.objects.append(self.third_letter)
        self.objects.append(TextObject(self.game, text='AAA', x=310, y=50))
        self.objects.append(TextObject(self.game, text='ENTER NICKNAME: ', x=150, y=50))

    def process_logic(self) -> None:
        self.name = ''
        self.name += self.first_letter.get_current_value()
        self.name += self.second_letter.get_current_value()
        self.name += self.third_letter.get_current_value()
        self.objects[4].update_text(self.name)

    def go_to_game_over_scene_2(self):
        HighScoresTable(self.game).add_new_score(self.name + ' ' + str(self.game.score))
        self.game.set_scene(6)


class FinalSceneScores(BaseScene):
    def create_objects(self) -> None:
        self.highscore_table = HighScoresTable(self.game)
        self.objects.append(TextObject(self.game,
                                       text=('WIN' if self.game.is_win else 'LOSE'),
                                       color=(Color.GREEN if self.game.is_win else Color.SOFT_RED),
                                       x=400, y=50))
        self.objects.append(ButtonObject(self.game, 10, 600, 220, 40, Color.SOFT_RED,
                                         self.game.exit_game, 'EXIT'))
        self.objects.append(ButtonObject(self.game, 10, 550, 220, 40, Color.BLUE,
                                         self.game.set_test_scene, 'TO TEST MENU'))
        self.objects.append(self.highscore_table)

    def on_activate(self) -> None:
        self.highscore_table.read_scores()

    # TEXT_FMT = 'Game over ({})'
    # seconds_to_end = 3
    #
    # def __init__(self, game) -> None:
    #     self.last_seconds_passed = 0
    #     super().__init__(game)
    #     self.update_start_time()
    #
    # def on_activate(self) -> None:
    #     self.update_start_time()
    #
    # def update_start_time(self) -> None:
    #     self.time_start = datetime.now()
    #
    # def get_gameover_text_formatted(self) -> str:
    #     return self.TEXT_FMT.format(self.seconds_to_end - self.last_seconds_passed)
    #
    # def create_objects(self) -> None:
    #     self.text = TextObject(
    #         self.game,
    #         text=self.get_gameover_text_formatted(), color=Color.RED,
    #         x=self.game.WIDTH // 2, y=self.game.HEIGHT // 2
    #     )
    #     self.objects.append(self.text)
    #
    # def additional_logic(self) -> None:
    #     time_current = datetime.now()
    #     seconds_passed = (time_current - self.time_start).seconds
    #     if self.last_seconds_passed != seconds_passed:
    #         self.last_seconds_passed = seconds_passed
    #         self.objects[0].update_text(self.get_gameover_text_formatted())
    #     if seconds_passed >= self.seconds_to_end:
    #         self.game.set_scene(self.game.MENU_SCENE_INDEX)
