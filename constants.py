import pygame


# https://www.pygame.org/docs/ref/color.html
# https://github.com/pygame/pygame/blob/master/src_py/colordict.py
from objects.animation import AnimationPreset


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
    PURPLE = pygame.color.Color(255, 0, 255)


pygame.font.init()
MAIN_FONT = pygame.font.SysFont('Consolas', 32, True)

CELL_SIZE = 30
PACMAN_SPEED = 1
GHOST_SPEED = 2


class Textures:
    MAIN_FOLDER = './resources/images/'
    WALL = MAIN_FOLDER + 'wall/default/0.png'
    SEED = MAIN_FOLDER + 'seed/0.png'
    TELEPORT = AnimationPreset(2, MAIN_FOLDER + 'teleport/[F].png')
