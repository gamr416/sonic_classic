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
                self.count_jump = 0
                next_y -= 1
                count += 1
                if count == 3:
                    JUMP = False
                    count = 0
            if not JUMP and self.map.is_free((next_x, next_y + 2)):
                next_y += 0.1
                '''
                if self.map.is_free((next_x, next_y + 0.1 ** self.count_jump)):
                    next_y += 0.1 ** self.count_jump
                else:
                    next_y += 1
                '''
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
            if (pygame.key.get_pressed()[pygame.K_a]
                    and not pygame.key.get_pressed()[pygame.K_d] and not pygame.key.get_pressed()[pygame.K_SPACE]
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
                # print(self.sonic.get_position(), not self.map.is_free((next_x, next_y + 2)),
                #      f'left-{self.left}, right-{self.right}, ll-{self.last_left}, lr-{self.last_right}')

            elif (pygame.key.get_pressed()[pygame.K_d]
                  and not pygame.key.get_pressed()[pygame.K_a]
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

                # print(self.sonic.get_position(), not self.map.is_free((next_x, next_y + 2)),
                #      f'left-{self.left}, right-{self.right}, ll-{self.last_left}, lr-{self.last_right}')
            else:
                self.left = False
                self.right = False

            if pygame.key.get_pressed()[pygame.K_SPACE] and not pygame.key.get_pressed()[pygame.K_s] \
                    and self.map.is_free((next_x, next_y - 2)) and not self.map.is_free((next_x, next_y + 2)):
                print(self.sonic.get_position(), not self.map.is_free((next_x, next_y - 2)),
                      f'left-{self.left}, right-{self.right}, ll-{self.last_left}, lr-{self.last_right}')
                JUMP = True
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
            if pygame.key.get_pressed()[pygame.K_s] and pygame.key.get_pressed()[pygame.K_SPACE] and self.map.is_free(
                    (next_x, next_y + 2)):
                next_y += 1

            if not pygame.key.get_pressed()[pygame.K_d] and not pygame.key.get_pressed()[pygame.K_a]:
                self.last_way = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type != pygame.key.get_pressed()[pygame.K_a] \
                        or event.type != pygame.key.get_pressed()[pygame.K_s] \
                        or event.type != pygame.key.get_pressed()[pygame.K_d] \
                        or event.type != pygame.key.get_pressed()[pygame.K_SPACE] \
                        or event.type != pygame.quit:
                    continue
            self.render(SCREEN)
            self.sonic.set_position((next_x, next_y))
            clock.tick(FPS)
            pygame.display.flip()
