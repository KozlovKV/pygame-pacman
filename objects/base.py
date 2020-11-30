import pygame


class DrawableObject:
    def __init__(self, game, x=0, y=0, w=0, h=0, color=(255, 255, 255),
                 hided_sprite_w=0, hided_sprite_h=0):
        self.game = game
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.color = color
        self.alive = True

        self.hided_collision_rect = None
        if hided_sprite_w != 0 or hided_sprite_h != 0:
            self.hided_collision_rect = pygame.rect.Rect(0, 0,
                                                         hided_sprite_w,
                                                         hided_sprite_h)
            self.recalculate_hided_sprite()

    def recalculate_hided_sprite(self):
        x = self.rect.x + (self.rect.w - self.hided_collision_rect.w) // 2
        y = self.rect.y + (self.rect.h - self.hided_collision_rect.h) // 2
        self.hided_collision_rect.x = x
        self.hided_collision_rect.y = y

    def collision(self, other):
        this_rect = self.rect
        other_rect = other.rect
        return this_rect.colliderect(other_rect)

    def collision_with_small_sprite(self, other):
        this_rect = self.hided_collision_rect
        other_rect = other.hided_collision_rect
        return this_rect.colliderect(other_rect)

    def die(self):
        self.rect.x = -1000
        self.rect.y = -1000
        self.process_draw()
        self.alive = False

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if self.hided_collision_rect is not None:
            self.recalculate_hided_sprite()

    def move_center(self, x, y):
        self.rect.centerx += x
        self.rect.centery += y
        if self.hided_collision_rect is not None:
            self.recalculate_hided_sprite()

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        if self.hided_collision_rect is not None:
            self.recalculate_hided_sprite()

    def set_center(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
        if self.hided_collision_rect is not None:
            self.recalculate_hided_sprite()

    def process_event(self, event):
        pass

    def process_logic(self):
        pass

    def process_draw(self):
        if self.alive:
            pygame.draw.rect(self.game.screen, self.color, self.rect)
