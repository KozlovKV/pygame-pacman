from objects import ImageObject
import pygame

accelerate = 1
speed = 3
class Pacman(ImageObject):
    def __init__(self, game, filename: str, x: int, y: int):
        super().__init__(game, filename, x, y)
        self.vec_x = speed
        self.vec_y = speed
        self.texture_name = f'./resources/images/pacman\_1\_{0}.jpg'
        self.frames_count = frames_count
        self.frame = frame
        bool self.rotable = rotable
        self.pacman_id = pacman_id

    def pacman_process_draw(self):
        if self.frame+1 == frames_count:
            self.frame = 0
        else:
            self.frame += 1
        change_img(self, filename)
        process_draw(self)

    def process_event(self, event):
        if self.pacman_id == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.y -= (speed * accelerate)
                    self.vec_x = 0
                    self.vec_y = 1
                elif event.key == pygame.K_s:
                    self.y += (speed * accelerate)
                    self.vec_x = 0
                    self.vec_y = -1
                elif event.key == pygame.K_a:
                    self.x -= (speed * accelerate)
                    self.vec_x = -1
                    self.vec_y = 0
                elif event.key == pygame.K_d:
                    self.x += (speed * accelerate)
                    self.vec_x = 1
                    self.vec_y = 0
        elif self.pacman_id == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.y -= (speed * accelerate)
                    self.vec_x = 0
                    self.vec_y = 1
                elif event.key == pygame.K_DOWN:
                    self.y += (speed * accelerate)
                    self.vec_x = 0
                    self.vec_y = -1
                elif event.key == pygame.K_LEFT:
                    self.x -= (speed * accelerate)
                    self.vec_x = -1
                    self.vec_y = 0
                elif event.key == pygame.K_RIGHT:
                    self.x += (speed * accelerate)
                    self.vec_x = 1
                    self.vec_y = 0

    def process_logic(self):
        self.move(self.x, self.y)