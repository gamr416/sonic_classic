import pygame
import sys
import os
from game import Game
from sonic import Sonic
from map import Map
from ring import Ring
from camera import Camera

MAPS_DIR = 'maps'
pygame.init()
SIZE = WIDTH, HEIGHT = 1200, 1000
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
    MAP = Map('maps/map5.tmx', [1, 2], 2, 3152, 5)
    SONIC = Sonic((3, 12))
    game = Game(MAP, SONIC)
    SCREEN.fill((0, 0, 255))
    pygame.display.set_caption('Sonic classic')
    Game.update_sonic(game)
    pygame.quit()
