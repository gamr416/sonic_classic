import pygame
import sys
import os
from game import Game
from sonic import Sonic
from map import Map
from camera import Camera
from motobug import Motobug

MAPS_DIR = 'maps'
pygame.init()
SIZE = WIDTH, HEIGHT = 1200, 600
SCREEN = pygame.display.set_mode(SIZE)
TILE_SIZE = 40
FPS = 30
left = False
right = False


def load_image(name, colorkey=None):
    # если файл не существует, то выходим
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image


if __name__ == '__main__':
    camera = Camera()
    SONIC = Sonic((10, 7))
    MOTOBUG1 = Motobug((82, 2), 72, -5)
    MOTOBUG2 = Motobug((82, 20), 72, 13)
    MOTOBUG3 = Motobug((155, 20), 145, 13)
    MAP = Map([1, 2, 16, 17, 18, 19, 24, 25], [20], [67, 134, 111, 112, 135], 1)
    game = Game(MAP, SONIC, [MOTOBUG1, MOTOBUG2, MOTOBUG3])
    SCREEN.fill((0, 0, 255))
    pygame.display.set_caption('Conic klassik')
    Game.update_sonic(game)
    pygame.quit()
