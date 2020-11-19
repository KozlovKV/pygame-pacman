import pygame


# https://www.pygame.org/docs/ref/color.html
# https://github.com/pygame/pygame/blob/master/src_py/colordict.py

class Color:
    RED = pygame.color.Color('red')
    BLUE = pygame.color.Color('blue')
    GREEN = pygame.color.Color('green')
    BLACK = pygame.color.Color('black')
    WHITE = pygame.color.Color('white')
    ORANGE = pygame.color.Color('orange')
    YELLOW = pygame.color.Color('yellow')
    GREY = pygame.color.Color(64, 64, 64)
    SOFT_RED = pygame.color.Color(255, 78, 51)
    SOFT_BLUE = pygame.color.Color(65, 105, 225)
    SOFT_GREEN = pygame.color.Color(32, 232, 14)
    SOFT_ORANGE = pygame.color.Color(255, 180, 51)
    SOFT_YELLOW = pygame.color.Color(255, 255, 82)


pygame.font.init()
MAIN_FONT = pygame.font.SysFont('Consolas', 32, True)
