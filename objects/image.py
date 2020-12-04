from copy import copy

import pygame

from constants import CELL_SIZE
from objects.animation import AnimationPreset
from objects.base import DrawableObject


class ImageObject(DrawableObject):
    def __init__(self, game, filename: str = None, x: int = None, y: int = None,
                 animation: AnimationPreset = None,
                 hided_sprite_w=0, hided_sprite_h=0):
        super().__init__(game, x=x, y=y, w=CELL_SIZE, h=CELL_SIZE,
                         hided_sprite_w=hided_sprite_w,
                         hided_sprite_h=hided_sprite_h)
        self.filename = None
        self.animation = None
        self.image = None
        if filename:
            self.load_new_image(filename)
        elif animation:
            self.load_new_animation(animation)

    def next_frame(self):
        self.image = self.animation.get_next_frame()
        self.recalculate_img_rect()

    def load_new_image(self, filename):
        self.filename = filename
        self.image = pygame.image.load(self.filename)
        self.recalculate_img_rect()

    def load_new_animation(self, anim):
        self.animation = copy(anim)
        self.image = anim.frames_list[0]
        self.recalculate_img_rect()

    def recalculate_img_rect(self):
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
            if self.animation is not None:
                self.next_frame()
