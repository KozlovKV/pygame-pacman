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
PACMAN_FONT = pygame.font.Font('./resources/fonts/pacman.ttf', 100)

CELL_SIZE = 30
PACMAN_SPEED = 5
GHOST_SPEED = 3
DEAD_GHOST_SPEED = GHOST_SPEED * 2

SETTINGS_PATH = './data/settings.json'


class Textures:
    MAIN_FOLDER = './resources/images/'
    WALL = MAIN_FOLDER + 'wall/default.png'
    WALL_GHOST_IN = MAIN_FOLDER + 'wall/ghost_in.png'
    CELL_BG = [
        MAIN_FOLDER + 'cell_bg/0.png',
        MAIN_FOLDER + 'cell_bg/1.png',
        MAIN_FOLDER + 'cell_bg/2.png',
        MAIN_FOLDER + 'cell_bg/3.png',
        MAIN_FOLDER + 'cell_bg/4.png',
    ]
    SEED = MAIN_FOLDER + 'seed/0.png'
    SUPER_SEED = MAIN_FOLDER + 'super_seed/default/0.png'
    TELEPORT = [
        AnimationPreset(4, MAIN_FOLDER + 'teleport/blue/[F].png'),
        AnimationPreset(4, MAIN_FOLDER + 'teleport/green/[F].png'),
        AnimationPreset(4, MAIN_FOLDER + 'teleport/red/[F].png'),
        AnimationPreset(4, MAIN_FOLDER + 'teleport/yellow/[F].png'),
    ]
    PACMAN = {
        'classic': (AnimationPreset(6, MAIN_FOLDER + 'pacman/classic/[F].png'), True),
        'bordered': (AnimationPreset(6, MAIN_FOLDER + 'pacman/bordered/[F].png'), True),
        'inverted': (AnimationPreset(6, MAIN_FOLDER + 'pacman/inverted/[F].png'), True),
        'ghost': (AnimationPreset(6, MAIN_FOLDER + 'pacman/ghost_like/[F].png'), False),
    }
    SIMPLE_GHOST = {
        'body': AnimationPreset(4, MAIN_FOLDER + 'ghost/default/body/[F].png'),
        'eye': MAIN_FOLDER + 'ghost/default/eye.png',
        'simple_core': AnimationPreset(4, MAIN_FOLDER + 'ghost/default/simple_core/[F].png'),
        'scared_core': AnimationPreset(4, MAIN_FOLDER + 'ghost/default/scared_core/[F].png'),
    }
    GHOST_COLORS = {
        'black': AnimationPreset(3, MAIN_FOLDER + 'ghost/colors/black/[F].png'),
        'blue': AnimationPreset(3, MAIN_FOLDER + 'ghost/colors/blue/[F].png'),
        'green': AnimationPreset(3, MAIN_FOLDER + 'ghost/colors/green/[F].png'),
        'purple': AnimationPreset(3, MAIN_FOLDER + 'ghost/colors/purple/[F].png'),
        'red': AnimationPreset(3, MAIN_FOLDER + 'ghost/colors/red/[F].png'),
        'yellow': AnimationPreset(3, MAIN_FOLDER + 'ghost/colors/yellow/[F].png'),
    }


pygame.mixer.init()

class Sounds:
    MAIN_FOLDER = './resources/sounds/'
    BEGINING = pygame.mixer.Sound(MAIN_FOLDER + 'begining.wav')
    SEED = [
        pygame.mixer.Sound(MAIN_FOLDER + 'seed_1.wav'),
        pygame.mixer.Sound(MAIN_FOLDER + 'seed_2.wav'),
    ]
    SUPER_SEED = pygame.mixer.Sound(MAIN_FOLDER + 'super_seed.wav')
    PACMAN_DEATH = pygame.mixer.Sound(MAIN_FOLDER + 'pacman_death.wav')
    GHOST_DEATH = pygame.mixer.Sound(MAIN_FOLDER + 'ghost_death.wav')
    WIN = pygame.mixer.Sound(MAIN_FOLDER + 'win.wav')
    LOSE = pygame.mixer.Sound(MAIN_FOLDER + 'lose.wav')
    SIREN = pygame.mixer.Sound(MAIN_FOLDER + 'siren.wav')
