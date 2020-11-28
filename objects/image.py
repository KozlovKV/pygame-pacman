import pygame

from objects.base import DrawableObject


class ImageObject(DrawableObject):
    def __init__(self, game, filename: str, x: int = None, y: int = None,
                 frames_count=0, frame_name='',
                 hided_sprite_w=0, hided_sprite_h=0):
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

        self.hided_collision_rect = None
        if hided_sprite_w != 0 or hided_sprite_h != 0:
            x = self.rect.x + (self.rect.w - hided_sprite_w) // 2
            y = self.rect.y + (self.rect.h - hided_sprite_h) // 2
            self.hided_collision_rect = pygame.rect.Rect(x, y,
                                                         hided_sprite_w,
                                                         hided_sprite_h)

    def collision(self, other):
        this_rect = self.rect
        other_rect = other.rect
        if self.hided_collision_rect is not None:
            this_rect = self.hided_collision_rect
        if other.hided_collision_rect is not None:
            other_rect = other.hided_collision_rect
        return this_rect.colliderect(other_rect)

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
