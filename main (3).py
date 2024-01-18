import pygame
import pytmx
import os


MAPS_DIR = 'maps'
pygame.init()
SIZE = WIDTH, HEIGHT = 1200, 600
SCREEN = pygame.display.set_mode(SIZE)
TILE_SIZE = 32
FPS = 120


class Map:
    def __init__(self, filename, free_tiles, finish_tiles):
        absolute_path = os.path.dirname(__file__)
        relative_path = f'{MAPS_DIR}/{filename}'
        full_path = os.path.join(absolute_path, relative_path)
        self.map = pytmx.load_pygame(f'{MAPS_DIR}/map3.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = 30
        self.free_tiles = free_tiles
        self.finish_tiles = finish_tiles

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position) -> int:
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position) -> bool:
        return self.get_tile_id(position) not in self.free_tiles


class Sonic:
    def __init__(self, picture, position):
        self.image = pygame.image.load(f"{picture}")
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        delta = (self.image.get_width() - TILE_SIZE) // 2
        screen.blit(self.image, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

    def jump(self, y):
        speed = 10
        last = speed
        almost_done = False
        if speed / FPS < last:
            last -= speed / FPS
            y += speed / FPS
            almost_done = True
        elif almost_done:
            y += last
            almost_done = False

        '''
        print(x, y)
        y += 1
        '''
        SCREEN.blit(self.image, (x, y))
        pygame.display.flip()
        clock.tick(FPS)


class Game:
    def __init__(self, map, sonic):
        self.map = map
        self.sonic = sonic

    def render(self, screen):
        self.map.render(screen)
        self.sonic.render(screen)

    def update_sonic(self):
        clock = pygame.time.Clock()
        next_x, next_y = self.sonic.get_position()
        JUMP = False
        count = 0
        running = True
        while running:
            if JUMP:
                next_y -= 1
                count += 1
                if count == 2:
                    JUMP = False
                    count = 0
            if not JUMP and self.map.is_free((next_x, next_y + 0.1)):
                next_y += 0.1
            if not self.map.is_free((next_x, next_y + 1)):
                next_y -= 0.1
            game.render(SCREEN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if pygame.key.get_pressed()[pygame.K_a]:
                    next_x -= 10/FPS
                if pygame.key.get_pressed()[pygame.K_d]:
                    next_x += 10/FPS
                if pygame.key.get_pressed()[pygame.K_SPACE] and not pygame.key.get_pressed()[pygame.K_s]:
                    #
                    next_y -= 1
                    '''
                    speed = 1
                    last = speed
                    
                    almost_done = False
                    while speed / FPS < last:
                        last -= speed / FPS
                        next_y -= speed / FPS
                        almost_done = True
                    if almost_done:
                        next_y -= last
                        almost_done = False
                    '''
                if pygame.key.get_pressed()[pygame.K_s] and pygame.key.get_pressed()[pygame.K_SPACE]:
                    next_y += 1
                if not self.map.is_free((next_x, next_y + 1)):
                    next_y -= 0.1
                self.sonic.set_position((next_x, next_y))
                print(self.sonic.get_position())
                clock.tick(fps)
                pygame.display.flip()



if __name__ == '__main__':
    MAP = Map('maps/map3.tmx', [0, 1, 2, 3, 4, 5],  3152)
    SONIC = Sonic("Sonic Sprites/tile000.png", (9, 4))
    game = Game(MAP, SONIC)
    fps = 120
    SCREEN.fill((0, 0, 255))
    pygame.display.set_caption('Sonic classic')
    clock = pygame.time.Clock()
    Game.update_sonic(game)
    pygame.quit()