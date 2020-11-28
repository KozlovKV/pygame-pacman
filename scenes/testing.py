import pygame

from constants import Color
from objects import ButtonObject, ImageObject
from objects.base import DrawableObject
from objects.highscore import HighScoresTable
from scenes import BaseScene


class TestScene(BaseScene):
    def create_objects(self) -> None:
        self.scene_buttons = [
            ButtonObject(self.game, 10, 100, 400, 42, Color.SOFT_RED,
                         self.game.set_menu_scene, 'MENU_SCENE'),
            ButtonObject(self.game, 10, 200, 400, 42, Color.SOFT_RED,
                         self.game.set_settings_scene, 'SETTINGS_SCENE'),
            ButtonObject(self.game, 10, 300, 400, 42, Color.SOFT_RED,
                         self.game.set_highscores_scene, 'HIGH_SCORES_SCENE'),
            ButtonObject(self.game, 10, 400, 400, 42, Color.SOFT_RED,
                         self.game.set_main_scene, 'MAIN_SCENE'),
            ButtonObject(self.game, 10, 500, 400, 42, Color.SOFT_RED,
                         self.game.set_game_over_scene, 'GAME_OVER_SCENE'),
            # HighScoresTable(self.game),
            ButtonObject(self.game, 10, 600, 400, 42, Color.SOFT_RED,
                         self.game.exit_game, 'EXIT'),
            ButtonObject(self.game, 10, 700, 400, 42, Color.SOFT_RED,
                         self.move_rect, 'BTN'),
            ButtonObject(self.game, 10, 800, 400, 42, Color.SOFT_RED,
                         self.next_img, 'NEXT'),
        ]
        self.objects += self.scene_buttons
        self.draw_obj = DrawableObject(self.game, 500, 500, 50, 50)
        self.objects.append(self.draw_obj)
        self.img_obj = ImageObject(self.game, './resources/images/teleport/teleport_0.png',
                                   600, 500, 2, './resources/images/teleport/teleport_[F].png')
        self.objects.append(self.img_obj)

    def additional_logic(self) -> None:
        self.img_obj.next_frame()

    def move_rect(self):
        self.draw_obj.move(0, -10)

    def next_img(self):
        self.img_obj.next_frame()
