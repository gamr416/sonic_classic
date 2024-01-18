import pygame
import pytmx
import os


MAPS_DIR = 'maps'
pygame.init()
SIZE = WIDTH, HEIGHT = 1200, 720
SCREEN = pygame.display.set_mode(SIZE)
TILE_SIZE = 32
FPS = 30


class Map:
    def __init__(self, filename, free_tiles, finish_tiles):
        absolute_path = os.path.dirname(__file__)
        relative_path = f'{MAPS_DIR}/{filename}'
        full_path = os.path.join(absolute_path, relative_path)
        self.map = pytmx.load_pygame('maps/map2.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = 6
        self.free_tiles = free_tiles
        self.finish_tiles = finish_tiles

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position):
        return self.get_tile_id(position) not in self.free_tiles


class Game:
    def __init__(self, map):
        self.map = map

    def render(self, screen):
        self.map.render(screen)



def load_image(name, colorkey=None):
    absolute_path = os.path.dirname(__file__)
    relative_path = 'data/gameover.png'
    full_path = os.path.join(absolute_path, relative_path)
    # если файл не существует, то выходим
    if not os.path.isfile(full_path):
        print(f"Файл с изображением '{full_path}' не найден")
        exit()
    image = pygame.image.load(full_path)
    return image




if __name__ == '__main__':
    MAP = Map('maps/map2.tmx', [0, 1, 2, 3, 4, 5], 3182)
    game = Game(MAP)
    SCREEN.fill((0, 0, 255))
    pygame.display.set_caption('conic klassic')
    running = True
    clock = pygame.time.Clock()
    while running:
        game.render(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()

