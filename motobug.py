import pygame


SIZE = WIDTH, HEIGHT = 1200, 600
FPS = 30
SCREEN = pygame.display.set_mode(SIZE)
TILE_SIZE = 40
clock = pygame.time.Clock()


class Motobug:
    def __init__(self, position, away_x, away_y):
        self.x, self.y = position
        self.start_x, self.start_y = 17, 17
        self.image1_right = pygame.image.load('Sonic Sprites/motobug1.png')
        self.image1_left = pygame.transform.flip(self.image1_right, True, False)
        self.image2_right = pygame.image.load('Sonic Sprites/motobug2.png')
        self.image2_left = pygame.transform.flip(self.image2_right, True, False)
        self.away_x = away_x
        self.away_y = away_y

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render1_right(self, screen):
        screen.blit(self.image1_right, (self.x * TILE_SIZE, self.y * TILE_SIZE))

    def render1_left(self, screen):
        screen.blit(self.image1_left, (self.x * TILE_SIZE, self.y * TILE_SIZE))

    def render2_right(self, screen):
        screen.blit(self.image1_left, (self.x * TILE_SIZE, self.y * TILE_SIZE))

    def render2_left(self, screen):
        screen.blit(self.image2_left, (self.x * TILE_SIZE, self.y * TILE_SIZE))


