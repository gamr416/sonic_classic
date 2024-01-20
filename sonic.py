import pygame


SIZE = WIDTH, HEIGHT = 1200, 600
FPS = 30
SCREEN = pygame.display.set_mode(SIZE)
TILE_SIZE = 30


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