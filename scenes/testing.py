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
                         self.menu_scene, 'MENU_SCENE'),
            ButtonObject(self.game, 10, 200, 400, 42, Color.SOFT_RED,
                         self.settings_scene, 'SETTINGS_SCENE'),
            ButtonObject(self.game, 10, 300, 400, 42, Color.SOFT_RED,
                         self.hs_scene, 'HIGH_SCORES_SCENE'),
            ButtonObject(self.game, 10, 400, 400, 42, Color.SOFT_RED,
                         self.main_scene, 'MAIN_SCENE'),
            ButtonObject(self.game, 10, 500, 400, 42, Color.SOFT_RED,
                         self.go_scene, 'GAME_OVER_SCENE'),
            # HighScoresTable(self.game),
            ButtonObject(self.game, 10, 600, 400, 42, Color.SOFT_RED,
                         self.game.exit_game, 'EXIT'),
            ButtonObject(self.game, 10, 700, 400, 42, Color.SOFT_RED,
                         self.move_rect, 'BTN'),
            ButtonObject(self.game, 10, 800, 400, 42, Color.SOFT_RED,
                         self.rotate_img, 'ROT'),
        ]
        self.objects += self.scene_buttons
        self.draw_obj = DrawableObject(self.game, 500, 500, 50, 50)
        self.objects.append(self.draw_obj)
        self.img_obj = ImageObject(self.game, './resources/images/test.jpg', 600, 500)
        self.objects.append(self.img_obj)

    def move_rect(self):
        self.draw_obj.move(0, -10)

    def rotate_img(self):
        self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 90)

    def menu_scene(self):
        print('MENU_TEMPLATE_LAUNCHED')
        self.game.set_scene(0)

    def settings_scene(self):
        print('SETTINGS_TEMPLATE_LAUNCHED')
        self.game.set_scene(1)

    def hs_scene(self):
        print('HIGH_SCORES_TEMPLATE_LAUNCHED')
        self.game.set_scene(2)

    def main_scene(self):
        print('MAIN_TEMPLATE_LAUNCHED')
        self.game.set_scene(3)

    def go_scene(self):
        print('GAME_OVER_TEMPLATE_LAUNCHED')
        self.game.set_scene(4)
