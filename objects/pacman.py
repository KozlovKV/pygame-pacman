from objects import ImageObject
import pygame

speed = 3
class Pacman(ImageObject):
    def __init__(self, game, filename: str, x: int, y: int):
        super().__init__(game, filename, x, y)
        self.angle = 0
        self.vec_x = 0
        self.vec_y = 0
        self.texture_name = f'./resources/images/pacman\_1\_{0}.jpg'
        self.frames_count = frames_count
        self.frame = 0
        self.rotable = rotable
        self.pacman_id = pacman_id

    def pacman_process_draw(self):
        self.next_frame()
        self.rotate_img(self.angle)
        self.process_draw()

    def process_event(self, event):
        if self.pacman_id == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.vec_x = 0
                    self.vec_y = 1
                    self.angle = 270
                elif event.key == pygame.K_s:
                    self.vec_x = 0
                    self.vec_y = -1  
                    self.angle = 90         
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
                    self.vec_y = 1
                    self.angle = 270
                elif event.key == pygame.K_DOWN:
                    self.vec_x = 0
                    self.vec_y = -1
                    self.angle = 90
                elif event.key == pygame.K_LEFT:
                    self.vec_x = -1
                    self.vec_y = 0
                    self.angle = 180
                elif event.key == pygame.K_RIGHT:
                    self.vec_x = 1
                    self.vec_y = 0
                    self.angle = 0

    def process_logic(self):
        x = self.vec_x * speed
        y = self.vec_y * speed
        self.move(x, y)
