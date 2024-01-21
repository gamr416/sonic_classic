import pygame

SIZE = WIDTH, HEIGHT = 1200, 600
FPS = 30
SCREEN = pygame.display.set_mode(SIZE)
TILE_SIZE = 32
clock = pygame.time.Clock()


class Sonic:
    def __init__(self, position):
        self.last_two = 0
        self.cur_frame = -1
        self.x, self.y = position
        self.start_x, self.start_y = 17, 17
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
        self.jump_iter = 0
        self.jump_sprites_right = [pygame.image.load('Sonic Sprites/tile032.png'),
                                   pygame.image.load('Sonic Sprites/tile033.png'),
                                   pygame.image.load('Sonic Sprites/tile034.png'),
                                   pygame.image.load('Sonic Sprites/tile035.png'),
                                   pygame.image.load('Sonic Sprites/tile036.png')]
        self.jump_sprites_left = [pygame.transform.flip(elements, True, False)
                                  for elements in self.jump_sprites_right]
        self.sprites_down = pygame.image.load('Sonic Sprites/tile006.png')
        self.start_screen_sonic = [pygame.image.load('Sonic Sprites/sonic_start_1.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_2.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_3.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_4.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_5.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_6.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_7.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_8.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_9.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_10.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_11.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_12.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_13.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_14.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_15.png'),
                                   pygame.image.load('Sonic Sprites/sonic_start_16.png')]
        self.start_screen_sonic_last = [pygame.image.load('Sonic Sprites/sonic_start_17.png'),
                                        pygame.image.load('Sonic Sprites/sonic_start_18.png'), ]
        self.start_screen_sonic = [
            pygame.transform.scale(elements, (elements.get_width() * 2, elements.get_height() * 2))
            for elements in self.start_screen_sonic]
        self.start_screen_sonic_last = [
            pygame.transform.scale(elements, (elements.get_width() * 2, elements.get_height() * 2))
            for elements in self.start_screen_sonic_last]
        self.rect = self.jump_image.get_rect()

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render_start_sonic(self, screen):
        if self.cur_frame != 300:
            self.cur_frame += 1
            needed_frame = self.cur_frame // 20
            image = self.start_screen_sonic[needed_frame]
        else:
            self.last_two = self.last_two + 1
            needed_frame = (self.last_two // 25) % 2
            image = self.start_screen_sonic_last[needed_frame]
        screen.blit(image, (WIDTH // 4, HEIGHT // 15))

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

    def render_jump_right(self, screen):
        if self.jump_iter + 1 >= 10:
            self.jump_iter = 0
        delta = (self.jump_sprites_right[self.jump_iter // 2].get_width() - TILE_SIZE) // 2
        screen.blit(self.jump_sprites_right[self.jump_iter // 2],
                    (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))
        if self.jump_iter != 8:
            self.jump_iter += 1

    def render_jump_left(self, screen):
        if self.jump_iter + 1 >= 10:
            self.jump_iter = 0
        delta = (self.jump_sprites_left[self.jump_iter // 2].get_width() - TILE_SIZE) // 2
        screen.blit(self.jump_sprites_left[self.jump_iter // 2],
                    (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))
        if self.jump_iter != 8:
            self.jump_iter += 1

    def render_down_right(self, screen):
        delta = (self.sprites_down.get_width() - TILE_SIZE) // 2
        screen.blit(self.sprites_down, (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))

    def render_down_left(self, screen):
        delta = (pygame.transform.flip(self.sprites_down, True, False).get_width() - TILE_SIZE) // 2
        screen.blit(pygame.transform.flip(self.sprites_down, True, False),
                    (self.x * TILE_SIZE - delta, self.y * TILE_SIZE - delta))
