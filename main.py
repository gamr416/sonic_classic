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
    MOTOBUG = Motobug((11, 7))
    MAP = Map([1, 2, 16, 17, 18, 19, 24, 25], [20], [67, 134, 111, 112, 135], 1)
    game = Game(MAP, SONIC, MOTOBUG)
    SCREEN.fill((0, 0, 255))
    pygame.display.set_caption('Conic klassik')
    Game.update_sonic(game)
    pygame.quit()
