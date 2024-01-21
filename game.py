import pygame


SIZE = WIDTH, HEIGHT = 1200, 600
FPS = 30
SCREEN = pygame.display.set_mode(SIZE)


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
        self.start_pic = pygame.image.load('start_win.jpg')

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
        gh_sound = pygame.mixer.Sound('music/GHzone.MP3')
        title_sound = pygame.mixer.Sound('music/Titlemus.MP3')
        over_sound = pygame.mixer.Sound('music/gameover.mp3')
        starting = True
        running = True
        ending = False
        title_sound.play()
        title_sound.set_volume(0.1)
        while starting:
            new_start_pic = pygame.transform.scale(self.start_pic, SIZE)
            SCREEN.blit(new_start_pic, (0, 0))
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
        JUMP = False
        jump_height = 3
        last_jump = 3
        count = 0
        gh_sound.play(-1)
        gh_sound.set_volume(0.1)
        while running:
            seconds = (pygame.time.get_ticks() - start_ticks) // 100
            if seconds >= 6000:
                running = False
                gh_sound.stop()
                ending = True
            if JUMP:
                if 0.5 ** count < last_jump:
                    next_y -= 0.5 ** count
                    last_jump -= 0.5 ** count
                else:
                    next_y -= last_jump
                    JUMP = False
                    count = 1
                    last_jump = 3
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
            if not JUMP and self.map.is_free((next_x, next_y + 2)):
                next_y += 0.5
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
                    and self.map.is_free((next_x, next_y + 1))):
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
                  and self.map.is_free((next_x, next_y + 1))):
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

            if pygame.key.get_pressed()[pygame.K_s] and pygame.key.get_pressed()[pygame.K_SPACE] and self.map.is_free(
                    (next_x, next_y + 2)):
                next_y += 1

            if not pygame.key.get_pressed()[pygame.K_d] and not pygame.key.get_pressed()[pygame.K_a]:
                self.last_way = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.map.is_free((next_x, next_y + 2)):
                        JUMP = True
            self.render(SCREEN)
            self.sonic.set_position((next_x, next_y))
            clock.tick(FPS)
            pygame.display.flip()
        over_sound.play()
        over_sound.set_volume(0.1)
        while ending:
            font = pygame.font.Font('font/sonic-press-start-button.otf', 30)
            text = font.render(f'GAME OVER', True, (255, 255, 0))
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            SCREEN.blit(text, text_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ending = False
            self.render(SCREEN)
            clock.tick(FPS)
