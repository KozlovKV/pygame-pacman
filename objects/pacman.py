from constants import PACMAN_SPEED, Textures
from objects.image import ImageObject
import pygame


class Pacman(ImageObject):
    FRAMES_KEEP_TURN = 10  # Сколько кадров хранить поворот

    def __init__(self, game, x: int, y: int, id: int = 1):
        texture_settings = Textures.PACMAN[game.settings['pacman_texture']]
        super().__init__(game, x=x, y=y, animation=texture_settings[0],
                         hided_sprite_w=10, hided_sprite_h=10)
        self.angle = 0
        self.vec_x = 0
        self.vec_y = 0
        self.speed = PACMAN_SPEED
        self.rotable = texture_settings[1]
        self.pacman_id = id

        self.frames_keeping = 0
        self.previous_turn_status = -1
        self.turn_buff = -1
        self.turn_status = -1
        '''
        -1 - нет поворота
        0 - поворот вправо
        1 - поворот вверх
        2 - поворот влево
        3 - поворот вниз
        '''
        # Показывает, можно ли повернуться в указанную сторону
        self.turn_ways = [0, 0, 0, 0]

    def update_turn_ways(self, ways=[0, 0, 0, 0]):
        self.turn_ways = ways

    def do_turn(self):
        if self.turn_status != -1:
            if self.turn_ways[self.turn_status] == 0 and self.turn_buff != -1 and self.turn_ways[self.turn_buff] == 1:
                self.angle = 90 * self.turn_buff
                if self.turn_buff % 2 == 0:
                    self.vec_x = 1 if self.turn_buff == 0 else -1
                    self.vec_y = 0
                if self.turn_buff % 2 != 0:
                    self.vec_y = 1 if self.turn_buff == 3 else -1
                    self.vec_x = 0
                self.turn_status = self.turn_buff
                self.turn_buff = -1
            elif self.turn_ways[self.turn_status] == 1:
                self.angle = 90 * self.turn_status
                if self.turn_status % 2 == 0:
                    self.vec_x = 1 if self.turn_status == 0 else -1
                    self.vec_y = 0
                if self.turn_status % 2 != 0:
                    self.vec_y = 1 if self.turn_status == 3 else -1
                    self.vec_x = 0
            elif self.turn_ways[self.turn_status] == 0:
                self.vec_y = 0
                self.vec_x = 0
                self.turn_status = -1
                self.turn_buff = -1

    def process_event(self, event):
        if self.pacman_id == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    if self.turn_status == 1 or self.turn_status == 3:
                        self.turn_buff = 0
                    elif self.turn_status == 2:
                        self.turn_status = 0
                        self.turn_buff = -1
                    else:
                        self.turn_status = 0
                        self.turn_buff = -1
                    # print('RIGHT', self.turn_status, self.turn_buff)
                elif event.key == pygame.K_w:
                    if self.turn_status == 0 or self.turn_status == 2:
                        self.turn_buff = 1
                    elif self.turn_status == 3:
                        self.turn_status = 1
                        self.turn_buff = -1
                    else:
                        self.turn_status = 1
                        self.turn_buff = -1
                    # print('   UP', self.turn_status, self.turn_buff)
                elif event.key == pygame.K_a:
                    if self.turn_status == 0:
                        self.turn_status = 2
                        self.turn_buff = -1
                    elif self.turn_status == 1 or self.turn_status == 3:
                        self.turn_buff = 2
                    else:
                        self.turn_status = 2
                        self.turn_buff = -1
                    # print(' LEFT', self.turn_status, self.turn_buff)
                elif event.key == pygame.K_s:
                    if self.turn_status == 0 or self.turn_status == 2:
                        self.turn_buff = 3
                    elif self.turn_status == 1:
                        self.turn_status = 3
                        self.turn_buff = -1
                    else:
                        self.turn_status = 3
                        self.turn_buff = -1
                    # print(' DOWN', self.turn_status, self.turn_buff)
                
        elif self.pacman_id == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.turn_status = 0
                elif event.key == pygame.K_UP:
                    self.turn_status = 1
                elif event.key == pygame.K_LEFT:
                    self.turn_status = 2
                elif event.key == pygame.K_DOWN:
                    self.turn_status = 3

    def process_logic(self):
        # if self.turn_status != -1:
        #     if self.turn_status == self.previous_turn_status:
        #         self.frames_keeping += 1
        #         if self.frames_keeping >= Pacman.FRAMES_KEEP_TURN:
        #             self.turn_status = -1
        #             self.frames_keeping = 0
        #     self.previous_turn_status = self.turn_status

        self.do_turn()

        x = self.vec_x * self.speed
        y = self.vec_y * self.speed
        self.move(x, y)

    def process_draw(self):
        self.next_frame()
        self.rotate_img(self.angle)
        super(Pacman, self).process_draw()
