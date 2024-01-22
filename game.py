import pygame

SIZE = WIDTH, HEIGHT = 1200, 600
SCREEN = pygame.display.set_mode(SIZE)
FPS = 30
TILE_SIZE = 40


class Game:
    def __init__(self, map, sonic):
        self.map = map
        self.sonic = sonic
        self.left = False
        self.last_left = False
        self.right = False
        self.last_right = True
        self.last_way = None
        self.counter_way = 0
        self.MAX_COUNTER_WAY = 4
        self.count_jump = 0
        self.bg_pic = pygame.image.load('Sonic Sprites/background.jpg')
        self.second_bg = self.bg_pic
        self.JUMP = False
        self.fall_after_jump = False
        self.down = False
        self.bg_pic_x = 0
        self.second_bg_x = self.second_bg.get_width()
        self.first_screen = False
        self.second_screen = False
        self.flag_start_bg = False
        self.world_offset = [0, 0]


    def blit_all_tiles(self, window, tmxdata, world_offset):
        for layer in tmxdata:
            for tile in layer.tiles():
                img = pygame.transform.scale(tile[2], (40, 40))
                x_pixel = tile[0] * 40 + world_offset[0]
                y_pixel = tile[1] * 40 + world_offset[1]
                window.blit(img, (x_pixel, y_pixel))

    def render(self, screen):
        self.map.render(screen)
        if self.JUMP or self.fall_after_jump and self.last_right:
            self.sonic.render_jump_right(screen)
        elif self.JUMP or self.fall_after_jump and self.last_left:
            self.sonic.render_jump_left(screen)
        elif self.left and not self.JUMP and not self.fall_after_jump:
            self.sonic.render_left_run(screen)
        elif self.right and not self.JUMP and not self.fall_after_jump:
            self.sonic.render_right_run(screen)
        elif self.down and self.last_right:
            self.sonic.render_down_right(screen)
        elif self.down and self.last_left:
            self.sonic.render_down_left(screen)
        else:
            if self.last_left:
                self.sonic.render_idle_left(screen)
            elif self.last_right:
                self.sonic.render_idle_right(screen)


    def update_sonic(self):
        gh_sound = pygame.mixer.Sound('music/GHzone.MP3')
        title_sound = pygame.mixer.Sound('music/Titlemus.MP3')
        over_sound = pygame.mixer.Sound('music/gameover.mp3')

        starting = True
        running = True
        ending = False
        title_sound.play()
        title_sound.set_volume(0.1)
        start_ticks = pygame.time.get_ticks()
        while starting:
            starting_seconds = (pygame.time.get_ticks() - start_ticks) // 100
            self.bg_pic_x -= 20 / FPS
            self.second_bg_x -= 20 / FPS
            if self.bg_pic_x + self.second_bg.get_width() <= WIDTH and self.flag_start_bg:
                self.second_bg_x = WIDTH
                self.flag_start_bg = False
            if self.second_bg_x + self.bg_pic.get_width() <= WIDTH and not self.flag_start_bg:
                self.bg_pic_x = WIDTH
                self.flag_start_bg = True
            SCREEN.blit(self.bg_pic, (self.bg_pic_x, 0))
            SCREEN.blit(self.second_bg, (self.second_bg_x, 0))
            self.sonic.render_start_sonic(SCREEN)
            if starting_seconds >= 5:
                font = pygame.font.Font('font/sonic-press-start-button.otf', 20)
                text = font.render('PRESS SPACE TO START', True, (255, 255, 0))
                text_rect = text.get_rect(center=(WIDTH / 40 * 19, HEIGHT / 40 * 31))
                SCREEN.blit(text, text_rect)
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    starting = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    starting = False
                    running = False
            pygame.display.flip()
        title_sound.stop()
        clock = pygame.time.Clock()
        next_x, next_y = self.sonic.get_position()
        jump_height = 3
        last_jump = 3
        max_jump = False
        count = 0
        gh_sound.play(-1)
        gh_sound.set_volume(0.1)
        playing_ticks = pygame.time.get_ticks()
        SCREEN.fill((0, 0, 0))
        while running:
            self.bg_pic_x -= 20 / FPS
            self.second_bg_x -= 20 / FPS
            if self.bg_pic_x + self.second_bg.get_width() <= WIDTH and self.flag_start_bg:
                self.second_bg_x = WIDTH
                self.flag_start_bg = False
            if self.second_bg_x + self.bg_pic.get_width() <= WIDTH and not self.flag_start_bg:
                self.bg_pic_x = WIDTH
                self.flag_start_bg = True
            SCREEN.blit(self.bg_pic, (self.bg_pic_x, 0))
            SCREEN.blit(self.second_bg, (self.second_bg_x, 0))
            self.map.render(SCREEN)
            self.blit_all_tiles(SCREEN, self.map.map, self.world_offset)
            self.render(SCREEN)
            seconds = (pygame.time.get_ticks() - playing_ticks) // 100
            if seconds >= 6000:
                running = False
                gh_sound.stop()
                ending = True
            if self.JUMP:
                if 0.5 ** count < last_jump and self.map.is_free((next_x, next_y - 0.5 ** count)):
                    next_y -= 0.5 ** count
                    last_jump -= 0.5 ** count
                elif 0.5 ** count >= last_jump and self.map.is_free((next_x, next_y - 0.5 ** count)):
                    next_y -= last_jump
                    count = 1
                    last_jump = 3
                    self.JUMP = False
                    self.fall_after_jump = True
                if self.last_way == 'RIGHT':
                    if self.counter_way > self.MAX_COUNTER_WAY:
                        next_x += (2 ** (1 / 2 * self.MAX_COUNTER_WAY)) / FPS
                    else:
                        next_x += (2 ** (1 / 2 * self.counter_way)) / FPS
                elif self.last_way == 'LEFT':
                    if self.counter_way > self.MAX_COUNTER_WAY:
                        next_x -= (2 ** (1 / 2 * self.MAX_COUNTER_WAY)) / FPS
                    else:
                        next_x -= (2 ** (1 / 2 * self.counter_way)) / FPS
            if not self.JUMP and self.map.is_free((next_x, next_y)):
                print(1)
                self.world_offset[1] -= 5
                if self.last_way == 'RIGHT':
                    if self.counter_way > self.MAX_COUNTER_WAY:
                        next_x += (2 ** (1 / 2 * self.MAX_COUNTER_WAY)) / FPS
                    else:
                        next_x += (2 ** (1 / 2 * self.counter_way)) / FPS
                elif self.last_way == 'LEFT':
                    if self.counter_way > self.MAX_COUNTER_WAY:
                        next_x -= (2 ** (1 / 2 * self.MAX_COUNTER_WAY)) / FPS
                    else:
                        next_x -= (2 ** (1 / 2 * self.counter_way)) / FPS
            if not self.map.is_free((next_x, next_y)):
                self.fall_after_jump = False
            '''
            if pygame.key.get_pressed()[pygame.K_d] and pygame.key.get_pressed()[pygame.K_SPACE] \
                    and not self.map.is_free((next_x, next_y + 2)):
                JUMP = True
                if self.counter_way > self.MAX_COUNTER_WAY:
                    next_x += (2 ** self.MAX_COUNTER_WAY) / FPS
                else:
                    next_x += (2 ** self.counter_way) / FPS
            if pygame.key.get_pressed()[pygame.K_a] and pygame.key.get_pressed()[pygame.K_SPACE] \
                    and not self.map.is_free((next_x, next_y + 2)):
                next_y -= 3
                next_x -= 1
            '''
            if (pygame.key.get_pressed()[pygame.K_a]
                    and self.map.is_free((next_x, next_y))):
                if self.last_way != 'LEFT':
                    self.counter_way = 2
                    self.left = True
                    self.right = False
                    self.last_right = False
                    self.last_left = True
                    next_x -= 2 ** self.MAX_COUNTER_WAY / FPS
                else:
                    self.counter_way += 0.05
                    if self.counter_way > self.MAX_COUNTER_WAY:
                        next_x -= (2 ** self.MAX_COUNTER_WAY) / FPS
                    else:
                        next_x -= (2 ** self.counter_way) / FPS
                self.last_way = 'LEFT'
            elif (pygame.key.get_pressed()[pygame.K_d]
                  and self.map.is_free((next_x, next_y))):
                if self.last_way != 'RIGHT':
                    self.counter_way = 2
                    self.left = False
                    self.right = True
                    self.last_right = True
                    self.last_left = False
                    next_x += 4 / FPS
                else:
                    self.counter_way += 0.05
                    if self.counter_way > self.MAX_COUNTER_WAY:
                        next_x += (2 ** self.MAX_COUNTER_WAY) / FPS
                    else:
                        next_x += (2 ** self.counter_way) / FPS
                self.last_way = 'RIGHT'
            else:
                self.left = False
                self.right = False

            if (pygame.key.get_pressed()[pygame.K_s]
                    and not pygame.key.get_pressed()[pygame.K_SPACE]
                    and not self.map.is_free((next_x, next_y))
                    and not pygame.key.get_pressed()[pygame.K_a]
                    and not pygame.key.get_pressed()[pygame.K_d]):
                self.down = True

            if not pygame.key.get_pressed()[pygame.K_s]:
                self.down = False

            if pygame.key.get_pressed()[pygame.K_s] and pygame.key.get_pressed()[pygame.K_SPACE] and self.map.is_free(
                    (next_x, next_y)):
                next_y += 1

            if not pygame.key.get_pressed()[pygame.K_d] and not pygame.key.get_pressed()[pygame.K_a]:
                self.last_way = None

            if next_x > 22:
                next_x = 22
                self.world_offset[0] -= 10
            if next_x < 18:
                next_x = 18
                self.world_offset[0] += 10

            # if next_y >= HEIGHT / TILE_SIZE - 10 and self.map.is_free((next_x, next_y + 4)):
            #     next_y = HEIGHT / TILE_SIZE - 10
            #     self.world_offset[1] -= 4
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_SPACE
                            and not pygame.key.get_pressed()[pygame.K_s]
                            and not self.map.is_free((next_x, next_y))):
                        self.JUMP = True
                        self.sonic.jump_iter = 0
            font = pygame.font.Font('font/sonic-press-start-button.otf', 10)
            text = font.render(f'TIME {seconds // 600} {seconds % 600}', True, (255, 255, 0))
            SCREEN.blit(text, (10, 10))
            pygame.display.flip()
            self.sonic.set_position((next_x, next_y))
            clock.tick(FPS)
            pygame.display.flip()
        over_sound.play()
        over_sound.set_volume(0.1)
        while ending:
            font = pygame.font.Font('font/sonic-press-start-button.otf', 30)
            text = font.render(f'TIME OVER', True, (255, 255, 0))
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            SCREEN.blit(text, text_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ending = False
            self.render(SCREEN)
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
