import pygame

from objects.base import DrawableObject


class ImageObject(DrawableObject):
    def __init__(self, game, filename: str, x: int = None, y: int = None):
        super().__init__(game)
        if filename:
            self.filename = filename
        self.image = pygame.image.load(self.filename)
        self.rect = self.image.get_rect()
        self.rect.x = x if x else 0
        self.rect.y = y if y else 0

    def change_img(self, filename):
        self.filename = filename
        self.image = pygame.image.load(self.filename)
        a = self.rect.x
        b = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = a
        self.rect.y = b

    def process_draw(self) -> None:
        if self.alive:
            self.game.screen.blit(self.image, self.rect)
