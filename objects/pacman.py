from constants import PACMAN_SPEED, Textures
from objects.image import ImageObject
import pygame


class Pacman(ImageObject):
    def __init__(self, game, x: int, y: int, id: int = 1):
        texture_settings = Textures.PACMAN[game.settings['pacman_texture']]
        super().__init__(game, x=x, y=y, animation=texture_settings[0])
        self.angle = 0
        self.vec_x = 0
        self.vec_y = 0
        self.speed = PACMAN_SPEED
        self.rotable = texture_settings[1]
        self.pacman_id = id

    def process_draw(self):
        self.next_frame()
        self.rotate_img(self.angle)
        super(Pacman, self).process_draw()

    def process_event(self, event):
        if self.pacman_id == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.vec_x = 0
                    self.vec_y = -1
                    self.angle = 90
                elif event.key == pygame.K_s:
                    self.vec_x = 0
                    self.vec_y = 1
                    self.angle = 270
                elif event.key == pygame.K_a:
                    self.vec_x = -1
                    self.vec_y = 0
                    self.angle = 180         
                elif event.key == pygame.K_d:
                    self.vec_x = 1
                    self.vec_y = 0
                    self.angle = 0
                
        elif self.pacman_id == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.vec_x = 0
                    self.vec_y = -1
                    self.angle = 90
                elif event.key == pygame.K_DOWN:
                    self.vec_x = 0
                    self.vec_y = 1
                    self.angle = 270
                elif event.key == pygame.K_LEFT:
                    self.vec_x = -1
                    self.vec_y = 0
                    self.angle = 180
                elif event.key == pygame.K_RIGHT:
                    self.vec_x = 1
                    self.vec_y = 0
                    self.angle = 0

    def process_logic(self):
        x = self.vec_x * self.speed
        y = self.vec_y * self.speed
        self.move(x, y)
