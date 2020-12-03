import datetime

import pygame

from constants import Color, MAIN_FONT
from objects.button import ButtonObject
from objects.ghost import Ghost
from objects.text import TextObject
from objects.matrix_map import MatrixMap
from scenes import BaseScene


class MainScene(BaseScene):
    def __init__(self, game):

        game.score = 0

        self.game_mode = game.settings['mode']

        self.last_timer = datetime.datetime.now()
        self.played_seconds = 0

        self.lives = 3

        self.paused = False

        super().__init__(game)

    def create_objects(self) -> None:
        self.score_bar = None
        self.time_bar = None
        self.lives_bar = None
        self.pause_bar = None
        self.pause_button = None

        tmp_x = 20 + MAIN_FONT.size('SCORE: 0000')[0] // 2
        self.score_bar = TextObject(self.game, text='SCORE: 0', x=tmp_x, y=20)

        tmp_x = self.game.SCREEN_WIDTH - MAIN_FONT.size('TIME: 0000')[
            0] // 2 - 20
        self.time_bar = TextObject(self.game, text='TIME: 0', x=tmp_x, y=20)

        tmp_x = self.game.SCREEN_WIDTH // 2
        self.lives_bar = TextObject(self.game, text=f'LIVES: {self.lives}',
                                    x=tmp_x, y=20)
        self.pause_bar = TextObject(self.game, text='PAUSED',
                                    x=tmp_x, y=-60, color=Color.RED)

        self.pause_button = ButtonObject(self.game,
                                         self.game.SCREEN_WIDTH - 210, 60,
                                         200, 40, Color.SOFT_RED,
                                         self.switch_pause, 'PAUSE')
        self.menu_button = ButtonObject(self.game, 10, 60, 200, 40, Color.SOFT_RED,
                         self.game.set_test_scene, 'TO MENU', 'exit')

        self.objects.append(self.score_bar)
        self.objects.append(self.time_bar)
        self.objects.append(self.lives_bar)
        self.objects.append(self.pause_bar)
        self.objects.append(self.pause_button)
        self.objects.append(self.menu_button)

        self.matrix = MatrixMap(self.game)
        self.objects.append(self.matrix)

    def process_logic(self) -> None:
        if self.paused:
            self.last_timer = datetime.datetime.now()
        else:
            super(MainScene, self).process_logic()

    def additional_logic(self) -> None:
        now = datetime.datetime.now()
        delta = now - self.last_timer
        self.last_timer = now
        self.played_seconds += delta.total_seconds()
        self.time_bar.update_text(f'TIME: {int(self.played_seconds)}')

        if self.game_mode == 'survival':
            self.game.set_scores(int(self.played_seconds)*10)

        self.score_bar.update_text(f'SCORE: {self.game.score}')

        self.lives_bar.update_text(f'LIVES: {self.lives}')

        self.pacmans_reviving()

        if self.is_win():
            self.end_game(True)
        elif self.is_lose():
            self.end_game(False)

    @staticmethod
    def scary_mode_on():
        Ghost.scary_mode_on()

    def pacmans_reviving(self):
        pacmans = self.matrix.pacmans
        ghosts = self.matrix.ghosts
        for pacman in pacmans:
            obj = pacman.obj
            if not obj.alive and self.lives > 0:
                self.lives -= 1
                for p in pacmans:
                    p.obj.revive()
                for g in ghosts:
                    g.obj.set_spawn_pos()

    def is_win(self):
        if self.game_mode == 'score_cup':
            return self.matrix.seeds_count <= 0
        elif self.game_mode == 'hunt':
            return self.matrix.ghosts_count <= 0
        return False

    def is_lose(self):
        if self.matrix.pacmans_count <= 0 and self.lives <= 0:
            return True
        return False

    def end_game(self, win=False):
        self.game.is_win = win
        self.game.set_scene(self.game.GAMEOVER_SCENE_INDEX)

    def on_activate(self) -> None:
        self.__init__(self.game)
        self.game.screen.fill(Color.BLACK)

    def process_event(self, event: pygame.event.Event) -> None:
        if self.paused:
            self.menu_button.process_event(event)
            self.pause_button.process_event(event)
            self.additional_event_check(event)
        else:
            super(MainScene, self).process_event(event)

    def additional_event_check(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.switch_pause()

    def switch_pause(self):
        self.pause_bar.rect.y *= -1
        self.paused = not self.paused

    def process_draw(self) -> None:
        pygame.draw.rect(self.game.screen, Color.BLACK,
                         (0, 0, self.game.SCREEN_WIDTH, MatrixMap.FIELD_Y))
        super(MainScene, self).process_draw()
