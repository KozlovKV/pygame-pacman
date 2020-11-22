import pygame


class DrawableObject:
    def __init__(self, game, x = 0, y = 0, w = 0, h = 0, color):
        self.game = game
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.color = color
        self.alive = True

    def collision(self, other):
        return self.rect.colliderect(other.rect)

    def die(self):
        self.alive = False
        self.rect.x = -1000
        self.rect.y = -1000

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def move_center(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def process_event(self, event):
        pass

    def process_logic(self):
        pass

    def process_draw(self):
        if self.alive == True:
            pygame.draw.rect(self.game.screen, self.rect, self.color)
