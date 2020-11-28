import pygame

from objects.base import DrawableObject


class ImageObject(DrawableObject):
    def __init__(self, game, filename: str, x: int = None, y: int = None,
                 frames_count=0, frame_name=''):
        super().__init__(game)
        if filename:
            self.filename = filename
        self.image = pygame.image.load(self.filename)
        self.rect = self.image.get_rect()

        self.frames_count = frames_count
        self.frame_name = frame_name
        self.current_frame = 0

        self.rect.x = x if x else 0
        self.rect.y = y if y else 0

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % self.frames_count
        current_frame_name = self.frame_name.replace('[F]',
                                                     str(self.current_frame))
        print(current_frame_name)
        print(self.frame_name)
        self.change_img(current_frame_name)

    def change_img(self, filename):
        self.filename = filename
        self.image = pygame.image.load(self.filename)
        a = self.rect.x
        b = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = a
        self.rect.y = b

    def rotate_img(self, deg):
        self.image = pygame.transform.rotate(self.image, deg)

    def process_draw(self) -> None:
        if self.alive:
            self.game.screen.blit(self.image, self.rect)
