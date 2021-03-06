from constants import Textures, Sounds, PACMAN_SPEED
from objects.image import ImageObject
import pygame


class Pacman(ImageObject):
    FRAMES_KEEP_TURN = 10  # Сколько кадров хранить поворот

    def __init__(self, game, x: int, y: int, matrix_grid,
                 id: int = 1):
        texture_settings = Textures.PACMAN[game.settings[str(id) + '_pacman_texture']]
        super().__init__(game, x=x, y=y, animation=texture_settings[0],
                         hided_sprite_w=10, hided_sprite_h=10)
        self.spawn = (x, y)
        self.rotable_points = matrix_grid
        # fieldx = x - (m_x * cell_size)
        # fieldy = y - (m_y * cell_size)
        # for my in range(m_h):
        #     for mx in range(m_w):
        #         self.rotable_points.append([my * cell_size + fieldy,
        #                                    mx * cell_size + fieldx])
        #       # print('POINTS', my * cell_size + fieldy, mx * cell_size + fieldx)  # /////////////////////////
        self.angle = 0
        self.vec_x = 0
        self.vec_y = 0
        self.speed = PACMAN_SPEED
        self.rotable = texture_settings[1]
        self.pacman_id = id

        self.ticks_to_revive = -1

        self.frames_keeping = 0
        self.previous_turn_status = -1
        self.turn_buff = -1
        self.previous_turn_buff = -1
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

    def check_turn_status(self):
        if self.turn_buff != -1:
            # print("PACPOS", self.rect.y, self.rect.x)  # /////////////////////////////
            if self.turn_ways[self.turn_buff] == 1 and [self.rect.y, self.rect.x] in self.rotable_points:
                self.turn_status = self.turn_buff
                self.turn_buff = -1

    def do_turn(self):
        if self.turn_status != -1:
            if self.turn_ways[self.turn_status] == 1 and self.turn_status != self.previous_turn_status:
                self.angle = 90 * self.turn_status
                if self.turn_status % 2 == 0:
                    self.vec_x = 1 if self.turn_status == 0 else -1
                    self.vec_y = 0
                if self.turn_status % 2 != 0:
                    self.vec_y = 1 if self.turn_status == 3 else -1
                    self.vec_x = 0
                self.previous_turn_status = self.turn_status
            elif self.turn_ways[self.turn_status] == 0:
                self.vec_y = 0
                self.vec_x = 0
                self.turn_status = -1
                self.turn_buff = -1

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            keys = [pygame.K_d, pygame.K_w, pygame.K_a, pygame.K_s]
            if self.pacman_id == 2:
                keys = [pygame.K_RIGHT, pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN]
            for i in range(len(keys)):
                if event.key == keys[i]:
                    self.turn_buff = i

    def process_logic(self):
        if not self.game.settings['long_buffer']:
            if self.turn_buff != -1:
                if self.turn_buff == self.previous_turn_buff:
                    self.frames_keeping += 1
                    if self.frames_keeping >= Pacman.FRAMES_KEEP_TURN:
                        self.turn_buff = -1
                        self.frames_keeping = 0
                self.previous_turn_buff = self.turn_buff

        self.check_turn_status()
        self.do_turn()

        x = self.vec_x * self.speed
        y = self.vec_y * self.speed
        self.move(x, y)

    def die(self):
        self.alive = False
        Sounds.PACMAN_DEATH.play()
        scene = self.game.scenes[self.game.current_scene_index]
        scene.death_music_timer = scene.TICKS_TO_DEATH_SOUND

    def revive(self):
        self.set_position(*self.spawn)
        self.vec_y = 0
        self.vec_x = 0
        self.turn_status = -1
        self.previous_turn_status = -1
        anim = Textures.PACMAN[self.game.settings[str(self.pacman_id) + '_pacman_texture']][0]
        self.load_new_animation(anim)
        self.alive = True

    def process_draw(self):
        if self.rotable:
            self.rotate_img(self.angle)
        super(Pacman, self).process_draw()

    def set_grid(self, matrix_grid):
        self.rotable_points = matrix_grid
