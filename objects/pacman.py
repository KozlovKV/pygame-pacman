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
        if self.frame+1 == self.frames_count:
            self.frame = 0
        else:
            self.frame += 1
        change_img(self, filename)
        process_draw(self)

    def rotate_pacman_up(self):
        if self.angle == 0:
           self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 270)
        elif self.angle == 90:
            self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 180)
        elif self.angle == 180:
            self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 90)
        self.angle = 270

    def rotate_pacman_down(self):
        if self.angle == 0:
            self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 90)
        elif self.angle == 180:
           self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 270)
        elif self.angle == 270:
          self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 180)
        self.angle = 90

    def rotate_pacman_left(self):
        if self.angle == 0:
            self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 180)
        elif self.angle == 90:
           self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 90)
        elif self.angle == 270:
          self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 270)
        self.angle = 180

    def rotate_pacman_right(self):
        if self.angle == 90:
            self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 270)
        elif self.angle == 180:
           self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 180)
        elif self.angle == 270:
          self.img_obj.image = pygame.transform.rotate(self.img_obj.image, 90)
        self.angle = 0

    def process_event(self, event):
        if self.pacman_id == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.vec_x = 0
                    self.vec_y = 1
                    if self.rotable == True:
                        rotate_pacman_up(self)
                elif event.key == pygame.K_s:
                    self.vec_x = 0
                    self.vec_y = -1  
                    if self.rotable == True:  
                        rotate_pacman_down(self)         
                elif event.key == pygame.K_a:
                    self.vec_x = -1
                    self.vec_y = 0
                    if self.rotable == True: 
                        rotate_pacman_left(self)          
                elif event.key == pygame.K_d:
                    self.vec_x = 1
                    self.vec_y = 0
                    if self.rotable == True:
                        rotate_pacman_right(self)
                
        elif self.pacman_id == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.vec_x = 0
                    self.vec_y = 1
                    if self.rotable == True:
                        rotate_pacman_up(self)
                elif event.key == pygame.K_DOWN:
                    self.vec_x = 0
                    self.vec_y = -1
                    if self.rotable == True:  
                        rotate_pacman_down(self) 
                elif event.key == pygame.K_LEFT:
                    self.vec_x = -1
                    self.vec_y = 0
                    if self.rotable == True: 
                        rotate_pacman_left(self) 
                elif event.key == pygame.K_RIGHT:
                    self.vec_x = 1
                    self.vec_y = 0
                    if self.rotable == True:
                        rotate_pacman_right(self)

    def process_logic(self):
        x = vec_x * speed
        y = vec_y * speed
        self.move(x, y)
