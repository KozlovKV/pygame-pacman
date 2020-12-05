import datetime

import pygame

from constants import Color, MAIN_FONT, Sounds
from objects.base import DrawableObject
from objects.button import ButtonObject
from objects.ghost import Ghost
from objects.text import TextObject
from objects.matrix_map import MatrixMap
from scenes import BaseScene


class MainScene(BaseScene):
    TICKS_TO_REVIVE = 40
    TICKS_TO_DEATH_SOUND = 30
    BORDER_SIZE = 2
    BARS_Y = 50

    def __init__(self, game):

        game.score = 0

        self.game_mode = game.settings['mode']

        self.last_timer = datetime.datetime.now()
        self.played_seconds = 0

        self.lives = 3

        self.death_music_timer = 0

        self.revivings_pause_ticks = self.TICKS_TO_REVIVE

        self.paused = False

        super().__init__(game)

    def create_objects(self) -> None:

        self.matrix = MatrixMap(self.game)
        self.objects.append(self.matrix)

        self.info_border = DrawableObject(self.game, 0, 0,
                                          self.game.SCREEN_WIDTH,
                                          self.matrix.FIELD_Y,
                                          self.game.settings[
                                              "level_border_color"])
        self.info_bg = DrawableObject(self.game, self.BORDER_SIZE,
                                      self.BORDER_SIZE,
                                      self.game.SCREEN_WIDTH - self.BORDER_SIZE * 2,
                                      self.matrix.FIELD_Y - self.BORDER_SIZE * 2,
                                      Color.BLACK)
        tmp_x = self.BORDER_SIZE*5 + MAIN_FONT.size('SCORE: 0000')[0] // 2
        self.score_bar = TextObject(self.game, text='SCORE: 0', x=tmp_x, y=20)

        tmp_x = self.game.SCREEN_WIDTH - MAIN_FONT.size('TIME: 0000')[
            0] // 2 - self.BORDER_SIZE*5
        self.time_bar = TextObject(self.game, text='TIME: 0', x=tmp_x, y=20)

        tmp_x = self.game.SCREEN_WIDTH // 2
        self.lives_bar = TextObject(self.game, text=f'SCORE: {self.game.score}',
                                    x=tmp_x, y=20)
        self.pause_bar = TextObject(self.game, text='PAUSED',
                                    x=tmp_x, y=-self.BARS_Y, color=Color.RED)
        self.ready_bar = TextObject(self.game, text='',
                                    x=tmp_x, y=-self.BARS_Y, color=Color.YELLOW)
        self.go_bar = TextObject(self.game, text='GO!',
                                 x=tmp_x, y=self.BARS_Y, color=Color.GREEN)

        self.pause_button = ButtonObject(self.game,
                                         self.game.SCREEN_WIDTH - 210, self.BARS_Y,
                                         200, 40, self.switch_pause,
                                         'PAUSE', 'multi')
        self.menu_button = ButtonObject(self.game, 10, self.BARS_Y, 200, 40,
                                        self.game.set_menu_scene, 'TO MENU',
                                        'exit')

        self.objects.append(self.info_border)
        self.objects.append(self.info_bg)
        self.objects.append(self.score_bar)
        self.objects.append(self.time_bar)
        self.objects.append(self.lives_bar)
        self.objects.append(self.pause_bar)
        self.objects.append(self.ready_bar)
        self.objects.append(self.go_bar)
        self.objects.append(self.pause_button)
        self.objects.append(self.menu_button)

    def process_logic(self) -> None:
        if self.paused:
            self.last_timer = datetime.datetime.now()
        elif self.death_music_timer > 0:
            self.death_music_timer -= 1
        elif self.revivings_pause_ticks > 0:
            self.revivings_pause_ticks -= 1
            self.ready_bar.rect.y = self.BARS_Y
            self.ready_bar.update_text(f'READY! {self.revivings_pause_ticks}')
            self.go_bar.rect.y = -self.BARS_Y
        elif self.revivings_pause_ticks == 0:
            self.revivings_pause_ticks = -1
            self.ready_bar.rect.y = -self.BARS_Y
            self.go_bar.rect.y = self.BARS_Y
        else:
            self.pacmans_reviving()
            super(MainScene, self).process_logic()

    def additional_logic(self) -> None:
        now = datetime.datetime.now()
        delta = now - self.last_timer
        self.last_timer = now
        self.played_seconds += delta.total_seconds()
        self.time_bar.update_text(f'TIME: {int(self.played_seconds)}')

        if self.game_mode == 'survival':
            self.game.set_scores(int(self.played_seconds) * 10)

        self.score_bar.update_text(f'SCORE: {self.game.score}')

        self.lives_bar.update_text(f'LIVES: {self.lives}')

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
                self.revivings_pause_ticks = self.TICKS_TO_REVIVE
                self.lives -= 1
                for p in pacmans:
                    p.obj.revive()
                for g in ghosts:
                    g.obj.set_spawn_pos()
                self.music_reload()

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
        self.music_reload()

    def music_reload(self, ):
        Sounds.SIREN.stop()
        Sounds.BEGINING.play()
        Sounds.SIREN.play(-1, fade_ms=50000)

    def on_deactivate(self) -> None:
        Sounds.SIREN.stop()

    def process_event(self, event: pygame.event.Event) -> None:
        if self.revivings_pause_ticks == -1 and self.death_music_timer == 0:
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
        self.go_bar.rect.y *= -1
        self.pause_bar.rect.y = self.BARS_Y if self.pause_bar.rect.y < 0 else -self.BARS_Y
        self.paused = not self.paused

    def process_draw(self) -> None:
        super(MainScene, self).process_draw()
