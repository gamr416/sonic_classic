import pygame
import pytmx
import sys
import os

MAPS_DIR = 'maps'
pygame.init()
SIZE = WIDTH, HEIGHT = 1200, 600
SCREEN = pygame.display.set_mode(SIZE)
TILE_SIZE = 32
FPS = 30
left = False
right = False
run_left = [pygame.image.load('Sonic Sprites/tile008_копия.png'), pygame.image.load('Sonic Sprites/tile009_копия.png'),
            pygame.image.load('Sonic Sprites/tile010_копия.png'), pygame.image.load('Sonic Sprites/tile011_копия.png'),
            pygame.image.load('Sonic Sprites/tile012_копия.png'), pygame.image.load('Sonic Sprites/tile013_копия.png')]
run_right = [[pygame.image.load('Sonic Sprites/tile008.png'), pygame.image.load('Sonic Sprites/tile009.png'),
              pygame.image.load('Sonic Sprites/tile010.png'), pygame.image.load('Sonic Sprites/tile011.png'),
              pygame.image.load('Sonic Sprites/tile012.png'), pygame.image.load('Sonic Sprites/tile013.png')]]
idle = pygame.image.load('Sonic Sprites/tile000.png')
anim_iter = 0


class Map:
    def __init__(self, filename, bad_tiles, finish_tiles, level):
        absolute_path = os.path.dirname(__file__)
        relative_path = f'{MAPS_DIR}/{filename}'
        full_path = os.path.join(absolute_path, relative_path)
        self.map = pytmx.load_pygame(f'{MAPS_DIR}/map{level}.tmx')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = 30
        self.solid_tiles = bad_tiles
        self.finish_tiles = finish_tiles

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position) -> int:
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position) -> bool:
        return self.get_tile_id(position) not in self.solid_tiles


class Sonic:
    def __init__(self, picture, position):
        self.x, self.y = position
        self.run_left = [pygame.image.load('Sonic Sprites/tile008_копия.png'),
                         pygame.image.load('Sonic Sprites/tile009_копия.png'),
                         pygame.image.load('Sonic Sprites/tile010_копия.png'),
                         pygame.image.load('Sonic Sprites/tile011_копия.png'),
                         pygame.image.load('Sonic Sprites/tile012_копия.png'),
                         pygame.image.load('Sonic Sprites/tile013_копия.png')]
        self.run_right = [
            pygame.image.load('Sonic Sprites/tile008.png'), pygame.image.load('Sonic Sprites/tile009.png'),
            pygame.image.load('Sonic Sprites/tile010.png'), pygame.image.load('Sonic Sprites/tile011.png'),
            pygame.image.load('Sonic Sprites/tile012.png'), pygame.image.load('Sonic Sprites/tile013.png')]
        self.idle_right = pygame.image.load('Sonic Sprites/tile000.png')
        self.idle_left = pygame.image.load('Sonic Sprites/tile000_копия.png')
        self.jump_image = pygame.image.load('Sonic Sprites/tile036.png')
        self.anim_iter = 0

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render_left_run(self, screen):
        if self.anim_iter + 1 >= 30:
            self.anim_iter = 0
        delta = (self.run_left[self.anim_iter // 5].get_width() - TILE_SIZE) // 2
        screen.blit(self.run_left[self.anim_iter // 5], (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))
        self.anim_iter += 1

    def render_right_run(self, screen):
        if self.anim_iter + 1 >= 30:
            self.anim_iter = 0
        delta = (self.run_right[self.anim_iter // 5].get_width() - TILE_SIZE) // 2
        screen.blit(self.run_right[self.anim_iter // 5], (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))
        self.anim_iter += 1

    def render_idle_left(self, screen):
        delta = (self.idle_left.get_width() - TILE_SIZE) // 2
        screen.blit(self.idle_left, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

    def render_idle_right(self, screen):
        delta = (self.idle_right.get_width() - TILE_SIZE) // 2
        screen.blit(self.idle_right, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

    def jump(self, x, y):
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
        SCREEN.blit(self.jump_image, (x, y))
        pygame.display.flip()
        clock.tick(FPS)


class Game:
    def __init__(self, map, sonic):
        self.map = map
        self.sonic = sonic
        self.left = False
        self.last_left = False
        self.right = False
        self.last_right = True

    def render(self, screen):
        self.map.render(screen)
        if self.left:
            self.sonic.render_left_run(screen)
        elif self.right:
            self.sonic.render_right_run(screen)
        else:
            if self.last_left:
                self.sonic.render_idle_left(screen)
            elif self.last_right:
                self.sonic.render_idle_right(screen)

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
            if not JUMP and self.map.is_free((next_x, next_y + 2)):
                next_y += 0.1
            for event in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_d] and pygame.key.get_pressed()[pygame.K_SPACE] \
                        and not self.map.is_free((next_x, next_y + 2)):
                    next_y -= 30 / FPS
                    next_x += 10 / FPS
                if pygame.key.get_pressed()[pygame.K_a] and pygame.key.get_pressed()[pygame.K_SPACE] \
                        and not self.map.is_free((next_x, next_y + 2)):
                    next_y -= 30 / FPS
                    next_x -= 10 / FPS
                if event.type == pygame.QUIT:
                    running = False
                if pygame.key.get_pressed()[pygame.K_a]:
                    self.left = True
                    self.right = False
                    self.last_right = False
                    self.last_left = True
                    next_x -= 5 / FPS
                    print(self.sonic.get_position(), not self.map.is_free((next_x, next_y + 2)),
                          f'left-{self.left}, right-{self.right}, ll-{self.last_left}, lr-{self.last_right}')
                elif pygame.key.get_pressed()[pygame.K_d]:
                    self.left = False
                    self.right = True
                    self.last_right = True
                    self.last_left = False
                    next_x += 5 / FPS
                    print(self.sonic.get_position(), not self.map.is_free((next_x, next_y + 2)),
                          f'left-{self.left}, right-{self.right}, ll-{self.last_left}, lr-{self.last_right}')
                else:
                    self.left = False
                    self.right = False

                if pygame.key.get_pressed()[pygame.K_SPACE] and not pygame.key.get_pressed()[pygame.K_s] \
                        and not self.map.is_free((next_x, next_y + 2)):
                    print(self.sonic.get_position(), not self.map.is_free((next_x, next_y + 2)),
                          f'left-{self.left}, right-{self.right}, ll-{self.last_left}, lr-{self.last_right}')
                    next_y -= 30 / FPS
                    '''
                    speed = 1
                    last = speed
                    
                    almost_done = False
                    while speed / FPS < last:
                        last -= speed / FPS                             
                        next_y -= speed / FPS
                        almost_done = Trueaaad
                    if almost_done:
                        next_y -= last
                        almost_done = False
                    '''
                if pygame.key.get_pressed()[pygame.K_s] and pygame.key.get_pressed()[pygame.K_SPACE]:
                    next_y += 30 / FPS
                if event.type != pygame.key.get_pressed()[pygame.K_a] \
                        or event.type != pygame.key.get_pressed()[pygame.K_s] \
                        or event.type != pygame.key.get_pressed()[pygame.K_d] \
                        or event.type != pygame.key.get_pressed()[pygame.K_SPACE] \
                        or event.type != pygame.quit:
                    continue
            game.render(SCREEN)
            self.sonic.set_position((next_x, next_y))
            clock.tick(FPS)
            pygame.display.flip()


all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    # если файл не существует, то выходим
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image


if __name__ == '__main__':
    MAP = Map('maps/map3.tmx', [1, 50], 3152, 3)
    SONIC = Sonic("Sonic Sprites/tile000.png", (3, 12))
    game = Game(MAP, SONIC)
    SCREEN.fill((0, 0, 255))
    pygame.display.set_caption('Sonic classic')
    clock = pygame.time.Clock()
    Game.update_sonic(game)
    pygame.quit()
