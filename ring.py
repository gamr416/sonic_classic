import pygame

SIZE = WIDTH, HEIGHT = 1200, 600
FPS = 30
SCREEN = pygame.display.set_mode(SIZE)
TILE_SIZE = 40


class Ring:
    def __init__(self, x, y):
        self.rings = [pygame.image.load('Sonic Sprites/ring_1.png'), pygame.image.load('Sonic Sprites/ring_2.png'),
                      pygame.image.load('Sonic Sprites/ring_3.png'), pygame.image.load('Sonic Sprites/ring_4.png')]
        self.anim_iter = 0
        self.x, self.y = x, y

    def get_position(self):
        return self.x, self.y

    def render(self, screen):
        if self.anim_iter + 1 >= 24:
            self.anim_iter = 0
        delta = (self.rings[self.anim_iter // 6].get_width() - TILE_SIZE) // 2
        screen.blit(self.rings[self.anim_iter // 6],
                    (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))
