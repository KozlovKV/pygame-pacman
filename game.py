import pygame

from constants import Color
from scenes import MenuScene, SettingsScene, HighScoresScene, MainScene, \
    FinalScene


class Game:
    SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 1000
    FIELD_SIZE = FIELD_WIDTH, FIELD_HEIGHT = 750, 750
    TICK = 75
    MENU_SCENE_INDEX = 0
    SETTINGS_SCENE_INDEX = 1
    HIGHSCORES_SCENE_INDEX = 2
    MAIN_SCENE_INDEX = 3
    GAMEOVER_SCENE_INDEX = 4
    current_scene_index = MENU_SCENE_INDEX

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(Game.SCREEN_SIZE)
        self.scenes = [MenuScene(self),
                       SettingsScene(self),
                       HighScoresScene(self),
                       MainScene(self),
                       FinalScene(self)]
        self.scores = 0
        self.settings = {
            'ghost_speed': 1,
            'ghosts_count': 4,
            'level': 0,
            'mode': 0,
            'field_texture': 0,
            'coop': False
        }
        self.game_over = False

    @staticmethod
    def exit_button_pressed(event: pygame.event.Event) -> bool:
        return event.type == pygame.QUIT

    @staticmethod
    def exit_hotkey_pressed(event: pygame.event.Event) -> bool:
        return event.type == pygame.KEYDOWN and event.mod & pygame.KMOD_CTRL and event.key == pygame.K_q

    def process_exit_events(self, event: pygame.event.Event) -> None:
        if Game.exit_button_pressed(event) or Game.exit_hotkey_pressed(event):
            self.exit_game()

    def process_all_events(self) -> None:
        for event in pygame.event.get():
            self.process_exit_events(event)
            self.scenes[self.current_scene_index].process_event(event)

    def process_all_logic(self) -> None:
        self.scenes[self.current_scene_index].process_logic()

    def process_all_draw(self) -> None:
        self.screen.fill(Color.BLACK)
        self.scenes[self.current_scene_index].process_draw()
        pygame.display.flip()

    def main_loop(self) -> None:
        while not self.game_over:
            self.process_all_events()
            self.process_all_logic()
            self.process_all_draw()
            pygame.time.wait(Game.TICK)

    def set_scene(self, index: int, resume: bool = False) -> None:
        if not resume:
            self.scenes[self.current_scene_index].on_deactivate()
        self.current_scene_index = index
        if not resume:
            self.scenes[self.current_scene_index].on_activate()

    def exit_game(self) -> None:
        print('Bye bye')
        self.game_over = True

    def set_scores(self, value):
        self.scores = value

    def add_scores(self, delta):
        self.scores += delta
