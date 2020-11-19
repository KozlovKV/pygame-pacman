from constants import Color
from objects import ButtonObject
from scenes import BaseScene


class TestScene(BaseScene):
    def create_objects(self) -> None:
        scene_buttons = [
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
            ButtonObject(self.game, 10, 600, 400, 42, Color.SOFT_RED,
                         self.game.exit_game, 'EXIT')
        ]
        self.objects += scene_buttons

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
